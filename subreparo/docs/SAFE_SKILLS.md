# SubReparo Safe Skill Review

SubReparo skills are not executed by default.

The first implementation is a manifest review system that answers:

```text
What does this add-on claim to do?
What permissions does it request?
Is the permission set low, medium, high, or blocked risk?
Should a human approve it first?
```

## Manifest format

```json
{
  "name": "docs-helper",
  "version": "0.1.0",
  "description": "Helps update local documentation.",
  "permissions": ["read_project"],
  "entrypoint": "optional-entrypoint",
  "author": "optional-author"
}
```

## Permission levels

Low-risk examples:

```text
read_project
read_subreparo_state
```

Medium-risk examples:

```text
write_project
write_subreparo_state
network_read
```

High-risk examples:

```text
network_write
shell_read
external_message
publish_public
```

Blocked examples:

```text
shell_write
secrets_read
spend_money
delete_data
```

## Review command

Until a console script is added, run the reviewer through Python module execution:

```bash
cd tools/subreparo-immune
python -m subreparo_immune.skills_cli ../../ --json
```

## Design rule

SubReparo must never silently execute third-party add-ons.

Future execution must require:

- manifest review;
- declared permissions;
- risk score;
- approval gate;
- audit record;
- safe rollback or disable path.
