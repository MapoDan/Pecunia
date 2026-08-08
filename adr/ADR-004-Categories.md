# ADR-004 — Categories and Suggestions

**Status:** Accepted

## Decision
Use hierarchical category/subcategory classification with lightweight automatic suggestions.

## Rationale
The user must not manually enter the same classification repeatedly. Suggestions should derive primarily from merchant history and, where available, PSD2 causal/payment description.

## Rules
Suggestions are defaults, not silent decisions. The user can override them. Only the administrator can manage global tags according to group rules; personal tags may become global when promoted.