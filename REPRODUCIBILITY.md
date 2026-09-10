# Reproducibility

## Scope

This release supports reproducibility of the symbolic/formal CHPG-O stack. Fresh reruns of external LLM services are not claimed to be bit-for-bit reproducible because provider-side models may change and no service-level random seed was recorded. Raw copyrighted source PDFs are not redistributed.

## Verified environment

- Python 3.13.5
- RDFLib 7.6.0
- OWLRL 7.6.2
- pySHACL 0.40.1
- PrettyTable 3.18.0

## Formal workflow

1. Load `ontology/pac-core.ttl`, `ontology/chpg-climate-health.ttl`, `ontology/chpg-who-2023.ttl`, and `ontology/chpg-provenance.ttl`.
2. Validate an assessment graph against `shapes/pac-shapes.ttl`.
3. Materialise OWL 2 RL entailments.
4. Execute `rules/R00` through `rules/R07` in order.
5. Apply the conservative public evidence-sufficiency guard in `backend/chpg_engine.py`.
6. Validate the output graph again with SHACL.

The reported 24-case formal rerun produced 24/24 input conformance, 24/24 OWL closures, 24/24 completed rule executions, 24/24 output conformance, and 24/24 decisions unchanged from the frozen three-layer integration.

The primary human comparison uses an author-coded, source-verified reference set and should not be described as independent expert validation.
