---
version: alpha
name: Apple Clinical Planner
description: Apple-inspired glass, calm clinical precision, and spatial-planning clarity for an infectious-disease ward layout tool.
colors:
  primary: "#1D1D1F"
  secondary: "#6E6E73"
  tertiary: "#0071E3"
  accent: "#30D158"
  warning: "#FF9F0A"
  danger: "#FF453A"
  canvas: "#F5F5F7"
  surface: "#FFFFFF"
  surfaceGlass: "#FBFBFD"
  separator: "#D2D2D7"
  clinicalBlue: "#64D2FF"
  clinicalOrange: "#FFB340"
  clinicalYellow: "#FFD60A"
  clinicalGreen: "#32D74B"
  clinicalRed: "#FF6961"
typography:
  h1:
    fontFamily: -apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, sans-serif
    fontSize: 2.25rem
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.035em"
  h2:
    fontFamily: -apple-system, BlinkMacSystemFont, SF Pro Display, Segoe UI, sans-serif
    fontSize: 1.25rem
    fontWeight: 650
    lineHeight: 1.18
    letterSpacing: "-0.018em"
  body-md:
    fontFamily: -apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, sans-serif
    fontSize: 0.95rem
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: -apple-system, BlinkMacSystemFont, SF Pro Text, Segoe UI, sans-serif
    fontSize: 0.75rem
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: "0.01em"
rounded:
  sm: 10px
  md: 16px
  lg: 24px
  xl: 32px
spacing:
  xs: 6px
  sm: 10px
  md: 16px
  lg: 24px
  xl: 36px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "#005BB5"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12px
  surface-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 20px
  glass-card:
    backgroundColor: "{colors.surfaceGlass}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 20px
  canvas-stage:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xl}"
    padding: 24px
  separator-line:
    backgroundColor: "{colors.separator}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 6px
  success-badge:
    backgroundColor: "{colors.accent}"
    textColor: "#003B14"
    rounded: "{rounded.md}"
    padding: 10px
  warning-badge:
    backgroundColor: "{colors.warning}"
    textColor: "#3A2400"
    rounded: "{rounded.md}"
    padding: 10px
  danger-badge:
    backgroundColor: "{colors.danger}"
    textColor: "#2B0000"
    rounded: "{rounded.md}"
    padding: 10px
  module-patient:
    backgroundColor: "{colors.clinicalOrange}"
    textColor: "#3A2200"
    rounded: "{rounded.sm}"
    padding: 6px
  module-anteroom:
    backgroundColor: "{colors.clinicalYellow}"
    textColor: "#2E2500"
    rounded: "{rounded.sm}"
    padding: 6px
  module-wc:
    backgroundColor: "{colors.clinicalBlue}"
    textColor: "#00324A"
    rounded: "{rounded.sm}"
    padding: 6px
  module-clean:
    backgroundColor: "{colors.clinicalGreen}"
    textColor: "#003B12"
    rounded: "{rounded.sm}"
    padding: 6px
  module-soiled:
    backgroundColor: "{colors.clinicalRed}"
    textColor: "#3A0000"
    rounded: "{rounded.sm}"
    padding: 6px
---

## Overview

Apple Clinical Planner translates Apple-style product calm into a professional infectious-disease ward planning interface. The UI should feel quiet, precise, and premium: large whitespace, soft glass surfaces, rounded cards, subtle separators, and a single strong blue action color. Architectural content remains the hero; controls should recede until needed.

## Colors

- **Primary (#1D1D1F):** Apple-like near-black for titles and high-importance text.
- **Secondary (#6E6E73):** Muted system gray for helper copy, metrics, and explanatory text.
- **Tertiary (#0071E3):** Primary Apple blue for the main action path: generate, select, view in 3D.
- **Canvas (#F5F5F7):** Light Apple system background for the page and plan workspace.
- **Surface (#FFFFFF):** Cards, panels, and control groups.
- **SurfaceGlass (#FBFBFD):** Slightly translucent glass panels over the canvas background.
- Clinical module colors should stay legible but become softer and more system-like: blue for WC/water, orange for patient rooms, yellow for anterooms, green for nurse/clean support, red only for soiled/error states.

## Typography

Use the system font stack to approximate SF Pro on every platform. Titles are large, tight, and confident. Body text is compact but not cramped. Small labels use medium-to-bold weights, not uppercase shouting unless they are metrics or badges.

## Layout

The page uses a product-style hierarchy:

1. A compact hero header explains the tool and current planning goal.
2. Sidebar controls are grouped into rounded glass cards.
3. The main canvas lives inside a large white stage card with soft shadow and 24px radius.
4. Reports, alternatives, and 3D viewer are separate cards below the canvas, not gray debug boxes.
5. JSON output is secondary and should not visually dominate the planning workflow.

Whitespace is part of the style. Prefer 16/24/36px spacing rhythm. Avoid raw HTML default margins, hard black borders, and dense debugging UI.

## Elevation & Depth

Use low, soft shadows only:

- Cards: `0 18px 60px rgba(0,0,0,0.08)`
- Small controls: `0 1px 2px rgba(0,0,0,0.06)`
- Canvas: subtle inset/separator line with rounded corners

No heavy drop shadows or skeuomorphic panels.

## Shapes

- Main cards: 24px radius
- Buttons: 999px pill radius or 16px rounded rectangles
- Swatches: 999px round chips
- Canvas and 3D viewer: 20px radius

## Components

- **Primary button:** Apple blue pill, white text, used for Generate and View in 3D.
- **Secondary button:** White/glass button with light separator, used for utility actions.
- **Panel card:** White surface, rounded 24px, soft shadow, compact label/title area.
- **Metric/status text:** Use secondary gray, compact line height, and bold only for numeric emphasis.
- **Legend chip:** rounded chip with a color dot and label; avoid raw inline text lists.

## Do's and Don'ts

Do:

- Make the plan/3D canvas feel like a designed workspace, not a debug iframe.
- Keep controls quiet and grouped.
- Preserve architectural legibility over pure decoration.
- Use blue sparingly for action and focus.

Don't:

- Use black 1px borders around every object.
- Let text areas and debug reports dominate the first screen.
- Use many saturated colors at full strength outside the architectural module map.
- Flatten the 3D equipment into labels; distinguish objects by geometry and silhouette first.
