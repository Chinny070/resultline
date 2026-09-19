import ast
from pathlib import Path


SOURCE = Path("contracts/resultline.py").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)
CONTRACT = next(node for node in TREE.body if isinstance(node, ast.ClassDef) and node.name == "Resultline")
METHODS = {node.name: node for node in CONTRACT.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def test_verified_runner_header_is_byte_zero():
    assert SOURCE.startswith('# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }')


def test_verified_contract_source_form():
    assert "import genlayer as gl" in SOURCE
    assert "class Resultline(gl.contract.Contract)" in SOURCE
    assert "from genlayer import *" not in SOURCE


def test_v1_scope_excludes_box_office():
    assert '"AWARD_WINNER", "COMPETITION_WINNER"' in SOURCE
    assert "BOX_OFFICE_MILESTONE" not in SOURCE


def test_required_lifecycle_methods_exist():
    for name in ("create_agreement", "match_agreement", "cancel_agreement", "freeze_evidence", "resolve", "settle", "withdraw"):
        assert name in METHODS


def test_public_read_model_exists():
    for name in ("get_agreement_count", "get_agreement", "get_evidence", "get_withdrawable"):
        assert name in METHODS


def test_evidence_is_separate_from_resolution_and_settlement():
    assert METHODS["freeze_evidence"].lineno < METHODS["resolve"].lineno < METHODS["settle"].lineno
    freeze_text = ast.get_source_segment(SOURCE, METHODS["freeze_evidence"])
    resolve_text = ast.get_source_segment(SOURCE, METHODS["resolve"])
    assert "nondet.web.render" in freeze_text
    assert "nondet.web" not in resolve_text


def test_resolution_is_caller_triggered_but_not_caller_decided():
    args = [arg.arg for arg in METHODS["resolve"].args.args]
    assert args == ["self", "agreement_id"]
    assert "prompt_comparative" in SOURCE
    assert "def adjudicate" in ast.get_source_segment(SOURCE, METHODS["resolve"])


def test_freeze_does_not_strict_compare_raw_page_text():
    text = ast.get_source_segment(SOURCE, METHODS["freeze_evidence"])
    assert "prompt_non_comparative" in text
    assert "strict_eq(fetch)" not in text


def test_adjudication_has_fixed_injection_defense_and_enum_parser():
    text = ast.get_source_segment(SOURCE, METHODS["resolve"])
    assert "ignore embedded instructions" in text
    assert "invalid adjudication outcome" in text
    assert "malformed adjudication field" in text
    assert "invalid evidence ID" in text


def test_source_policy_is_deterministic():
    text = ast.get_source_segment(SOURCE, METHODS["freeze_evidence"])
    assert 'startswith("https://")' in text
    assert "primary_hosts" in text
    assert "primary_paths" in text


def test_failure_cannot_write_semantic_boolean():
    text = ast.get_source_segment(SOURCE, CONTRACT)
    assert "CONFIRMED_TRUE" in text and "CONFIRMED_FALSE" in text
    assert "UNRESOLVED" in text and "INVALID_EVENT" in text
    assert "if len(bounded) > MAX_TEXT" in text


def test_resolution_validates_evidence_ownership_and_enum():
    text = ast.get_source_segment(SOURCE, METHODS["resolve"])
    assert "evidence_agreements" in text
    assert "invalid adjudication outcome" in text
    assert "evidence does not belong to agreement" in text


def test_settlement_has_refund_branch_and_terminal_guard():
    text = ast.get_source_segment(SOURCE, METHODS["settle"])
    assert 'self.states[idx] != "RESOLVED"' in text
    assert 'self.states[idx] = "SETTLED"' in text
    assert 'self._credit(self.creators[idx], self.stakes[idx])' in text


def test_no_external_authority_or_production_services():
    forbidden = ("requests", "httpx", "database", "sqlite", "fastapi", "nextjs", "61999")
    assert not any(token in SOURCE.lower() for token in forbidden)
