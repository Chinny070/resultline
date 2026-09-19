import pytest


@pytest.mark.direct
def test_web_probe_uses_mocked_get_and_render(direct_vm, direct_deploy):
    contract = direct_deploy(
        "tests/runtime_verification/web_render_probe.py",
        sdk_version="v0.6.0-rc5",
    )
    direct_vm.mock_web(
        r"https://example\.com/",
        {
            "status": 200,
            "body": "Example Domain",
            "text": "Example Domain",
            "html": "<html><head><title>Example Domain</title></head></html>",
        },
    )

    contract.probe_get()
    contract.probe_render_text()
    contract.probe_render_html()

    assert contract.show_probe_results() == {
        "get_text_match": True,
        "render_text_match": True,
        "render_html_match": True,
    }
