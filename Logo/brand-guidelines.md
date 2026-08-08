# Pecunia — Brand & UI Color Guidelines

This document defines the official visual color system for Pecunia. The colors are semantic design tokens and must be used consistently throughout the PWA frontend, dashboards, charts, forms, notifications, buttons, cards, tables, empty states, status indicators and icons.

Developers must not introduce arbitrary colors when an existing semantic token is available.

## Assets

- `logo.png` — full application logo, to be supplied/finalized.
- `icon.png` — application icon, to be supplied/finalized.

## Core color palette

| Token | Hex | Semantic meaning |
|---|---|---|
| `primary` | `#10B981` | Primary brand color / Emerald |
| `primary-dark` | `#047857` | Dark primary variant |
| `background` | `#F8FAFC` | Main application background |
| `surface` | `#FFFFFF` | Cards, panels, modals and elevated surfaces |
| `text-primary` | `#0F172A` | Main text |
| `text-secondary` | `#64748B` | Secondary text, metadata and supporting information |
| `expense` | `#F43F5E` | Expenses / negative financial values |
| `income` | `#10B981` | Reserved for future income tracking |
| `warning` | `#F59E0B` | Warnings / attention required |
| `error` | `#EF4444` | Errors / failed operations |

## Financial semantics

### Expense

`#F43F5E` is used for expense amounts, negative financial variations, expense-related chart series, expense indicators and expense trends. It must not be used to indicate generic errors.

### Income — reserved for V2

`#10B981` is reserved for future income tracking. Pecunia V1 does not track income, so no income-related UI should be introduced in V1.

## Status semantics

### Warning / Attention

`#F59E0B` is used for pending actions, PSD2 transactions requiring user attention, warnings, incomplete classification, non-blocking issues and notification indicators.

### Error

`#EF4444` is used for failed operations, validation errors, authentication errors, API errors, unrecoverable processing failures and destructive error states.

Warning and error must not be used interchangeably.

## Primary colors

### Primary

`#10B981` is used for primary actions, main CTA buttons, selected controls, active navigation states, links where appropriate, positive confirmations, selected filters and primary interactive elements.

### Primary Dark

`#047857` is used for hover states, pressed states, stronger emphasis, dark variants of primary components and text/icons when the primary color does not provide sufficient contrast.

## Neutral colors

### Background

`#F8FAFC` is the default application background. The main application canvas should generally use this color rather than pure white.

### Surface

`#FFFFFF` is used for cards, panels, modals, dropdowns, tables, forms and elevated UI elements.

### Primary Text

`#0F172A` is used for headings, primary labels, expense descriptions, merchant names and important numerical values.

### Secondary Text

`#64748B` is used for supporting information, timestamps, metadata, secondary labels, descriptions and less important numerical information.

## Accessibility

Color must not be the sole mechanism used to communicate information. Expenses, warnings and errors must also use appropriate combinations of iconography, labels, text, shape, position and status indicators.

The implementation must respect WCAG accessibility requirements for text and interactive elements. Whenever a color is used as text, sufficient contrast against its background must be verified.

## Dark mode

Dark mode is not part of the mandatory V1 visual specification. Do not invent a dark-mode palette. If dark mode is introduced in a future phase, create a dedicated design decision and define semantic tokens rather than simply inverting the existing colors.

## Charts

Charts must use the semantic palette consistently. Do not assign arbitrary colors to financial categories.

Recommended semantic usage:

- Expenses → `#F43F5E`
- Positive/primary indicators → `#10B981`
- Warnings → `#F59E0B`
- Errors → `#EF4444`
- Neutral/reference data → appropriate neutral colors derived from the design system

When multiple categories need to be displayed simultaneously, use a dedicated chart palette derived from the Pecunia brand rather than unrelated colors. The chart palette must remain visually coherent with the main brand.

## PSD2 UI

PSD2 transactions requiring user action should use the warning/attention semantic `#F59E0B`. The interface must clearly communicate that the transaction is detected, not yet registered as an expense and waiting for a user decision.

Once accepted, the transaction should adopt normal expense semantics. Ignored transactions should not be displayed as active expenses.

## Semantic design tokens

The frontend should reference semantic tokens rather than hardcoding hexadecimal values throughout components.

Conceptual tokens include:

- `--color-primary`
- `--color-primary-dark`
- `--color-background`
- `--color-surface`
- `--color-text-primary`
- `--color-text-secondary`
- `--color-expense`
- `--color-income`
- `--color-warning`
- `--color-error`

The implementation technology may differ, but the semantic separation must be maintained.

## Usage guidance

The final visual system should also define:

- primary logo;
- app icon;
- light/dark usage;
- minimum clear space;
- typography;
- favicon/PWA icon variants;
- accessibility requirements.

The functional/UI specifications must not hard-code a different visual identity from the palette defined here.

## Brand principle

Pecunia should communicate financial control, clarity, trust, modernity, simplicity and calmness.

The Emerald primary color should remain the dominant brand accent. Avoid excessive use of saturated colors. Color should communicate meaning, not decoration.
