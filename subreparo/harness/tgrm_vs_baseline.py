from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SimulationResult:
    mode: str
    steps: int
    average_abs_drift: float
    max_abs_drift: float
    repair_events: int
    energy_used: float


def deterministic_noise(step: int) -> float:
    return (((step * 1103515245 + 12345) % 65536) / 65536.0 - 0.5) * 0.012


def simulate_baseline(*, steps: int, initial_drift: float, decay: float) -> tuple[SimulationResult, list[dict[str, float]]]:
    drift = initial_drift
    rows: list[dict[str, float]] = []
    total_abs = 0.0
    max_abs = 0.0
    for step in range(steps):
        drift = drift * (1.0 - decay) + deterministic_noise(step)
        abs_drift = abs(drift)
        total_abs += abs_drift
        max_abs = max(max_abs, abs_drift)
        rows.append({"step": step, "drift": drift, "repair": 0.0, "energy": 0.0})
    return SimulationResult("baseline", steps, total_abs / steps, max_abs, 0, 0.0), rows


def simulate_tgrm(
    *,
    steps: int,
    initial_drift: float,
    tau: float,
    gain: float,
    e_max: float,
    cooldown: int,
) -> tuple[SimulationResult, list[dict[str, float]]]:
    drift = initial_drift
    cooldown_remaining = 0
    total_abs = 0.0
    max_abs = 0.0
    repair_events = 0
    energy_used = 0.0
    rows: list[dict[str, float]] = []
    for step in range(steps):
        drift += deterministic_noise(step)
        repair = 0.0
        energy = 0.0
        if cooldown_remaining > 0:
            cooldown_remaining -= 1
        if abs(drift) > tau and cooldown_remaining == 0:
            gradient = drift * gain
            repair = max(-e_max, min(e_max, gradient))
            drift -= repair
            energy = abs(repair)
            energy_used += energy
            repair_events += 1
            cooldown_remaining = cooldown
        abs_drift = abs(drift)
        total_abs += abs_drift
        max_abs = max(max_abs, abs_drift)
        rows.append({"step": step, "drift": drift, "repair": repair, "energy": energy})
    return SimulationResult("tgrm", steps, total_abs / steps, max_abs, repair_events, energy_used), rows


def run(output: Path | None = None) -> dict[str, object]:
    baseline, baseline_rows = simulate_baseline(steps=1000, initial_drift=1.0, decay=0.002)
    tgrm, tgrm_rows = simulate_tgrm(steps=1000, initial_drift=1.0, tau=0.06, gain=0.45, e_max=0.7, cooldown=3)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["mode", "step", "drift", "repair", "energy"])
            writer.writeheader()
            for row in baseline_rows:
                writer.writerow({"mode": "baseline", **row})
            for row in tgrm_rows:
                writer.writerow({"mode": "tgrm", **row})
    improvement = 0.0
    if baseline.average_abs_drift:
        improvement = 1.0 - (tgrm.average_abs_drift / baseline.average_abs_drift)
    return {
        "schema": "subreparo.tgrm_harness.v1",
        "baseline": asdict(baseline),
        "tgrm": asdict(tgrm),
        "average_drift_reduction": improvement,
        "csv": str(output) if output else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare baseline drift against bounded TGRM repair.")
    parser.add_argument("--csv", default="subreparo/harness/tgrm_vs_baseline.csv")
    args = parser.parse_args()
    result = run(Path(args.csv))
    print(result)


if __name__ == "__main__":
    main()
