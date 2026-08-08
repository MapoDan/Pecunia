# Classification Service

## Responsibility
Categories, subcategories, merchants and lightweight automatic suggestions.

## Suggestion priority
1. exact merchant history;
2. normalized merchant history;
3. merchant + payment method;
4. PSD2 description/causal text;
5. user history;
6. defaults.

Suggestions never silently overwrite a user decision.

## Resource constraint
No heavyweight ML is required. Rules/statistics must remain lightweight enough for the NAS.