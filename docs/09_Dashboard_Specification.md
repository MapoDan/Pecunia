# Pecunia — Dashboard Specification

## Objective
Allow the user to understand where money is going, identify recurring behaviors and find realistic saving opportunities. V1 tracks expenses only; it does not implement budgets.

## Default dashboard
New users receive a preconfigured dashboard containing:

1. total spending in selected period;
2. ordinary vs extraordinary spending;
3. spending trend over time;
4. spending by category/subcategory;
5. spending by payment method type;
6. top merchants;
7. recurring/high-frequency spending indicators;
8. recent expenses;
9. activity requiring attention.

## Configurability
The dashboard is composed of configurable sections. Users can reorder, enable/disable and configure supported widgets. Admin has separate application-usage/performance dashboards.

## Filters
Common filters:

- date range;
- category/subcategory;
- merchant;
- tag;
- payment method type;
- group/context;
- ordinary/extraordinary;
- currency where relevant;
- user/member when authorized.

## Search
Search must cover merchant/description and other indexed textual fields. Results are paginated and server-side.

## Core KPIs

- gross spending;
- effective personal spending;
- ordinary spending;
- extraordinary spending;
- average daily/weekly/monthly spending;
- number of transactions;
- largest merchants/categories.

## Charts
V1 should support at least:

- line/area trend;
- category bar chart;
- category distribution;
- payment-method distribution;
- merchant ranking;
- calendar/heatmap style view if performance permits.

Charts must remain useful on mobile.

## Analytical rules

The default personal-spending view uses the user's effective share, not gross expense, when an expense is shared with others.

Extraordinary expenses can be excluded from ordinary-spending analysis without deleting them from the ledger.

Payment method statistics use generic types (card, cash, Satispay, meal voucher, transfer, etc.), not individual card numbers/accounts unless an explicit detail view requests PSD2 provenance.

Currency conversion uses the exchange rate applicable to the expense date and must be deterministic.

## Performance
Dashboard queries are aggregated server-side. No dashboard should require downloading the full expense history to the browser.

## Admin dashboard
Admin-only dashboard includes application-level, not financial-content-by-default, metrics such as:

- registered users;
- active users;
- activity volume;
- PSD2 synchronization success/failure;
- import jobs;
- API latency/error rates;
- worker/job status;
- database/storage health;
- container resource indicators where available.

Admin financial data access is not implied by the existence of the admin role; it must be separately authorized if ever introduced.