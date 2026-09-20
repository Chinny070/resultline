import ast
from pathlib import Path

SOURCE = Path("contracts/resultline.py").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)
CONTRACT = next(n for n in TREE.body if isinstance(n, ast.ClassDef) and n.name == "Resultline")
METHODS = {n.name: n for n in CONTRACT.body if isinstance(n, ast.FunctionDef)}

def test_depends_header_and_class():
    assert SOURCE.startswith('# v0.2.16')
    assert '# { "Depends":' in SOURCE
    assert "class Resultline(gl.contract.Contract)" in SOURCE

def test_v1_enums_and_lifecycle():
    for value in ("AWARD_WINNER", "COMPETITION_WINNER", "YES", "NO", "CONFIRMED_TRUE", "CONFIRMED_FALSE", "UNRESOLVED", "INVALID_EVENT", "OPEN", "MATCHED", "EVIDENCE_FROZEN", "RESOLVED", "SETTLED"):
        assert value in SOURCE
    for name in ("create_agreement", "match_agreement", "cancel_agreement", "freeze_evidence", "resolve", "settle", "withdraw", "get_agreement", "get_agreement_count", "get_evidence", "get_withdrawable"):
        assert name in METHODS

def test_constitution_and_explicit_counterparty_position():
    assert "counterparty_position: gl.storage.DynArray[str]" in SOURCE
    text = ast.get_source_segment(SOURCE, METHODS["match_agreement"])
    assert "counterparty_position" in text and "position == self.creator_position" in text
    assert "temporal_mode" in SOURCE and "POST_EVENT_VERIFICATION" in SOURCE

def test_resolution_traceability_and_evidence_references():
    for name in ("resolution_source_authority", "resolution_event_status", "resolution_temporal_validity", "resolution_subject_match", "resolution_category_match", "resolution_evidence_sufficiency", "resolution_evidence_ids", "resolution_rationale"):
        assert name in SOURCE
    text = ast.get_source_segment(SOURCE, METHODS["resolve"])
    for phrase in ("evidence_ids_relied_on", "rationale", "do not browse", "untrusted data", "missing evidence"):
        assert phrase in text.lower()

def test_storage_and_timestamp():
    assert "owed: gl.storage.TreeMap[gl.Address, gl.u256]" in SOURCE
    assert "datetime.now(timezone.utc)" in SOURCE

def test_source_policy_and_render_flow():
    assert '"https://"' in SOURCE and "source_url !=" in SOURCE
    text = ast.get_source_segment(SOURCE, METHODS["freeze_evidence"])
    assert "gl.nondet.web.render" in text and "prompt_non_comparative" in text
    assert "untrusted evidence data" in text

def test_adjudication_is_structured_and_fail_closed():
    text = ast.get_source_segment(SOURCE, METHODS["resolve"])
    assert "exec_prompt" in text and "response_format=\"json\"" in text
    assert "prompt_comparative" in text and "malformed adjudication" in text
    assert "UNRESOLVED" in text and "CONFIRMED_FALSE" in text

def test_deterministic_settlement_and_withdrawal():
    settle = ast.get_source_segment(SOURCE, METHODS["settle"])
    withdraw = ast.get_source_segment(SOURCE, METHODS["withdraw"])
    assert "CONFIRMED_TRUE" in settle and "CONFIRMED_FALSE" in settle
    assert "self._credit(self.creator[i], self.stake[i])" in settle
    assert "self.owed[gl.message.sender_address] = gl.u256(0)" in withdraw
    assert "emit_transfer" in withdraw and "get_at" not in withdraw

def test_no_admin_or_external_service_backdoor():
    assert "admin" not in SOURCE.lower()
    for forbidden in ("requests", "httpx", "fastapi", "sqlite", "61997"):
        assert forbidden not in SOURCE.lower()
