# SubReparo Messaging Connectors

SubReparo can integrate with messaging platforms only through official APIs and explicit user configuration.

## Supported connector targets

```text
Telegram Bot API
WhatsApp Business Platform / Cloud API
```

## Safety model

SubReparo messaging access must follow these rules:

```text
official APIs only
no scraping personal WhatsApp Web
no hidden message sending
recipient allowlist required
outbound messages require approval
tokens are read from environment variables only
```

## Telegram setup

Create a Telegram bot with BotFather, then configure:

```bash
export SUBREPARO_TELEGRAM_BOT_TOKEN="your-bot-token"
export SUBREPARO_TELEGRAM_ALLOWED_CHAT_IDS="123456789,987654321"
```

Check status:

```bash
cd tools/subreparo-immune
python -m subreparo_immune.messaging_cli --status --json
```

Plan a message without sending:

```bash
python -m subreparo_immune.messaging_cli \
  --plan-message \
  --channel telegram \
  --recipient 123456789 \
  --text "SubReparo needs approval" \
  --json
```

## WhatsApp setup

Use Meta's official WhatsApp Business Platform / Cloud API.

Configure:

```bash
export SUBREPARO_WHATSAPP_ACCESS_TOKEN="your-meta-access-token"
export SUBREPARO_WHATSAPP_PHONE_NUMBER_ID="your-phone-number-id"
export SUBREPARO_WHATSAPP_ALLOWED_RECIPIENTS="5215555555555"
```

Plan a message without sending:

```bash
python -m subreparo_immune.messaging_cli \
  --plan-message \
  --channel whatsapp \
  --recipient 5215555555555 \
  --text "SubReparo needs approval" \
  --json
```

## Current implementation

The current connector layer performs:

```text
configuration readiness checks
recipient allowlist checks
message preview planning
approval requirement flags
safe status reporting
```

It does not silently send messages.

## Next implementation step

Add an approval-queue bridge:

```text
approved message plan -> outbound queue -> audit record -> official API send
```

Actual sending must remain disabled unless the user approves the specific outbound action.
