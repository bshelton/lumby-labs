---
name: Lumby Labs
description: A simple, readable home for RuneLite plugin guides.
colors:
  paper: "#faf9f5"
  ink: "#25382f"
  muted: "#58645e"
  green: "#275844"
  soft: "#edf1e9"
  line: "#d8ddd4"
  white: "#fff"
  gold: "#b78a36"
  green-hover: "#1e4635"
typography:
  display:
    fontFamily: 'Georgia, "Times New Roman", serif'
    fontSize: "58px"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-.035em"
  headline:
    fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "38px"
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: "-.03em"
  title:
    fontSize: "23px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-.02em"
  body:
    fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  lead:
    fontSize: "19px"
    lineHeight: 1.7
  label:
    fontSize: "14px"
    fontWeight: 600
rounded:
  code: "3px"
  navigation: "4px"
  button: "5px"
  note: "6px"
spacing:
  inline: "12px"
  compact: "16px"
  paragraph: "20px"
  group: "24px"
  gutter: "32px"
components:
  button-primary:
    backgroundColor: "{colors.green}"
    textColor: "{colors.white}"
    rounded: "{rounded.button}"
    padding: "10px 18px"
  button-primary-hover:
    backgroundColor: "{colors.green-hover}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.green}"
    rounded: "{rounded.button}"
    padding: "10px 18px"
  button-secondary-hover:
    backgroundColor: "{colors.soft}"
  documentation-navigation:
    textColor: "{colors.muted}"
    rounded: "{rounded.navigation}"
    padding: "8px 12px"
  documentation-navigation-current:
    backgroundColor: "{colors.soft}"
    textColor: "{colors.green}"
  note:
    backgroundColor: "{colors.soft}"
    rounded: "{rounded.note}"
    padding: "20px 24px"
---

# Design System: Lumby Labs

## Overview

**Creative North Star: "Read mode"**

Lumby Labs uses a quiet documentation style: warm paper, forest-green links, generous reading space, and a small outlined LL mark. The serif homepage headline adds character; guides use system typography for direct, comfortable reading.

This document records the implemented system in `assets/site.css` and `build.py`. The palette and LL treatment are implementation choices, not a separately approved permanent brand identity.

**Key Characteristics:**
- Cream canvas and restrained forest-green accents.
- Flat, rule-separated sections with clear reading hierarchy.
- Persistent desktop guide navigation and a compact mobile disclosure.

## Colors

### Primary

Forest green (`green`) identifies links, primary actions, current navigation, and the LL outline. The darker `green-hover` is the filled action hover state.

### Neutral

Warm paper (`paper`) is the page background. Deep green-gray (`ink`) carries headings and body text; `muted` carries supporting text. Pale sage (`soft`) distinguishes notes, code, table headers, and selected guide links. `line` separates sections without heavy frames. White (`white`) supplies primary-action text.

### Interaction accent

Muted gold (`gold`) is the keyboard focus outline. It is not a second marketing accent. Selection uses the stylesheet's local pale-green background and dark-green text.

## Typography

The homepage display uses Georgia with Times New Roman and serif fallbacks. Body copy and guide headings use the native system stack. The LL monogram and accounting formula also use Georgia.

Guide headings follow the frontmatter headline and title roles. Third-level guide headings are 17px. The homepage plugin name is 26px, with a 1.25 line height and slightly tightened tracking. Body paragraphs and lists cap at 70ch; lead paragraphs use the larger lead role and muted color. Small captions and footer text are 13px; availability labels are 12px and semibold.

## Layout

The shared wrapper is centered with a 1160px maximum width and 32px horizontal padding, including padding within its border-box width. The desktop header is at least 94px tall. The hero has 74px top and 58px bottom padding, a 780px content limit, and a 620px paragraph limit.

The plugin entry pairs a flexible description with a 300px facts column and a 60px gap. Documentation pairs a 220px sticky sidebar with flexible content and a 64px gap. The sidebar sticks 24px from the top. Articles cap at 760px. Paragraph spacing is 20px; guide section headings begin with 40px top spacing.

At widths up to 900px, the plugin facts column becomes 230px with a 30px gap, the documentation sidebar becomes 180px with a 32px gap, and the hero headline becomes 48px.

At widths up to 640px, wrapper gutters become 20px. Header navigation wraps below the brand; the header minimum height becomes 108px. Plugin entries and documentation become single-column. The desktop sidebar is hidden and a native details disclosure labeled “In this guide” appears above the article. The hero headline becomes 39px, guide title 31px, lead text 17px, guide section headings 22px, and formula 22px. Notes use 16px padding. Footer and help content stack; previous/next links can wrap. Tables scroll horizontally within their wrapper; images remain fluid.

## Elevation & Depth

There are no box shadows. Pale surfaces and thin divider rules provide grouping. Nothing floats above the document except the keyboard-visible skip link. Smooth anchor scrolling is disabled when reduced motion is requested; component state changes have no animated transitions.

## Shapes

The LL mark is a square 38px outlined frame with centered serif initials. Section rules and table separators are 1px. Rounding is small and functional: inline code, guide navigation, buttons and figures, then notes follow the frontmatter radii. No pill-shaped containers are used.

## Components

- **Actions:** Filled forest-green links and outlined secondary links share a minimum 44px height, 14px text, and weight 650. Action groups wrap with 20px gaps. Hover darkens the filled variant or adds a pale background to the secondary variant.
- **Navigation:** The header uses 14px semibold links. Current and hovered links gain green text and an underline. Guide navigation uses full-row links; the current page has a pale background and weight 650. Mobile guide navigation uses native details/summary semantics.
- **Notes:** Pale sage panels with a thin divider-colored border and restrained corners highlight limitations within the reading flow. The final paragraph has no bottom margin.
- **Plugin entries:** Open rows separated by rules, with a 48px pixel-rendered plugin icon, title, availability text, description, actions, and a definition list of facts. They are not elevated cards.
- **Tables:** Left-aligned, 14px text, pale header cells, and bottom rules. Cells use 13px vertical and 12px horizontal padding. Overflow stays inside the table wrapper.
- **Troubleshooting disclosures:** Native details with bottom rules, 14px vertical padding, and semibold summaries. Open summaries turn green.
- **Keyboard interaction:** Links and summaries receive a 3px gold focus outline with a 5px offset. The skip link becomes visible on focus. Preserve semantic landmarks and current-page attributes.

There are no input fields, forms, dialogs, or chips in the implemented website; support actions link to the relevant GitHub issue tracker.

## Do's and Don'ts

- Do preserve the readable article measure and mobile guide disclosure.
- Do use thin rules and pale surfaces for grouping.
- Do preserve visible keyboard focus and reduced-motion scrolling behavior.
- Do keep the LL mark small and the plugin artwork pixel-rendered.
- Don't turn documentation into a grid of elevated cards.
- Don't introduce oversized rounded containers or ornamental shadows into this system.
- Don't treat the current palette or LL mark as a separately approved permanent identity.
