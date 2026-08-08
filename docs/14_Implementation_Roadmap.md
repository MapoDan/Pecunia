# Pecunia — Implementation Roadmap

This document is an implementation sequence for the development AI. It contains no implementation code.

## Phase 0 — Documentation and foundation

- Read all canonical docs.
- Resolve any contradiction before coding.
- Establish project structure, configuration, Docker and CI.
- No financial feature yet.

## Phase 1 — Identity

- Google login.
- User creation/default settings.
- Role model and authorization foundation.
- Session/security hardening.

**Exit:** authenticated user can access only their own context.

## Phase 2 — Expense engine

- categories/subcategories;
- merchants;
- payment methods;
- expense CRUD;
- extraordinary flag;
- tags;
- minimal-entry UX and suggestions.

**Exit:** manual expenses can be recorded and queried reliably.

## Phase 3 — Payment and personal share

- multiple payment components;
- payment total invariant;
- effective personal amount;
- shared expense handling.

**Exit:** examples such as €10 = €8 card + €2 voucher and €10 gross/€5 personal are correctly represented in ledger and analytics.

## Phase 4 — Dashboard

- default widgets;
- filters/search;
- ordinary vs extraordinary comparison;
- effective personal spending;
- trends/category/merchant/payment analysis.

**Exit:** user can understand spending behavior without exporting data.

## Phase 5 — Activity center

- actionable items;
- pending PSD2 placeholders;
- dismiss/process semantics;
- update-suggestion notifications.

## Phase 6 — PSD2

- connections;
- connection start date;
- provider adapter;
- synchronization;
- PENDING transaction store;
- accept/ignore;
- editable amount/payment split;
- provenance/account display;
- deduplication.

**Exit:** no PSD2 transaction becomes an expense without explicit user decision.

## Phase 7 — CSV

- configuration/account import area;
- upload;
- mapping;
- preview;
- validation;
- commit;
- duplicate detection;
- historical dates.

## Phase 8 — Groups

- groups;
- members/roles;
- shared account;
- group-only shared expenses;
- parental visibility;
- global tags/admin control.

## Phase 9 — Admin

- application usage dashboard;
- performance/health metrics;
- operational activity;
- no implicit access to users' financial content.

## Phase 10 — Security hardening

- threat-model verification;
- authorization tests;
- secret review;
- dependency review;
- backup/restore test;
- production deployment checklist.

## Phase 11 — Passkeys

Implement WebAuthn/passkey registration and authentication without weakening Google onboarding or account recovery.

## Phase 12 — Release

- end-to-end regression;
- performance test on NAS;
- backup/restore drill;
- documentation freeze;
- release notes;
- V1 scope verification.

## Development rule

Implement vertical slices. Do not build an entire backend before connecting the frontend. Every phase must leave the system in a coherent, testable state.