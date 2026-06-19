from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class RepairPhase(str, Enum):
    TEST = "test"
    DETECT = "detect"
    REPAIR = "repair"
    VERIFY = "verify"
    MEMORY = "memory"


class RepairOutcome(str, Enum):
    PENDING = "pending"
    IMPROVED = "improved"
    VERIFIED = "verified"
    REGRESSED = "regressed"
    RECURRING = "recurring"


@dataclass(frozen=True)
class RepairSignal:
    stress: float
    fracture: float
    repair_gain: float
    energy_cost: float
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepairScore:
    rye: float
    stability: float
    efficiency: float
    phase: RepairPhase
    outcome: RepairOutcome

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["phase"] = self.phase.value
        data["outcome"] = self.outcome.value
        return data


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def repair_yield_per_energy(repair_gain: float, energy_cost: float) -> float:
    if energy_cost <= 0:
        return 0.0
    return repair_gain / energy_cost


def tgrm_phase(signal: RepairSignal) -> RepairPhase:
    if signal.stress <= 0 and signal.fracture <= 0:
        return RepairPhase.TEST
    if signal.fracture > 0 and signal.repair_gain <= 0:
        return RepairPhase.DETECT
    if signal.repair_gain > 0 and signal.confidence < 0.8:
        return RepairPhase.REPAIR
    if signal.confidence >= 0.8 and signal.repair_gain > 0:
        return RepairPhase.VERIFY
    return RepairPhase.MEMORY


def score_repair(signal: RepairSignal) -> RepairScore:
    rye = repair_yield_per_energy(signal.repair_gain, signal.energy_cost)
    stability = clamp(1.0 - signal.fracture + signal.repair_gain)
    efficiency = clamp(rye / 10.0)
    phase = tgrm_phase(signal)
    if signal.fracture > 0 and signal.repair_gain <= 0:
        outcome = RepairOutcome.PENDING
    elif signal.repair_gain > 0 and signal.confidence < 0.8:
        outcome = RepairOutcome.IMPROVED
    elif signal.repair_gain > 0 and signal.confidence >= 0.8:
        outcome = RepairOutcome.VERIFIED
    else:
        outcome = RepairOutcome.PENDING
    return RepairScore(
        rye=round(rye, 6),
        stability=round(stability, 6),
        efficiency=round(efficiency, 6),
        phase=phase,
        outcome=outcome,
    )


def finding_signal(severity_weight: float, verified_gain: float = 0.0, energy_cost: float = 1.0) -> RepairSignal:
    stress = clamp(severity_weight)
    fracture = clamp(severity_weight)
    return RepairSignal(
        stress=stress,
        fracture=fracture,
        repair_gain=clamp(verified_gain),
        energy_cost=max(energy_cost, 0.000001),
        confidence=clamp(verified_gain),
    )
