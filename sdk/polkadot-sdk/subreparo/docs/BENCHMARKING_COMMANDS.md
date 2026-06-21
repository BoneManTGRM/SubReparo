# SubReparo FRAME Benchmarking Commands

These are template commands. Adjust node binary, chain spec, pallet names, and output paths for the selected Polkadot SDK runtime.

## pallet-subreparo

```bash
./target/release/reparo-node benchmark pallet \
  --chain dev \
  --pallet pallet_subreparo \
  --extrinsic '*' \
  --steps 50 \
  --repeat 20 \
  --output frame/subreparo/src/weights.rs
```

## pallet-subreparo-controller

```bash
./target/release/reparo-node benchmark pallet \
  --chain dev \
  --pallet pallet_subreparo_controller \
  --extrinsic '*' \
  --steps 50 \
  --repeat 20 \
  --output frame/subreparo-controller/src/weights.rs
```

## pallet-subreparo-finality-backoff

```bash
./target/release/reparo-node benchmark pallet \
  --chain dev \
  --pallet pallet_subreparo_finality_backoff \
  --extrinsic '*' \
  --steps 50 \
  --repeat 20 \
  --output frame/subreparo-finality-backoff/src/weights.rs
```

## Requirement

Do not use stub weights for production claims. Generate and review real weights from the target runtime.
