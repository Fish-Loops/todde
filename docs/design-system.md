# Todde Design System Overview

This document distills the design language defined in the Todde Design Language Constitution into actionable guidance for designers and engineers.

## Design Tokens

| Token Group | Location | Notes |
|-------------|----------|-------|
| Colors | `tokens/design.json` | Primary `#1F4B99`, Secondary `#F2A900`, neutrals `#0C1320`–`#F7F9FC`, success `#0F9D58`, error `#C62828` |
| Typography | `tokens/design.json` | Scale: `--font-h1` 48px/56px, `--font-h2` 36px/44px, `--font-h3` 28px/36px, `--font-body` 16px/24px, `--font-caption` 12px/18px |
| Spacing | `tokens/design.json` | Unit = 4px. Use tokens `--space-1` (4px) through `--space-8` (32px) |
| Motion | `tokens/design.json` | Easing presets `--ease-standard` cubic-bezier(0.2, 0, 0, 1), `--ease-emphasized` cubic-bezier(0.4, 0, 0.2, 1) |

> **Maintenance**: Token updates require a changelog entry and contrast/accessibility validation before merging.

## Component Standards

- **Base Components**: Buttons, inputs, cards, banners, and modals exist in the shared component library. Extend rather than fork them.
- **States**: Implement hover, focus-visible, active, disabled, and error states. Ensure focus outlines meet 3:1 contrast.
- **Responsiveness**: Components expose responsive props for breakpoint overrides (`mobile`, `tablet`, `desktop`). Avoid hard-coded pixel widths.
- **Localization**: Reserve space for strings expanding up to 30% without breaking layouts.

## Content & Voice

- Headings use sentence case. Avoid marketing slang and prefer concise, action-oriented language.
- Primary actions use imperative verbs (e.g., “Save changes”). Secondary actions use neutral phrasing (“Cancel”).
- Microcopy should clarify purpose in ≤ 80 characters and support accessibility hints.

## Accessibility Checklist

1. Validate text/background contrast with automated tooling.
2. Confirm tab order and focus states align with visual hierarchy.
3. Provide `aria-live` regions for asynchronous feedback.
4. Respect system reduced-motion preferences for subtle animations.
5. Test with screen readers (VoiceOver on macOS, NVDA on Windows) for critical flows.

## Release Workflow

1. Propose updates via a Design Language RFC referencing the affected tokens/components.
2. Sync with design counterparts to review Figma artifacts and usage examples.
3. Implement changes behind a feature flag when risk is high; capture screenshots pre/post in mobile and desktop.
4. Run automated tests (unit, integration, visual regression) and axe-core scans.
5. Update this document within the same pull request to reflect new patterns or tokens.

---

_Last reviewed: 2025-10-11_
