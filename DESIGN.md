---
version: alpha
name: Luis Fernando Barrera
description: Personal CV and professional identity — technical sophistication meets human warmth. A software engineering manager and AI-augmented developer whose work bridges fintech, open source, and contemplative depth.
colors:
  primary: "#0F172A"
  primary-soft: "#1E293B"
  secondary: "#475569"
  muted: "#94A3B8"
  tertiary: "#C14E3C"
  tertiary-soft: "#E07A5F"
  accent: "#3B82F6"
  accent-soft: "#60A5FA"
  canvas: "#F8FAFC"
  canvas-alt: "#F1F5F9"
  surface: "#FFFFFF"
  hairline: "#E2E8F0"
  ink: "#0F172A"
  ink-secondary: "#475569"
  ink-muted: "#94A3B8"
  on-primary: "#FFFFFF"
  on-tertiary: "#FFFFFF"
  success: "#10B981"
  warning: "#F59E0B"
  # Dark mode overrides
  dark-canvas: "#0B1120"
  dark-surface: "#131C31"
  dark-hairline: "#1E293B"
  dark-ink: "#E2E8F0"
  dark-ink-secondary: "#94A3B8"
typography:
  display-xl:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 2.5rem
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  display-lg:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 1.75rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  heading-md:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  heading-sm:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 1rem
    fontWeight: 600
    lineHeight: 1.4
  body-lg:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.7
  body-md:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.6
  label-sm:
    fontFamily: "'IBM Plex Sans', system-ui, -apple-system, sans-serif"
    fontSize: 0.75rem
    fontWeight: 600
    letterSpacing: "0.05em"
    textTransform: uppercase
  print-body:
    fontFamily: "Merriweather, Georgia, Times New Roman, serif"
    fontSize: 0.833rem
    lineHeight: 1.5
  print-title:
    fontFamily: "Raleway, Helvetica, Arial, sans-serif"
    fontWeight: 300
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 64px
components:
  section-title:
    typography: "{typography.display-lg}"
    textColor: "{colors.primary}"
  job-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  job-position:
    typography: "{typography.body-md}"
    textColor: "{colors.tertiary}"
  job-date:
    typography: "{typography.label-sm}"
    textColor: "{colors.ink-muted}"
  job-summary:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.body-md}"
  highlight-bullet:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.body-md}"
  skill-tag:
    backgroundColor: "{colors.canvas-alt}"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
    padding: "4px 12px"
    typography: "{typography.body-md}"
  skill-tag-hover:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
  sidebar-section:
    backgroundColor: "{colors.canvas-alt}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  profile-image:
    rounded: "{rounded.full}"
    size: 120px
  contact-link:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.body-md}"
  dark-toggle:
    backgroundColor: "{colors.canvas-alt}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
  dark-toggle-active:
    backgroundColor: "{colors.dark-surface}"
    textColor: "{colors.dark-ink}"
---
## Overview

The Luis Fernando Barrera CV design system balances **technical sophistication** with **human warmth**. The palette draws from two sources: the deep, trusted navies of financial services (primary/ink) and the warm terracotta of Mexican craft and the Dante Valentino painting that anchors the informind identity. IBM Plex Sans provides clean, readable body text — modern without being trendy. The layout prioritizes scanability: a clear sidebar for identity/contact, a main column for narrative career progression, and generous whitespace to let achievements breathe.

The design exists in two modes — **screen** (dark/light toggle) and **print** (serif-optimized for PDF). Both share the same hierarchy but adapt medium-appropriate typography.

## Colors

- **Primary (#0F172A):** Deep ink for name, section titles, high-emphasis text. Evokes stability, trust, depth.
- **Tertiary (#C14E3C):** Terracotta accent — the sole driver for interaction and visual emphasis. Links, job positions, section underlines. Warm without being soft.
- **Accent (#3B82F6):** Reserved for external links and code references. A cool counterpoint to the warm terracotta.
- **Canvas (#F8FAFC):** Off-white page background. Reduces glare vs pure white.
- **Surface (#FFFFFF):** Card and content backgrounds.
- **Hairline (#E2E8F0):** Subtle dividers and borders.
- **Dark mode:** Inverts canvas→dark-canvas (#0B1120), surface→dark-surface (#131C31), ink→dark-ink (#E2E8F0).

### Dark mode

The dark palette is not a simple inversion. Canvas becomes a deep midnight blue (not pure black) to reduce eye strain. Cards lift subtly from the background via surface tint. Terracotta shifts warmer to maintain contrast against the dark backdrop.

```yaml
dark-canvas:  "#0B1120"
dark-surface: "#131C31"
dark-hairline: "#1E293B"
dark-ink:     "#E2E8F0"
```

## Typography

**IBM Plex Sans** for everything on screen. Single-family hierarchy keeps the page cohesive. Weight and size carry hierarchy, not font switches.

- **Display XL (2.5rem / 600):** Name at top of CV. Tight letter-spacing for presence.
- **Display LG (1.75rem / 600):** Section titles (Experience, Skills, Projects).
- **Heading MD (1.25rem / 600):** Company names in job cards.
- **Body LG (1rem / 400, 1.7 line-height):** About paragraphs and summaries.
- **Body MD (0.875rem / 400, 1.6 line-height):** Highlight bullets and skill tags.
- **Label SM (0.75rem / 600):** Date ranges, metadata. Uppercase with tracking.

**Print:** Merriweather for body (readable serif at 10pt), Raleway (light 300) for header titles. The print layout relaxes into a more traditional resume feel.

## Layout

The CV uses a **two-column layout** on wide screens, collapsing to single-column on mobile:

- **Sidebar (narrow, sticky):** Photo, name, label, contact info, language badges, skills tags.
- **Main (wide, scrollable):** About, Experience (job cards in timeline), Projects, Education, Volunteer.

On print and narrow screens, the sidebar collapses to a header band.

### Spacing scale

4px baseline. Section breaks use 64px (`section`) for clear visual separation. Job cards within a section are separated by 24px (`lg`). Intra-card spacing uses 16px (`md`).

## Components

### Job Card

The primary content unit. White surface with subtle shadow. Contains:
- Company name (heading-md, primary ink)
- Position (body-md, terracotta, 600 weight)
- Date range (label-sm, muted)
- Summary paragraph
- Bulleted highlights

On hover, shadow deepens to indicate interactivity.

### Skill Tags

Pill-shaped badges. Default: light gray background, primary ink text. Hover: terracotta background, white text. Used in the Skills section and sidebar.

### Section Titles

Display-lg weight, primary ink. Underlined with a 2px terracotta rule for visual anchoring as the user scrolls.

### Dark Mode Toggle

A pill button in the top-right corner. Default matches the canvas background. Active state shifts to dark-surface. Smooth transition between modes.

### Print Mode

- Serif body (Merriweather) for readability on paper
- Raleway for header titles (elegant, light weight)
- No shadows or cards — clean linear flow
- Section separators become simple hairline rules
- Two-column sidebar becomes full-width header

## Do's and Don'ts

- **Do** use token references (`{colors.tertiary}`) instead of literal hex values in component definitions.
- **Do** respect the two-mode system: screen (sans-serif, shadows, cards) vs print (serif, linear, no shadows).
- **Don't** introduce additional accent colors. The warm terracotta + cool blue pair is the entire palette beyond neutrals.
- **Don't** use pure black (`#000000`) anywhere — the darkest color is `#0F172A` (primary).
- **Don't** use drop shadows on print output.
- **Do** keep job cards at consistent height within a section; align company names and date ranges.
- **Don't** exceed 3 levels of heading depth in any section.