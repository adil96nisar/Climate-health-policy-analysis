"""CHPG-O symbolic reasoning engine.

The ontology, SHACL shapes, and SPARQL rules stored in this repository are the
authoritative symbolic artifacts. The engine keeps the native graph decision and
applies a conservative public evidence-sufficiency guard so unresolved evidence
is not exposed as a positive no-gap conclusion.
"""
from __future__ import annotations
from pathlib import Path
from rdflib import Graph, Namespace, RDF
from owlrl import DeductiveClosure, OWLRL_Semantics
from pyshacl import validate

PAC = Namespace("https://w3id.org/chpg-o/pac#")
ROOT = Path(__file__).resolve().parents[1]


def local_name(term):
    return str(term).rsplit("#", 1)[-1]


class CHPGEngine:
    def __init__(self, package_root: str | Path = ROOT):
        self.root = Path(package_root)

    def analyze(self, data: Graph, output_dir: Path | None = None):
        ontology = Graph()
        for name in ["pac-core", "chpg-climate-health", "chpg-who-2023", "chpg-provenance"]:
            ontology.parse(self.root / "ontology" / f"{name}.ttl")
        shapes = Graph().parse(self.root / "shapes" / "pac-shapes.ttl")
        graph = ontology + data

        conforms, report, report_text = validate(graph, shacl_graph=shapes, inference="none", advanced=True)
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            data.serialize(output_dir / "input.ttl", format="turtle")
            report.serialize(output_dir / "shacl-input.ttl", format="turtle")
        if not conforms:
            raise ValueError("SHACL input validation failed: " + str(report_text))

        cases = list(data.subjects(RDF.type, PAC.AssessmentCase))
        if len(cases) != 1:
            raise ValueError("Exactly one independent AssessmentCase is required")
        case = cases[0]

        asserted = set(graph)
        DeductiveClosure(OWLRL_Semantics).expand(graph)
        owl_delta = set(graph) - asserted
        if output_dir:
            graph.serialize(output_dir / "owlrl.ttl", format="turtle")
            delta_graph = Graph()
            for triple in owl_delta:
                delta_graph.add(triple)
            delta_graph.serialize(output_dir / "owlrl-inferred.ttl", format="turtle")

        execution = []
        for rule in sorted((self.root / "rules").glob("R*.rq")):
            before = set(graph)
            result = graph.query(rule.read_text(encoding="utf-8"))
            for triple in result.graph:
                graph.add(triple)
            added = set(graph) - before
            execution.append({
                "rule_file": rule.name,
                "new_triple_count": len(added),
                "triples": sorted(" ".join(t.n3() for t in triple) + " ." for triple in added),
            })

        post_conforms, post_report, post_text = validate(graph, shacl_graph=shapes, inference="none", advanced=True)
        if output_dir:
            graph.serialize(output_dir / "inferred.ttl", format="turtle")
            post_report.serialize(output_dir / "shacl-output.ttl", format="turtle")
        if not post_conforms:
            raise ValueError("SHACL output validation failed: " + str(post_text))

        native = sorted(local_name(v) for v in graph.objects(case, PAC.assessmentDecision))
        gaps = sorted({
            local_name(v)
            for gap in graph.objects(case, PAC.hasGapFinding)
            for v in graph.objects(gap, PAC.gapType)
        })
        criteria = {
            graph.value(ca, PAC.assessesCriterion): graph.value(ca, PAC.criterionStatus)
            for ca in graph.objects(case, PAC.hasCriterionAssessment)
        }
        statuses = list(criteria.values())
        missing_prerequisite = any(
            criteria.get(c) == PAC.NotFoundAfterDefinedSearch
            for c in (
                PAC.ResponsibleActorCriterion,
                PAC.PolicyInstrumentCriterion,
                PAC.ImplementationPathwayCriterion,
                PAC.ResourceFinancingCriterion,
            )
        ) and criteria.get(PAC.ProblemRecognitionCriterion) != PAC.Supported

        guarded = (
            PAC.InsufficientEvidence in statuses
            or "NotAssessed" in native
            or len(native) != 1
            or missing_prerequisite
        )
        if guarded:
            final = "InsufficientEvidence"
        elif gaps:
            final = gaps[0] if len(gaps) == 1 else "MultipleGapTypes"
        elif native == ["NoConfirmedGapWithinAssessedCriteria"]:
            final = "NoConfirmedGapWithinAssessedCriteria"
        else:
            final = "InsufficientEvidence"

        return {
            "predicted_final_assessment": final,
            "native_assessment_decisions": native,
            "gap_types": gaps,
            "public_sufficiency_guard_applied": guarded,
            "implementation_rule_prerequisite_unmet": missing_prerequisite,
            "shacl_input_conforms": bool(conforms),
            "shacl_output_conforms": bool(post_conforms),
            "owl_inferred_triple_count": len(owl_delta),
            "rule_execution": execution,
            "rule_ids": sorted(
                {local_name(v) for v in graph.objects(case, PAC.decisionRule)}
                | {
                    local_name(v)
                    for gap in graph.objects(case, PAC.hasGapFinding)
                    for v in graph.objects(gap, PAC.appliedRule)
                }
            ),
        }
