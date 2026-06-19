# Aegis Mesh

Aegis Mesh is the SubReparo product architecture for a local-first defensive immune network.

## Core definition

Aegis Mesh is a defensive mesh of protected nodes. Each node runs SubReparo Immune locally, detects suspicious activity, isolates high-risk files with user approval, records repair memory, and can optionally share privacy-preserving digests with other trusted nodes.

## Design principle

```text
protect locally -> remember locally -> share safely -> improve the mesh
```

## Node model

```text
Aegis Node
  -> local sweep
  -> immune patrol
  -> baseline self/non-self memory
  -> runtime process review
  -> network review
  -> quarantine staging
  -> audit chain
  -> incident bundle
  -> optional mesh digest export
```

## Mesh layers

### 1. Aegis Node

A single protected machine or project folder.

### 2. Aegis Cell

A small trusted group of nodes, such as a family, small business, or lab.

### 3. Aegis Mesh

A larger defensive network of trusted cells.

### 4. Aegis Chain

Optional Polkadot SDK-backed repair-memory layer for digest-only proof of defensive events.

## Privacy boundary

By default, Aegis Mesh does not upload raw files, private logs, customer data, or secrets.

Mesh exports should contain:

- rule IDs;
- severity labels;
- timestamps;
- redacted targets;
- file hashes when approved;
- repair status;
- TGRM phase;
- RYE score;
- audit digest.

Mesh exports should not contain:

- raw file contents;
- private keys;
- API tokens;
- customer data;
- full private paths unless explicitly enabled.

## Defensive-only boundary

Aegis Mesh is defensive. It should not spread, exploit third-party systems, hide itself, steal credentials, or attack outside systems.

## Product promise

Aegis Mesh aims to become a user-friendly defensive immune layer:

```text
sweep -> baseline -> monitor -> detect -> explain -> isolate -> restore -> learn -> prove
```
