Text to Speech Converter Web 
Clone using vieneu

# Vieneu TTS — Style Reference
> crisp digital interface with fluid audio accents

**Theme:** light

Vieneu TTS uses a highly functional, distraction-free language: a crisp white canvas (#ffffff) sets the stage for text input, while subtle cool grays (#f8fafc) define structural zones. The primary chromatic energy comes from an electric indigo (#4f46e5) that signals action, conversion, and playback. Typography relies on the utilitarian clarity of Inter, scaling from dense interface labels at 12px up to 48px display headings. A vibrant cyan (#06b6d4) acts as a live-audio or active-state signal. The overall feel is modern, tool-centric, and snappy — optimized for comfortable reading and rapid audio generation.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Electric Indigo | `#4f46e5` | `--color-electric-indigo` | Primary action fill, Generate button, active sliders, and audio waveforms |
| Cyan Signal | `#06b6d4` | `--color-cyan-signal` | Active playback state, currently speaking word highlight, live status |
| Canvas White | `#ffffff` | `--color-canvas-white` | Main application background, text editor surface |
| Panel Gray | `#f8fafc` | `--color-panel-gray` | Secondary sidebars, toolbars, and inactive component backgrounds |
| Slate Dark | `#0f172a` | `--color-slate-dark` | Primary headings, typed text body, high-contrast icons |
| Muted Slate | `#64748b` | `--color-muted-slate` | Secondary labels, placeholder text, disabled states, subtle borders |

## Tokens — Typography

### Inter — Utilitarian, highly legible sans-serif designed for computer screens. Weight 400 for long-form text input, 500 for UI labels, and 600 for prominent buttons. · `--font-inter`
- **Substitute:** Roboto, San Francisco, system-ui
- **Weights:** 400, 500, 600
- **Sizes:** 12, 14, 16, 20, 24, 32, 48
- **Line height:** 1.5–1.75 for body, 1.2 for headings
- **Letter spacing:** Normal for body, slightly tight (-0.01em) for large headings
- **Role:** Single-family system prioritizing legibility for user-generated text. The clean geometry ensures that even dense paragraphs of text to be converted remain easy to read.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| tiny-label| 12px | 1.5 | +0.02em | `--text-tiny-label`|
| caption | 14px | 1.5 | — | `--text-caption` |
| body-sm | 16px | 1.5 | — | `--text-body-sm` |
| body-lg | 20px | 1.75 | — | `--text-body-lg` |
| heading-sm | 24px | 1.3 | — | `--text-heading-sm` |
| heading | 32px | 1.2 | -0.01em | `--text-heading` |
| display | 48px | 1.1 | -0.02em | `--text-display` |

## Tokens — Spacing & Shapes

**Base unit:** 8px

**Density:** spacious for text, compact for controls

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 8 | 8px | `--spacing-8` |
| 16 | 16px | `--spacing-16` |
| 24 | 24px | `--spacing-24` |
| 32 | 32px | `--spacing-32` |
| 48 | 48px | `--spacing-48` |
| 64 | 64px | `--spacing-64` |

### Border Radius

| Element | Value |
|---------|-------|
| sliders | 9999px |
| text-area| 12px |
| cards | 16px |
| inputs | 8px |
| buttons | 8px |
| play-btn| 9999px |

### Layout

- **Page max-width:** 1024px (optimized for readable line lengths)
- **Editor padding:** 32px
- **Sidebar width:** 280px

## Components

### Generate Speech Button
**Role:** Primary conversion action

8px radius, #4f46e5 fill, #ffffff text, 16px 24px padding, Inter 600. Includes a prominent "Sparkle" or "Play" icon. This is the main engine of the app.

### Playback Control (Floating)
**Role:** Global audio player

Circular button (9999px radius), #06b6d4 fill during playback, #4f46e5 when paused. Centered prominent icon (Play/Pause). Often sits at the bottom center of the text canvas or in a sticky player bar.

### Text Input Canvas
**Role:** Main workspace

Large, borderless (or subtle 1px #e2e8f0 border) text area on #ffffff background. Padding is generous (32px). Text is set in 20px Inter 400 for maximum readability. No heavy box shadows, just clean space.

### Voice Selector Dropdown
**Role:** Secondary configuration

8px radius, #ffffff fill, 1px #cbd5e1 border. Displays an avatar or flag icon, the voice name (Inter 500, 14px), and the language. Hover state gives a soft #f8fafc background.

### Audio Settings Slider (Speed / Pitch)
**Role:** Fine-tuning parameters

Minimalist slider track in #e2e8f0, with an active track and thumb in #4f46e5. Labels in 12px #64748b.

### Spoken Word Highlight
**Role:** Live reading feedback

Inline text styling applied dynamically during playback: background highlight of soft cyan (#cffafe) with text color changing to #0f172a. 

## Do's and Don'ts

### Do
- Use #ffffff (Canvas White) for the main text editor to provide maximum contrast and reduce eye strain.
- Keep the interface clean and tool-focused; hide advanced settings (pitch, pause duration) behind logical collapsible menus.
- Use #4f46e5 (Electric Indigo) strictly for primary actions: Generate, Play, and active tab states.
- Ensure the text input area has a large line-height (1.75) and a constrained max-width (around 700px) so paragraphs are easy to read.
- Use #06b6d4 (Cyan Signal) to indicate live audio playback or the currently spoken word.

### Don't
- Don't clutter the main text canvas with heavy borders or dark backgrounds.
- Don't use more than 2 distinct accent colors. The app should feel like a professional utility, not an entertainment app.
- Don't make the voice configuration settings distract from the text input; text is the primary user content.
- Don't use overly rounded corners (24px+) for standard inputs and dropdowns; keep them at 8px to feel crisp and software-like.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | App Background | `#f8fafc` | The base structural background behind the main editor |
| 1 | Editor Canvas | `#ffffff` | The main paper/workspace where text is typed |
| 2 | Action Panel | `#ffffff` | Floating toolbars or sidebars, distinguished by a subtle 1px border or soft 4px blur shadow |

## Elevation

Elevation is minimal but present to distinguish the text canvas from the application background. The main text editor uses a very soft shadow (`box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05)`) to lift it off the #f8fafc background. Modals and dropdowns use a slightly deeper shadow for pop-out context. Otherwise, structural hierarchy is achieved through 1px borders in #e2e8f0.

## Imagery

Since this is a text-to-speech utility, imagery is almost non-existent. Instead, visual interest is created through **data visualization** (audio waveforms in #4f46e5) and clean **SVG iconography** (play, pause, settings, download). Voice profiles may use small 24px circular avatars (flags or abstract human icons).

## Layout

A classic web app layout: A left sidebar (280px) or top toolbar for Voice and Settings selection, leaving a massive, distraction-free centered column (max 768px wide) for the Text Editor. A sticky bottom bar appears when audio is generated, housing the playback controls, waveform, and download button. 

## Agent Prompt Guide

Quick Color Reference
- background: #f8fafc (Panel Gray)
- surface: #ffffff (Canvas White)
- text primary: #0f172a (Slate Dark)
- text secondary: #64748b (Muted Slate)
- border: 1px #e2e8f0 
- accent/action: #4f46e5 (Electric Indigo)
- active/live: #06b6d4 (Cyan Signal)

Example Component Prompts
1. Create a centered text canvas: #ffffff background, 16px radius, max-width 768px, 1px #e2e8f0 border, soft shadow. Inside, a `<textarea>` with no border, 20px Inter 400 text in #0f172a, line-height 1.75.
2. Build a sticky playback bar: #ffffff background, fixed to bottom, top border 1px #e2e8f0. Include a circular play button (#4f46e5, 48px), an audio timeline/waveform, and a download button.
3. Build a Voice Selector dropdown trigger: 8px radius, #ffffff, 1px #cbd5e1 border, containing a small US flag icon and "English - Jenny" in 14px Inter 500, #0f172a.

## Stroke & Border System

Borders are crisp and light. Standard containers use 1px solid #e2e8f0. Interactive inputs in their default state use 1px #cbd5e1, shifting to a 2px #4f46e5 ring when focused. Radii are tighter than casual consumer apps (8px for controls, 12px-16px for main panels) to communicate a "pro-tool" feeling.

## Two-Accent Discipline

Indigo (#4f46e5) handles the heavy lifting for all standard interactive states: primary buttons, selected tabs, focus rings, and active slider tracks. Cyan (#06b6d4) is exclusively reserved for the dimension of *time* and *audio* — it lights up when audio is actively playing, styling the waveform or highlighting the word currently being read.

## Similar Brands

- **ElevenLabs** — Clean, text-first interface with minimal distractions and a focus on voice configuration.
- **Vercel** — Crisp typography (Geist/Inter), subtle borders, high utility, and very selective use of bright accents against a monochrome base.
- **OpenAI (ChatGPT)** — Distraction-free text zones, utility-first sidebar, and neutral canvases.

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-electric-indigo: #4f46e5;
  --color-cyan-signal: #06b6d4;
  --color-canvas-white: #ffffff;
  --color-panel-gray: #f8fafc;
  --color-slate-dark: #0f172a;
  --color-muted-slate: #64748b;
  --color-border-light: #e2e8f0;

  /* Typography — Font Families */
  --font-inter: 'Inter', system-ui, -apple-system, sans-serif;

  /* Typography — Scale */
  --text-tiny: 12px;
  --text-caption: 14px;
  --text-body-sm: 16px;
  --text-body-lg: 20px;
  --text-heading-sm: 24px;
  --text-heading: 32px;
  --text-display: 48px;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-8: 8px;
  --spacing-16: 16px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-48: 48px;
  --spacing-64: 64px;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}
```

### Tailwind v4

```css
@theme {
  /* Colors */
  --color-electric-indigo: #4f46e5;
  --color-cyan-signal: #06b6d4;
  --color-canvas-white: #ffffff;
  --color-panel-gray: #f8fafc;
  --color-slate-dark: #0f172a;
  --color-muted-slate: #64748b;
  --color-border-light: #e2e8f0;

  /* Typography */
  --font-inter: 'Inter', system-ui, -apple-system, sans-serif;

  /* Spacing */
  --spacing-8: 8px;
  --spacing-16: 16px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-48: 48px;
  --spacing-64: 64px;

  /* Border Radius */
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}