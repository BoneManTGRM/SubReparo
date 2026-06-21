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

The repository now includes:

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
queue a project-health review request
queue an Agent Factory request
view the latest proof export when present
show the mobile request queue
switch English/Spanish
```

## What still needs a cloud runner

```text
running full scans
running full agent cycles
running repair verification
building larger agent scaffolds
continuous background monitoring
```

## Deploy path

Deploy `subreparo_mobile_app.py` as a hosted Streamlit app. Then open the hosted URL on your iPhone.

## Recommended next build step

Add a cloud-runner bridge:

```text
mobile request queue -> GitHub Action or hosted worker -> SubReparo agent command -> result back to mobile dashboard
```

That would let the iPhone control the real agent even without owning a computer.
