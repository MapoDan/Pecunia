# Dashboard Service

## Responsibility
Server-side aggregation and configurable dashboard widgets.

## Rules
- never bypass authorization;
- use effective personal amount for personal spending analytics;
- allow ordinary/extraordinary comparison;
- support period/category/payment/merchant/tag/group filters;
- return compact aggregate payloads;
- avoid a separate analytics warehouse in V1.

## Admin
Application usage/performance metrics are separate from personal financial dashboards.