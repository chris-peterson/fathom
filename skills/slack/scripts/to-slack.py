#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""Convert a markdown draft to Slack markup, print it, and copy it to the clipboard.

Usage: to-slack.py [--no-copy] < draft.md

Rewrites the syntax Slack renders differently (bold, italic, strikethrough,
headings, bullets, the API-only `<url|text>` and `<url>` link forms, which the
composer breaks on a paste), drops a terminal prompt marker
(`❯`, `›`, `$`, `%`) from the start of a block quote, and leaves code spans and
fenced blocks untouched.

Refuses what a regex can't fix rather than letting it reach the channel: a table
row outside a code block, which Slack renders as raw pipes, and anywhere in the
draft, code blocks included, a value shaped like a secret or a path under a
home directory, which names its user and opens for no reader.

Copies with pbcopy; --no-copy only prints, for a session whose clipboard isn't
the user's (a remote host).

Exit codes:
  0  converted and copied; stdout is the message
  1  pbcopy missing or failed
  2  stderr names each line to rewrite; nothing was copied
"""
import re
import shutil
import subprocess
import sys

FENCE = re.compile(r"^(```|~~~)")
CODE_SPAN = re.compile(r"`[^`\n]+`")
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
PROMPT_MARKER = re.compile(r"^(\s*>\s*(?:\*\*|__|\*|_)?)(?:❯|›|\$|%)\s+")
SECRET = re.compile(
    r"\bAKIA[0-9A-Z]{16}\b"
    r"|\bgh[pousr]_[A-Za-z0-9]{36,}"
    r"|\bglpat-[A-Za-z0-9_-]{20,}"
    r"|\bxox[abporse]-[A-Za-z0-9-]{10,}"
    r"|\bsk-[A-Za-z0-9_-]{20,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
)
HOME_PATH = re.compile(r"(?<![\w.~])(?:/Users/|/home/|[A-Za-z]:\\Users\\)[^/\\\s`'\"]+")


def convert_prose(line):
    spans = []

    def hold(m):
        spans.append(m.group(0))
        return f"\x00{len(spans) - 1}\x00"

    line = PROMPT_MARKER.sub(r"\1", line)
    line = CODE_SPAN.sub(hold, line)
    line = re.sub(r"<(https?://[^|>\s]+)\|([^>]+)>", r"[\2](\1)", line)
    line = re.sub(r"(?<!\]\()<(https?://[^|>\s]+)>", r"\1", line)
    heading = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
    if heading:
        line = f"\x01{heading.group(1)}\x01"
    line = re.sub(r"^(\s*)[-*+]\s+", r"\1• ", line)
    line = re.sub(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", "\x01\\2\x01", line)
    line = re.sub(r"(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])", r"_\1_", line)
    line = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"~\1~", line)
    line = re.sub("\x01+", "*", line)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], line)


def exposure(n, line):
    found = []
    if SECRET.search(line):
        found.append(f"line {n}: looks like a secret value (name the secret instead)")
    if HOME_PATH.search(line):
        found.append(f"line {n}: a path under a home directory (link the forge file or drop it)")
    return found


def convert(text):
    out, problems, fence = [], [], None
    for n, line in enumerate(text.splitlines(), 1):
        problems += exposure(n, line)
        opener = FENCE.match(line)
        if fence:
            out.append(line)
            if opener and opener.group(1) == fence:
                fence = None
            continue
        if opener:
            fence = opener.group(1)
            out.append(opener.group(1))
            continue
        if TABLE_ROW.match(line):
            problems.append(f"line {n}: table row (Slack renders none; a list, or a code block in a transcript)")
        out.append(convert_prose(line))
    return "\n".join(out).strip() + "\n", problems


def main():
    copy = "--no-copy" not in sys.argv[1:]
    slack, problems = convert(sys.stdin.read())
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(2)
    if copy:
        if not shutil.which("pbcopy"):
            sys.exit("pbcopy not found; rerun with --no-copy")
        subprocess.run(["pbcopy"], input=slack, text=True, check=True)
    sys.stdout.write(slack)


if __name__ == "__main__":
    main()
