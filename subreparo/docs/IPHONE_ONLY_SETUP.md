# iPhone-only SubReparo setup

This guide is for using SubReparo when you do not currently have a computer.

## Important limitation

An iPhone cannot run the full local Python SubReparo agent by itself in the same way a laptop or desktop can.

The practical setup is:

```text
iPhone -> hosted SubReparo Mobile app -> cloud runner later
```

The mobile app gives you a phone-first control panel. A cloud runner can be added later to execute the heavier Python agent tasks.

## Mobile app entrypoint

The repository includes:

```text
subreparo_mobile_app.py
```

This is a Streamlit-compatible mobile control panel.

## What the iPhone app can do now

```text
view SubReparo status
view agent cycle count
view scar-memory count
view proof-export status
view Factory registry count
run a lightweight hosted cloud health review
create a proof export from the hosted app
create Agent Factory records from blueprints
review agent permission risk
view Factory registry records
queue future mobile requests
view the mobile action log
switch English/Spanish
download JSON reports
```

## What still needs a dedicated cloud runner or computer

```text
scanning your iPhone
scanning a private local computer
repairing local machine files
continuous 24/7 endpoint monitoring
running heavyweight builds
running full Polkadot SDK chain nodes
```

## Deploy path

Deploy `subreparo_mobile_app.py` as a hosted Streamlit app. Then open the hosted URL on your iPhone.

## Recommended next build step

Add a cloud-runner bridge:

```text
mobile request queue -> GitHub Action or hosted worker -> SubReparo command -> result back to mobile dashboard
```

That would let the iPhone control the real agent even without owning a computer.
