# SubReparo Mobile Preview

SubReparo normally binds the Control Center to localhost only:

```text
http://127.0.0.1:8765
```

That address works only on the computer running SubReparo.

To open the Control Center from an iPhone on the same Wi-Fi, use the mobile preview mode with a token.

## Start mobile preview

From the computer running SubReparo:

```bash
subreparo-immune dashboard --host 0.0.0.0 --mobile-preview --token change-this-token
```

The terminal will print a token URL.

## Open from iPhone

Find the computer's local IP address, for example:

```text
192.168.1.25
```

Then open this on the iPhone:

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
