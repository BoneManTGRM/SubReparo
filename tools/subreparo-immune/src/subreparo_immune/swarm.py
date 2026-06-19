from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .detectors import check_website, scan_git, scan_project
from .immune_patrol import patrol
from .models import Finding, FindingType, Severity


class Analyzer(Protocol):
    name: str

    def run(self, root: Path, websites: list[str]) -> list[Finding]:
        ...


@dataclass(frozen=True)
class AnalyzerResult:
    analyzer: str
    findings: list[Finding]

    def to_dict(self) -> dict[str, object]:
        return {
            "analyzer": self.analyzer,
            "findings": [finding.to_dict() for finding in self.findings],
        }


class ProjectAnalyzer:
    name = "project"

    def run(self, root: Path, websites: list[str]) -> list[Finding]:
        return scan_project(root)


class ImmunePatrolAnalyzer:
    name = "immune-patrol"

    def run(self, root: Path, websites: list[str]) -> list[Finding]:
        return patrol(root)


class GitAnalyzer:
    name = "git"

    def run(self, root: Path, websites: list[str]) -> list[Finding]:
        return scan_git(root)


class WebsiteAnalyzer:
    name = "website"

    def run(self, root: Path, websites: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        for website in websites:
            findings.extend(check_website(website))
        return findings


class ProductReadinessAnalyzer:
    name = "product-readiness"

    def run(self, root: Path, websites: list[str]) -> list[Finding]:
        findings: list[Finding] = []
        important = {
            "README.md": "Add a root README before sharing or release.",
            "CHANGELOG.md": "Add a changelog before release.",
            "THIRD_PARTY_NOTICES.md": "Add third-party notices before public or commercial use.",
        }
        for filename, recommendation in important.items():
            if not (root / filename).exists():
                findings.append(Finding(
                    type=FindingType.PROJECT_CHANGE,
                    severity=Severity.MEDIUM,
                    target=filename,
                    message=f"Expected product file missing: {filename}",
                    recommendation=recommendation,
                ))
        return findings


ANALYZERS: list[Analyzer] = [
    ProjectAnalyzer(),
    ImmunePatrolAnalyzer(),
    GitAnalyzer(),
    WebsiteAnalyzer(),
    ProductReadinessAnalyzer(),
]


def run_swarm(root: Path, websites: list[str] | None = None) -> list[AnalyzerResult]:
    root = root.resolve()
    website_list = websites or []
    results: list[AnalyzerResult] = []
    for analyzer in ANALYZERS:
        results.append(AnalyzerResult(analyzer=analyzer.name, findings=analyzer.run(root, website_list)))
    return results


def flatten(results: list[AnalyzerResult]) -> list[Finding]:
    findings: list[Finding] = []
    for result in results:
        findings.extend(result.findings)
    return findings
