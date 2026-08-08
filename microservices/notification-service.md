# Notification Service

## Responsibility
Activity Center and actionable notifications.

## V1
- pending PSD2 operations;
- historical update suggestions;
- dismiss/process state;
- aggregation of items requiring attention.

A heavy push infrastructure is not required in V1. Polling/API refresh is acceptable.

## Rule
Notifications must be idempotent and must not cause duplicate financial writes.