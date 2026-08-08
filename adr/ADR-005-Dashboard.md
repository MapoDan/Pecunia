# ADR-005 — Dashboard

**Status:** Accepted

## Decision
Dashboard data is aggregated server-side in configurable widgets. A default dashboard is provided for every new user and can be customized.

## Analytical principles
- compare ordinary and extraordinary expenses;
- use effective personal amount for personal spending;
- filter by period/category/merchant/payment method/tag/group;
- expose recurring behavior and saving opportunities;
- keep admin operational metrics separate from personal financial analytics.

## Rationale
Server-side aggregation reduces browser/NAS load and prevents the PWA from downloading the entire financial history.