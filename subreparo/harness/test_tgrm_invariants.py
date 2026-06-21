from __future__ import annotations

from tgrm_vs_baseline import simulate_tgrm


def test_tgrm_repair_never_exceeds_energy_cap() -> None:
    _result, rows = simulate_tgrm(
        steps=200,
        initial_drift=1.0,
        tau=0.06,
        gain=0.45,
        e_max=0.7,
        cooldown=3,
    )
    assert all(abs(row["repair"]) <= 0.7 for row in rows)


def test_tgrm_reduces_average_drift_against_unrepaired_start() -> None:
    result, _rows = simulate_tgrm(
        steps=500,
        initial_drift=1.0,
        tau=0.06,
        gain=0.45,
        e_max=0.7,
        cooldown=3,
    )
    assert result.average_abs_drift < 1.0
    assert result.repair_events > 0


def test_tgrm_cooldown_limits_repair_frequency() -> None:
    result, _rows = simulate_tgrm(
        steps=100,
        initial_drift=1.0,
        tau=0.01,
        gain=0.45,
        e_max=0.7,
        cooldown=4,
    )
    assert result.repair_events <= 25
