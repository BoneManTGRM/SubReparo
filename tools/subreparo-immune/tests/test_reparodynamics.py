from subreparo_immune.reparodynamics import (
    RepairOutcome,
    RepairPhase,
    RepairSignal,
    repair_yield_per_energy,
    score_repair,
    tgrm_phase,
)


def test_rye_calculation() -> None:
    assert repair_yield_per_energy(0.8, 0.2) == 4.0


def test_tgrm_detect_phase() -> None:
    signal = RepairSignal(stress=0.8, fracture=0.8, repair_gain=0.0, energy_cost=1.0, confidence=0.0)
    assert tgrm_phase(signal) == RepairPhase.DETECT


def test_verified_repair_score() -> None:
    signal = RepairSignal(stress=0.5, fracture=0.4, repair_gain=0.6, energy_cost=0.3, confidence=0.9)
    score = score_repair(signal)
    assert score.outcome == RepairOutcome.VERIFIED
    assert score.rye == 2.0
