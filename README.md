# CHPG-O

**Tracing Coherence and Gaps in Climate-Health Policy and News Evidence Through an Ontology-Guided RDF Knowledge Graph Framework**

CHPG-O is a news-first, three-layer neuro-symbolic framework for traceable climate-health policy assessment. The current public release preserves the original research architecture while replacing the earlier non-commensurate media/policy score subtraction with criterion-based, executable reasoning.

## Implemented evidence architecture

1. **News/media evidence** identifies and contextualises a media-visible climate-health risk profile.
2. **National policy evidence** supplies bounded P1-P8 criterion states used for policy assessment.
3. **WHO/external-memory evidence** supplies P9 normative alignment and trusted update context. WHO guidance is not treated as proof of national implementation.

The evidence layers are merged in RDF with provenance and passed through: **pySHACL input validation -> OWL 2 RL materialisation -> executable SPARQL CONSTRUCT rules R00-R07 -> evidence-sufficiency guard -> pySHACL output validation -> bounded assessment**.

## Current ontology release

The authoritative ontology is modular and stored under `ontology/`:

- `pac-core.ttl` - Policy Assessment Core (PAC), version `2.0.0-reviewer-ready`
- `chpg-climate-health.ttl` - climate-health extension, version `2.0.0-reviewer-ready`
- `chpg-who-2023.ttl` - WHO 2023 component alignment module
- `chpg-provenance.ttl` - PROV-O provenance alignment

The current release separates domain policy concepts from workflow provenance, includes explicit evidence states, P1-P9 criteria, testable OWL property-chain entailments, and executable R00-R07 decision rules. The old `Ontology_chpg-0 _updated.ttl` monolith and the previous score-subtraction logic are superseded and are not part of this release.

## Evidence states

`Supported`, `NotFoundAfterDefinedSearch`, `InsufficientEvidence`, and `NotApplicable`.

Missing retrieval is not equivalent to policy absence. Gap findings require bounded negative-search evidence inside a defined source scope.

## Gap categories

`DesignGap`, `ImplementationGap`, `CoverageGap`, `EquityGap`, and `OutcomeEvidenceGap`. These are study-developed operational categories informed by policy-design, implementation, target-population, implementation-outcome, and health-equity literature.

## Formal verification

The frozen 24-case three-layer graphs were rerun with RDFLib 7.6.0, OWLRL 7.6.2, pySHACL 0.40.1, and PrettyTable 3.18.0. All 24 inputs passed SHACL validation, all 24 completed OWL 2 RL materialisation and unchanged R00-R07 execution, all 24 outputs passed SHACL validation, and all 24 final decisions were preserved. The formal rerun produced 22,137 inferred-only triples across the 24 closures.

Primary evaluation details and the complete three-layer artifact set are documented in the accompanying paper and release package. The human benchmark is an **author-coded, source-verified reference set**, not an independent expert gold standard.

## Repository map

- `ontology/` current modular ontology
- `shapes/` SHACL constraints
- `rules/` executable SPARQL CONSTRUCT rules R00-R07
- `queries/` competency queries
- `backend/` minimal symbolic reasoning engine
- `REPRODUCIBILITY.md` environment and verification scope
- `DATA_ACCESS.md` data redistribution/access limitations
- `PROJECT_STATUS.md` implemented scope and limitations
- `CITATION.cff` citation metadata

## Public repository

https://github.com/adil96nisar/Climate-health-policy-analysis

## Data and claim limitations

Raw newspaper PDFs and some policy/source documents are not redistributed where redistribution rights are not established. The public release does not claim practitioner deployment, universal cross-domain validity, or end-to-end superiority over LLM/RAG systems.

## License

No software/data reuse license is assigned in this repository yet. Public visibility on GitHub does not itself grant reuse rights.
