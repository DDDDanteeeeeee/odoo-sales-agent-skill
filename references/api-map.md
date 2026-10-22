# Odoo 销售 Skill 接口映射

## Action 与模型

| action | 模型 | 用途 |
|---:|---|---|
| 56 / 590 | `res.partner` | 客户 |
| 598 | `crm.lead` | 普通商机 |
| 599 | `crm.lead` | 定制商机 |
| 372 | `sale.order` | 全部销售订单 |
| 603 | `sale.order` | 定制销售订单 |
| 604 | `sale.order` | 普通销售 |
| 385 | `product.template` | 产品 |
| 219 | `product.pricelist` | 价格表 |
| 364 | `sale.report` | 销售分析 |

## Read methods

```text
res.partner/web_read_group
res.partner/read
res.partner/name_get
crm.lead/web_search_read
crm.lead/read
sale.order/web_search_read
sale.order/read
sale.order.line/read
kview.order.payment.collection.line/read
product.template/web_search_read
product.template/read
product.pricelist/web_search_read
product.pricelist/read
sale.report/web_read_group
crm.tag/read
account.tax/read
```

## Query guidance

- Lists: use `web_search_read` with `domain`, `fields`, `limit`, `offset`, and `order`.
- Details: use `read` with record IDs and an explicit field list.
- Aggregates: use `web_read_group` with `domain`, `fields`, and `groupby`.
- Use related IDs from the first query to fetch details; do not dump unrelated tables.
- Use the user's Odoo context and permissions for every request.
