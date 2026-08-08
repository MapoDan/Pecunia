# Pecunia — UI/UX Guidelines

## Product character

Pecunia must feel modern, fast and calm. The primary task is recording a daily expense with minimum friction, while dashboards provide analytical depth when the user wants it.

## Principles

1. Mobile-first.
2. One-handed interaction where practical.
3. Minimal mandatory fields.
4. Smart defaults and suggestions.
5. Progressive disclosure for advanced details.
6. Clear distinction between gross expense and user's effective share.
7. Clear distinction between PENDING PSD2 operations and booked expenses.
8. Accessibility and readable contrast.
9. Consistent visual language.
10. Avoid decorative UI that slows the workflow.

## Primary navigation

Recommended information architecture:

- Home/Dashboard
- Expenses
- Activity/Notifications
- Groups (when applicable)
- Settings/Account

A prominent speed-dial/add action is recommended for quick manual expense entry.

CSV import belongs under account/configuration management, together with integrations/plugins and account connections; it must not compete with the primary expense-entry action.

## Expense entry

The quick entry should initially request only the essential amount and classification/payment information. Merchant, tags and other metadata should be suggested automatically when possible.

Example:

```text
€50
Category: Food
Merchant: Coop
Paid with:
  Meal voucher €20
  Card €30
```

The user can expand advanced details only when necessary.

## PSD2 pending operation

A pending operation must be actionable by tapping the item itself. The detail view must clearly show:

- amount identified;
- date;
- merchant/description;
- source connection/bank, e.g. “identified by Fineco account”;
- suggested classification;
- suggested payment method;
- option to change total amount;
- option to add other payment components;
- option to set personal share;
- accept/book or ignore.

There must be no ambiguity that PENDING is not yet a registered expense.

## Activity center

The activity center is the single place where actionable items can be collected. Example message:

> “Individuate 5 operazioni che necessitano aggiornamenti”

Tapping it opens the list. The user may process items individually or dismiss the notification according to the specified workflow.

## Dashboard

Dashboards are configurable sections containing charts, tables, KPIs, filters and search. Default dashboards must be preconfigured for new users, while advanced users/admins can configure sections.

Important analytical distinction:

- ordinary spending;
- extraordinary/one-time spending;
- gross expense;
- user's effective share.

## Groups

Group UI must make context obvious. A shared-account expense must never look like a personal expense without a visible context indicator.

Parent/child visibility is explicit and permission-based.

## Responsive behavior

The UI must work on:

- iPhone Safari/PWA;
- Android mobile browsers/PWA;
- tablet;
- desktop.

Touch targets must be comfortable. Desktop layouts may use denser tables and side panels.

## PWA

The application is a web application that can be installed as a PWA. Installation must not require an App Store distribution path. Offline support is limited to safe UI/app-shell behavior in V1; financial writes require server confirmation.

## Visual system

Use a small, coherent design system with:

- typography scale;
- spacing scale;
- semantic states;
- cards/surfaces;
- form controls;
- chart rules;
- empty/error/loading states.

The final logo and icon are stored under `Logo/`.