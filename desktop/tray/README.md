# SubReparo Desktop Tray Scaffold

This folder defines the future desktop tray/control-center direction for SubReparo.

## Scope

The tray app should be local-first and should not perform high-impact repair actions without approval.

Planned tray functions:

- show local monitor status;
- open the localhost dashboard;
- show pending approvals;
- surface watch alerts;
- launch scan, trust, learning, and report commands;
- keep destructive or high-impact actions behind explicit approval.

## Safety boundary

The tray scaffold is documentation only at this stage. It does not install background services, modify startup entries, or change system settings.
