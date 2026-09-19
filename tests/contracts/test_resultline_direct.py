import pytest


@pytest.mark.direct
def test_resultline_direct_creation_and_readback(direct_vm, direct_deploy):
    """Contract-level GenVM test; currently blocked by Windows gltest fd0 cleanup."""
    contract = direct_deploy("contracts/resultline.py", direct_vm, sdk_version="v0.6.0-rc5")
    agreement_id = contract.create_agreement(
        "AWARD_WINNER", "Film X wins Event Y", "Film X", "Best Picture",
        "Event Organizer", "event-y", "example.com", "/results", "YES",
        100, 200, 200, 400, 0,
    )
    assert int(agreement_id) == 0
    assert contract.get_agreement_count() == 1
