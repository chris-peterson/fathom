#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.45", "pypdf>=4", "pypdfium2>=4", "pillow>=10"]
# ///
"""Render an HTML page to a PDF, scaled to fit a fixed number of pages.

Usage: to-pdf.py <page.html | url> <out.pdf> [--paper letter|a4] [--landscape]
                 [--pages N | --paginate] [--min-scale 0.75] [--margin 0.4in]
                 [--css extra.css] [--preview DIR] [--links-from original.html]
                 [--record DIR]

Prints with the installed Google Chrome (Playwright's `chrome` channel), in the
light color scheme with print media, so an artifact's dark theme and screen-only
chrome don't reach the paper; assets/print.css goes in first, then any --css.
A layout fits when its PDF lands on N pages and nothing runs past the right
margin. The fit is decided by rendering real PDFs and counting their pages: the
largest scale in [min-scale, 1] that fits wins.

--preview writes PNGs of the first three pages and the last to DIR, so the
result can be looked at without poppler. --links-from loads the original page a
one-pager was written from and reports which of its links the PDF kept, leaving
out claude.ai links, which readers without a license can't open. A warning line
follows when the page's H1 wraps onto a second line.

A page stamped with <meta name="fathom-version"> is a fathom view: it prints
only with --record naming its record, after `fathom check` passes against it.

Exit codes:
  0  written; stdout reports pages, scale, link count, and path
  3  too many pages at --min-scale; stdout reports the page count at 100% and
     at the floor, plus any width overflow; nothing written
  4  the page count fits, but content runs past the right margin and would be
     clipped; stdout names the widest elements; nothing written
  5  a fathom view failed `fathom check`, or has no --record; nothing written
  1  Chrome, Playwright, or the page failed to load
"""
import argparse
import io
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pypdfium2
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

PAPER_INCHES = {"letter": (8.5, 11.0), "a4": (8.27, 11.69)}
PAPER_FORMAT = {"letter": "Letter", "a4": "A4"}
PRINT_CSS = Path(__file__).resolve().parent.parent / "assets" / "print.css"
CSS_PX_PER_INCH = 96
SCALE_TOLERANCE = 0.01
PREVIEW_DPI = 110
UNOPENABLE = re.compile(r"https://claude\.ai/")
FATHOM_STAMP = re.compile(r"<meta[^>]+name=[\"']fathom-version[\"']", re.I)
FATHOM = Path(__file__).resolve().parents[3] / "scripts" / "fathom"

# The outermost elements whose right edge passes the viewport, widest first.
WIDEST_JS = """() => {
  const limit = window.innerWidth + 1;
  const over = new Set([...document.body.querySelectorAll('*')]
    .filter(el => el.getBoundingClientRect().right > limit));
  const outermost = [...over].filter(el => {
    for (let p = el.parentElement; p; p = p.parentElement) if (over.has(p)) return false;
    return true;
  });
  return outermost
    .map(el => {
      const r = el.getBoundingClientRect();
      const cls = el.classList.length ? '.' + el.classList[0] : '';
      const text = el.textContent.trim().replace(/\\s+/g, ' ').slice(0, 40);
      return {past: Math.round(r.right - window.innerWidth), width: Math.round(r.width),
              what: `${el.tagName.toLowerCase()}${cls} "${text}"`};
    })
    .sort((a, b) => b.past - a.past)
    .slice(0, 5);
}"""


# Lines the first H1 occupies: the distinct tops of its text's line boxes.
H1_LINES_JS = """() => {
  const h = document.querySelector('h1');
  if (!h) return 0;
  const range = document.createRange();
  range.selectNodeContents(h);
  return new Set([...range.getClientRects()].map(r => Math.round(r.top))).size;
}"""


@dataclass
class Render:
    scale: float
    pdf: bytes
    pages: int
    widest: list
    h1_lines: int

    @property
    def overflow(self):
        return self.widest[0]["past"] if self.widest else 0


def inches(value):
    if value == "0":
        return 0.0
    if value.endswith("in"):
        return float(value[:-2])
    if value.endswith("mm"):
        return float(value[:-2]) / 25.4
    raise argparse.ArgumentTypeError(f"margin needs an in or mm unit: {value}")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source")
    p.add_argument("out", type=Path)
    p.add_argument("--paper", choices=PAPER_INCHES, default="letter")
    p.add_argument("--landscape", action="store_true")
    p.add_argument("--pages", type=int, default=1)
    p.add_argument("--paginate", action="store_true", help="print at 100%% on as many pages as it takes")
    p.add_argument("--min-scale", type=float, default=0.75)
    p.add_argument("--margin", type=inches, default=inches("0.4in"))
    p.add_argument("--css", type=Path, help="extra stylesheet injected after assets/print.css")
    p.add_argument("--preview", type=Path, help="directory for PNGs of the first three pages and the last")
    p.add_argument("--links-from", help="the original page (file or URL); reports which of its links the PDF kept")
    p.add_argument("--record", help="the fathom record a stamped view was rendered from; checked before printing")
    return p.parse_args()


def source_url(source):
    if "://" in source:
        return source
    path = Path(source).expanduser().resolve()
    if not path.is_file():
        sys.exit(f"no such file: {path}")
    return path.as_uri()


