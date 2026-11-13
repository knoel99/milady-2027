#!/usr/bin/env python3
"""Shared Quarto front matter for every page of the site (English only).

`up` is the relative path to the site root (where assets/ lives):
index.qmd → "", report/index.qmd → "../", prep/p1-x/index.qmd → "../../".
"""

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.19.0/dist/katex.min.js"

UI = {"skip": "Skip to content", "contents": "Contents", "theme": "Theme", "home": "← Home",
      "prep": "Preparation", "sup": "Supervisors", "report": "Internship report", "thesis": "PhD proposal",
      "exp": "Experiments", "interactive": "Interactive diagrams", "calc": "Computing and data",
      "teams": "Teams"}


def header(title: str, subtitle: str, up: str) -> str:
    u = UI
    home = up
    return f'''---
title: "{title}"
subtitle: "{subtitle}"
lang: en
format:
  html:
    theme: none
    minimal: true
    toc: false
    anchor-sections: false
    html-math-method:
      method: katex
      url: "{KATEX}"
    highlight-style: github
    embed-resources: false
    css: {up}assets/paper.css
    include-in-header:
      - text: |
          <meta name="color-scheme" content="light dark">
          <script>(function(){{try{{var t=localStorage.getItem("milady-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();</script>
    include-before-body:
      - text: |
          <a class="skip" href="#main">{u["skip"]}</a>
          <header class="topbar">
            <button type="button" class="tb-btn" id="toc-toggle" aria-controls="sidetoc" aria-expanded="false"><span aria-hidden="true">☰</span><span class="tb-label">{u["contents"]}</span></button>
            <a class="brand" href="{home}index.html">MilaDy<span class="brand-sub"> · 2027</span></a>
            <span class="tb-title" id="tb-title"></span>
            <button type="button" class="tb-btn" id="theme-toggle"><span aria-hidden="true">◐</span><span class="tb-label">{u["theme"]}</span></button>
          </header>
          <div class="layout">
          <nav class="sidetoc" id="sidetoc" aria-label="{u["contents"]}"></nav>
          <main class="paper" id="main">
    include-after-body:
      - text: |
          </main>
          </div>
          <footer class="foot"><p><a href="{home}index.html">{u["home"]}</a> · <a href="{home}prep/index.html">{u["prep"]}</a> · <a href="{home}supervisors/index.html">{u["sup"]}</a> · <a href="{home}report/index.html">{u["report"]}</a> · <a href="{home}thesis/index.html">{u["thesis"]}</a> · <a href="{home}interactive/index.html">{u["interactive"]}</a> · <a href="{home}experiments/index.html">{u["exp"]}</a> · <a href="{home}computing/index.html">{u["calc"]}</a> · <a href="{home}teams/index.html">{u["teams"]}</a></p></footer>
          <script defer src="{up}assets/theme.js"></script>
---
'''
