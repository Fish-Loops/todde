# Todde Design Language Constitution

## Core Principles

### I. Cohesive Visual Identity
Every surface reflects the Todde brand palette, typographic scale, and spacing rhythm. Colors, fonts, and elevation tokens are reused—not redefined—so that users can build familiarity as they move across the site.

### II. Component-Driven Experience
Interfaces are composed from the shared component library. New UI elements extend or adapt existing patterns before introducing bespoke solutions, ensuring interaction affordances feel predictable everywhere.

### III. Accessible & Responsive by Default
Each component meets WCAG 2.2 AA contrast, keyboard, and screen-reader expectations and gracefully adapts from mobile to widescreen layouts. No release ships without verifying accessibility across the supported breakpoints.

### IV. Consistent Voice & Content Hierarchy
Headings, body copy, and microcopy follow the same tone, capitalization, and hierarchy rules. Layouts highlight primary actions consistently, reinforcing user trust and reducing cognitive load.

### V. Governed Evolution
Design tokens, components, and documentation change through a transparent proposal workflow. Versioned artifacts and changelogs keep engineering, design, and content teams synchronized.

## Design Language Standards

- **Color System**: Primary (`#1F4B99`), secondary (`#F2A900`), neutral grayscale, and success/error palettes live in the design tokens (`tokens/design.json`). Updates require regression checks against contrast ratios and affected components.
- **Typography**: Use the `Inter` font family. Semantic HTML tags map to predefined token sizes (`--font-h1` through `--font-caption`). Weight changes outside the scale must be approved during design review.
- **Spacing & Layout**: Apply the 4px spacing scale (`4 · n`). Grid breakpoints: 0–599px (mobile), 600–1023px (tablet), 1024px+ (desktop). Components expose layout props rather than inline spacing overrides.
- **Iconography & Illustration**: Leverage the shared SVG set located in `static/icons`. Custom icons adopt the same stroke width, corner radius, and grid. Illustrations adhere to the three-tone palette plus neutrals.
- **Motion**: Animations use the easing presets defined in `--ease-standard` and `--ease-emphasized`. Duration options are 100ms, 200ms, 300ms, and 500ms. Motion must reinforce hierarchy and stay within accessibility guidelines (reduced motion support included).

## Delivery Workflow & Quality Gates

1. **Discovery**: Any design change begins with a Figma exploration linked to the associated ticket. Define the target component(s) and tokens impacted.
2. **Implementation Plan**: Engineers outline updates to shared styles, React/Django templates, or CSS modules. Plans include accessibility checks and responsive behaviour notes.
3. **Build & Review**: Pull requests must include before/after screenshots (mobile + desktop), Storybook/preview links when available, and confirmation that automated visual regression and unit tests pass.
4. **Validation**: Run linting, unit tests, and axe-core scans. Reviewers verify adherence to the constitution before approving merges.
5. **Documentation**: Update `docs/design-system.md` and component READMEs with usage guidance, examples, and any migration steps.

## Governance

- This constitution supersedes ad-hoc design decisions. Exceptions require a written RFC documenting rationale, impact, and rollback.
- Amendments follow the proposal workflow: draft → design council review → engineering sign-off → documentation update → version release.
- Compliance is checked during design handoff, code review, and QA. Non-compliant work is blocked until brought into alignment.
- Repository hygiene keeps operational directories private. The `.specify`, `.vscode`, and `.github` folders are workspace-scoped and must stay untracked in the public git history. Collaborators maintain local copies and document relevant guidance instead of committing these directories.

**Version**: 1.0.1 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-12