class Printer:
    def __init__(self, page, args):
        self.page = page
        self.args = args
        width, height = PAPER_INCHES[args.paper]
        if args.landscape:
            width, height = height, width
        self.printable_px = round((width - 2 * args.margin) * CSS_PX_PER_INCH)

    def render(self, scale):
        # Chrome lays a scaled print out at page-width / scale; matching the
        # viewport lets JS-drawn charts size themselves to that width, and lets
        # WIDEST_JS measure the same layout the PDF gets.
        self.page.set_viewport_size({"width": round(self.printable_px / scale), "height": 1000})
        self.page.wait_for_timeout(250)
        widest = self.page.evaluate(WIDEST_JS)
        h1_lines = self.page.evaluate(H1_LINES_JS)
        margin = f"{self.args.margin}in"
        pdf = self.page.pdf(
            format=PAPER_FORMAT[self.args.paper],
            landscape=self.args.landscape,
            print_background=True,
            scale=scale,
            margin={"top": margin, "right": margin, "bottom": margin, "left": margin},
        )
        return Render(scale, pdf, len(PdfReader(io.BytesIO(pdf)).pages), widest, h1_lines)

    def fits(self, r):
        return r.pages <= self.args.pages and not r.overflow


def fit(printer, args):
    """Return (chosen render or None, the render at 100%, the render at the floor)."""
    full = printer.render(1.0)
    if args.paginate:
        return (None if full.overflow else full), full, full
    if printer.fits(full):
        return full, full, full
    floor = printer.render(args.min_scale)
    if not printer.fits(floor):
        return None, full, floor
    lo, hi, best = args.min_scale, 1.0, floor
    while hi - lo > SCALE_TOLERANCE:
        mid = printer.render((lo + hi) / 2)
        if printer.fits(mid):
            lo, best = mid.scale, mid
        else:
            hi = mid.scale
    return best, full, floor


def link_uris(pdf):
    pages = PdfReader(io.BytesIO(pdf)).pages
    actions = (a.get_object().get("/A") or {} for page in pages for a in page.get("/Annots") or [])
    return [str(action["/URI"]) for action in actions if "/URI" in action]


def page_links(browser, url):
    page = browser.new_page()
    try:
        page.goto(url, wait_until="networkidle")
    except PlaywrightError as e:
        sys.exit(f"could not load {url}: {e}")
    page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    return set(page.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => /^https?:/.test(h))"))


def report_links(kept, source, label):
    unopenable = {u for u in source if UNOPENABLE.match(u)}
    wanted = source - unopenable
    missing = sorted(wanted - kept)
    print(f"links: kept {len(wanted & kept)} of {len(wanted)} from {label}"
          + (f" ({len(unopenable)} claude.ai links left out)" if unopenable else ""))
    for u in missing[:10]:
        print(f"  missing: {u}")
    if len(missing) > 10:
        print(f"  … and {len(missing) - 10} more")


def report_widest(r):
    print(f"too wide: content runs {r.overflow}px past the right margin at {r.scale:.0%}; widest:")
    for w in r.widest:
        print(f"  {w['what']}  {w['width']}px wide, {w['past']}px past")


def write_previews(pdf_path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pypdfium2.PdfDocument(str(pdf_path))
    count = len(doc)
    wanted = sorted({i for i in (0, 1, 2, count - 1) if 0 <= i < count})
    paths = []
    for i in wanted:
        path = out_dir / f"{pdf_path.stem}-p{i + 1}.png"
        doc[i].render(scale=PREVIEW_DPI / 72).to_pil().save(path)
        paths.append(path)
    return paths


def check_view(args):
    if "://" in args.source or not FATHOM_STAMP.search(Path(args.source).expanduser().read_text()):
        return
    if not args.record:
        print("this page is a fathom view; pass --record <dir> so it is checked before it prints")
        sys.exit(5)
    result = subprocess.run([str(FATHOM), "check", args.source, "--record", args.record])
    if result.returncode != 0:
        sys.exit(5 if result.returncode == 3 else 1)


def main():
    args = parse_args()
    url = source_url(args.source)
    check_view(args)
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel="chrome")
        except PlaywrightError as e:
            sys.exit(f"could not launch Google Chrome: {e}")
        page = browser.new_page(color_scheme="light")
        try:
            page.goto(url, wait_until="networkidle")
        except PlaywrightError as e:
            sys.exit(f"could not load {url}: {e}")
        page.emulate_media(media="print", color_scheme="light")
        page.evaluate("document.documentElement.setAttribute('data-theme', 'light')")
        page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        page.add_style_tag(path=str(PRINT_CSS))
        if args.css:
            page.add_style_tag(path=str(args.css))
        page.evaluate("document.fonts.ready.then(() => true)")

        chosen, full, floor = fit(Printer(page, args), args)
        source_links = page_links(browser, source_url(args.links_from)) if args.links_from else None
        browser.close()

    if chosen is None:
        if floor.pages > args.pages and not args.paginate:
            print(f"does not fit: {full.pages} pages at 100%, {floor.pages} pages at {floor.scale:.0%}")
            if floor.overflow:
                report_widest(floor)
            sys.exit(3)
        report_widest(floor)
        sys.exit(4)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(chosen.pdf)
    natural = f" (was {full.pages} pages at 100%)" if chosen is not full else ""
    uris = link_uris(chosen.pdf)
    print(f"{chosen.pages} page(s), {args.paper}{' landscape' if args.landscape else ''}, scale {chosen.scale:.0%}{natural}, {len(uris)} links")
    print(f"{args.out.resolve()} ({len(chosen.pdf) // 1024} KB)")
    if source_links is not None:
        report_links(set(uris), source_links, args.links_from)
    if chosen.h1_lines > 1:
        print(f"warning: the H1 wraps to {chosen.h1_lines} lines; shorten it")
    if args.preview:
        for path in write_previews(args.out, args.preview):
            print(f"preview: {path}")


if __name__ == "__main__":
    main()
