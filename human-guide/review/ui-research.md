# Readable technical workspace

The user chose **dark theme, compact panels**. This revision applies note-taking interface patterns to the existing offline guide. The chapter text, commands, prepared helpers, tool restrictions and Markdown handbook are preserved.

## Research translated into decisions

| Source | Relevant pattern | Applied here |
| --- | --- | --- |
| [Obsidian settings](https://obsidian.md/help/settings) | Readable line length and adjustable text size | Limit prose width; 16 px body/14 px code by default, with 18/20 px reading options |
| [Obsidian outline](https://obsidian.md/help/plugins/outline) | Navigate a note through its headings | Persistent desktop outline with current-section highlighting; collapsible outline on smaller screens |
| [Notion sidebar](https://www.notion.com/help/navigate-with-the-sidebar) | Grouped, collapsible sections and easily reached pages | Keep quick reference, setup and tool chooser visible; collapse secondary reference groups; opening a deep link reveals its group |
| [Notion page styling](https://www.notion.com/help/customize-and-style-your-content) | Page-level display controls and distinct content blocks | Quiet reading controls, compact task shortcuts and separate command-panel headers |
| [W3C contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum) | Normal text contrast at least 4.5:1 | Measure primary foreground/background pairs in both dark and light themes |
| [W3C reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow) | Reflow at 320 CSS px without page-wide two-direction scrolling | Test all 22 pages at 320 px; keep wide reference tables in their own keyboard-focusable scroll regions |
| [W3C text spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) | User spacing overrides must not lose content | Check enlarged text and line/paragraph/letter/word spacing on quick reference, setup and chooser |

These are design choices informed by the sources, not claims that one note-taking product proves the guide's usability. Only interface patterns were borrowed; no external product, cloud sync or AI integration is part of the reader.

## What changed

- Charcoal surfaces, restrained blue accents, stronger body text and fewer competing controls. The marketing banner was removed from the reading path.
- Compact, collapsible navigation preserves all seven competition categories and every reference page. Task shortcuts replace the quick sheet's wide navigation table.
- Setup paragraphs remain available behind a short disclosure. Page text itself is not shortened or removed. Print opens this disclosure before rendering.
- Commands get a language/line-count header, a copy control outside the scrollable code, and an expand control for longer scripts. Visual line wrapping does not insert characters into copied commands.
- Focus mode removes side panels. Theme and text size are remembered locally where storage is available; storage failure leaves working defaults.
- Mobile navigation has a dismissible backdrop and Escape behavior; a collapsing outline gives the main text priority.

## Verification

The jsdom suite first failed on the old light default, then passed after the workspace changes. It covers route navigation, focus/text controls, long-script expansion, print-state restoration, exact copied text, offline downloads, search and workbook filters.

The separate Chrome test uses the installed browser through a development-only Playwright dependency outside the guide package. [Chrome headless](https://developer.chrome.com/docs/automation-and-testing/headless) renders the actual local page. It checks all 22 routes at desktop/tablet/mobile widths, preserves every displayed code block's text, checks primary contrast pairs, exercises controls and rejects external HTTP requests. A baseline hash comparison proves all 28 guide/helper files selected before the UI work, including HANDBOOK.md, remain byte-for-byte unchanged.

See `ui-validation.json` for the browser version, current HTML hash, check results and measured contrast. The primary tested pairs exceed 4.5:1 in both themes. Three key pages are also checked at 20 px text and with W3C's spacing overrides at 320 px. Print checks confirm that setup details are visible and navigation is hidden on light paper.

Screenshots reviewed: [desktop workspace](ui/desktop-dark.png), [command view](ui/command-view.png), [mobile](ui/mobile-dark.png), [tool chooser](ui/tool-chooser.png). Additional development captures cover light theme, focus, mobile navigation and spacing overrides. Visual review checks hierarchy, spacing, clipping and control placement; it is not a recruited human study or a full WCAG certification. Clipboard contents are verified by the DOM suite's stub; OS clipboard integration and organizer machines are outside this UI test.

An independent code reviewer reproduced a mobile drawer/search issue and noticed that the printed task index was hidden. Both were fixed: displaying search results now closes the drawer and clears the inert state, and the task mappings print in a compact grid. Regression checks cover the mobile transition and printed index visibility. The final suites pass 11 DOM groups and 11 Chrome groups. The review did not reassess challenge-solution accuracy, organizer tools, screen-reader behavior or other browser engines.
