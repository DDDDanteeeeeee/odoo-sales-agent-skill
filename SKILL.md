---
name: odoo-sales-agent
version: 0.1.0
description: Use this skill whenever a user asks about Odoo CRM sales data, customers, opportunities, sales orders, products, pricelists, sales analysis, customer status, follow-up planning, product customer tracking, sales performance, or any business task that requires retrieving and reasoning over sales data from an Odoo instance. The skill provides read-only Odoo JSON-RPC access; the agent must decompose the user's business goal, retrieve only the required records, analyze them, and return the completed business result rather than a raw data dump unless raw data is explicitly requested.
compatibility: Requires Python 3.10+ and an Odoo 16-compatible instance. Configure ODOO_URL, ODOO_DB, ODOO_LOGIN, and ODOO_PASSWORD in the runtime environment, or obtain equivalent credentials through the host agent's approved login flow.
---

# Odoo Sales Agent

Use the bundled read-only RPC client to obtain facts from the user's Odoo sales module, then complete the user's business task. The user's request is the task; CRM data retrieval is an internal step.

## Operating rules

- Treat Odoo as the source of record for CRM facts.
- Use only the allowlisted read methods in `scripts/odoo_rpc_read.py`.
- Never call create, write, unlink, action, workflow, approval, export, print, attachment-download, ERP push, delivery, payment, refund, or status-changing methods.
- Query the smallest useful field set and paginate large lists.
- Preserve the user's Odoo permissions. Do not use administrator credentials or `sudo` semantics.
- Distinguish observed facts from analysis and recommendations.
- When the request is ambiguous, ask only for the missing business constraint; do not ask the user to design the API query.
- Return the completed task result. Include a concise evidence section with the models and time range used when that helps the user verify the result.

## Connection configuration

The client reads configuration from environment variables:

```text
ODOO_URL       Base URL, for example http://192.168.0.192
ODOO_DB        Database name, for example kv
ODOO_LOGIN     Odoo login
ODOO_PASSWORD  Odoo password
```

Do not put passwords or session cookies in prompts, source files, commits, or reports. If configuration is absent, ask the user to configure it through the host agent's approved secret mechanism.

## Read workflow

1. Identify the business entity and requested outcome.
2. Select the minimum models from `references/api-map.md`.
3. Use list reads to identify relevant record IDs.
4. Use detail reads and related models to gather the evidence needed for the task.
5. Reconcile duplicates, dates, currencies, statuses, and relationships before reasoning.
6. Produce the requested business result: assessment, next actions, follow-up plan, ranking, summary, or raw data.
7. State when the available Odoo permissions or data do not support a conclusion.

## Common task patterns

### Customer situation and next action

Read `res.partner`, related `crm.lead`, related `sale.order`, recent activities, and payment/order status. Summarize current relationship, open opportunities, recent activity, risks, and prioritized next actions.

### Product customer tracking

Read `sale.order.line` for the target product, resolve `partner_id` through related orders, deduplicate customers, then read opportunity and activity context. Group customers by value, recency, opportunity stage, and follow-up need.

### Sales performance

Use `sale.report/web_read_group` with an explicit date domain and groupby such as `user_id`, `team_id`, `partner_id`, `product_id`, or `state`. Explain currency and date boundaries.

## Output contract

Unless the user asks for raw data, structure the response as:

1. Result or current situation
2. Evidence used
3. Recommended next actions
4. Uncertainty or missing permissions

Do not expose JSON-RPC payloads unless the user asks for technical details.
