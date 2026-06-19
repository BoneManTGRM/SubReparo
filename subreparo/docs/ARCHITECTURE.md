# SubReparo Architecture

```text
+------------------------+
| SubReparo Immune       |
| local-first engine     |
+-----------+------------+
            |
            v
+------------------------+
| Local repair ledger    |
| report + jsonl + export|
+-----------+------------+
            |
            v
+------------------------+
| Chain export payload   |
| safe summaries only    |
+-----------+------------+
            |
            v
+------------------------+
| pallet-reparodynamics  |
| FRAME repair ledger    |
+-----------+------------+
            |
            v
+------------------------+
| SubReparo Chain        |
| Polkadot SDK runtime   |
+------------------------+
```

## Local-first MVP

The local engine is useful before the chain exists.

It produces:

- score;
- report;
- local ledger;
- chain export payload.

## Chain role

The chain is for durable repair memory and proof-style summaries.

The chain should not store raw private project data.

## Future adapters

- GitHub repository review.
- Pull request report bot.
- Website monitor.
- AI-agent boundary review.
- Server folder monitor.
- Desktop dashboard.
