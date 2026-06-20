# SubReparo Mobile Preview

SubReparo normally binds the Control Center to localhost only:

```text
http://127.0.0.1:8765
```

That address works only on the computer running SubReparo.

To open the Control Center from an iPhone on the same Wi-Fi, use the mobile preview mode with a token.

## Easiest one-command preview

From the computer running SubReparo:

```bash
subreparo-mobile-preview
```

The command will:

```text
generate a token
detect the computer's local Wi-Fi IP
print the iPhone URL
start the token-gated Control Center
```

Open the printed URL on your iPhone.

## Preview plan only

To print the iPhone URL without starting the dashboard:

```bash
subreparo-mobile-preview --json
```

## Manual mobile preview

From the computer running SubReparo:

```bash
subreparo-immune dashboard --host 0.0.0.0 --mobile-preview --token change-this-token
```

The terminal will print a token URL.

## Open from iPhone

The one-command preview prints the exact URL. It will look like this:

```text
http://192.168.1.25:8765/?token=change-this-token
```

The iPhone and computer must be on the same Wi-Fi network.

## Safety rules

Mobile preview is not public hosting.

Use it only on a trusted local network.

```text
same Wi-Fi only
use a token
stop the server when finished
do not port-forward it to the internet
```

## Stop preview

In the terminal running the dashboard, press:

```text
Ctrl+C
```
