// Turns each .methods group into tabs: a reader following a how-to picks one method,
// so only that one shows. Without this script, or on paper, every method stacks.
document.querySelectorAll(".methods").forEach((group, g) => {
  const panels = [...group.querySelectorAll(":scope > .method")];
  if (panels.length < 2) return;
  const list = document.createElement("div");
  list.setAttribute("role", "tablist");
  const tabs = panels.map((panel, i) => {
    const tab = document.createElement("button");
    tab.type = "button";
    tab.setAttribute("role", "tab");
    tab.id = `methods-${g}-tab-${i}`;
    panel.id ||= `methods-${g}-panel-${i}`;
    tab.setAttribute("aria-controls", panel.id);
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tab.id);
    tab.textContent = panel.querySelector("h2")?.textContent ?? "";
    list.append(tab);
    return tab;
  });
  const select = (i) => tabs.forEach((tab, j) => {
    tab.setAttribute("aria-selected", String(i === j));
    tab.tabIndex = i === j ? 0 : -1;
    panels[j].hidden = i !== j;
  });
  list.addEventListener("click", (e) => { const i = tabs.indexOf(e.target.closest("[role=tab]")); if (i >= 0) select(i); });
  list.addEventListener("keydown", (e) => {
    const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
    if (!step) return;
    const i = (tabs.indexOf(document.activeElement) + step + tabs.length) % tabs.length;
    select(i); tabs[i].focus();
  });
  group.prepend(list);
  select(0);
});
