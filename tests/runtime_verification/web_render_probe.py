# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }

import typing

import genlayer as gl

# TEST-ONLY WEB-RENDER VERIFICATION CONTRACT


class WebRenderVerification(gl.contract.Contract):
    """Minimal probe for Studio Next web retrieval/render support.

    This contract has no RESULTLINE state, staking, settlement, or production
    logic. It is intended only for local lint/schema/direct checks and a later
    explicitly authorized Studio Next test deployment.
    """

    get_text_match: bool
    render_text_match: bool
    render_html_match: bool

    def __init__(self):
        self.get_text_match = False
        self.render_text_match = False
        self.render_html_match = False

    @gl.public.write
    def probe_get(self) -> typing.Any:
        def fetch_text() -> bool:
            response = gl.nondet.web.get("https://example.com/")
            return "Example Domain" in response.body.decode("utf-8")

        self.get_text_match = gl.eq_principle.strict_eq(fetch_text)

    @gl.public.write
    def probe_render_text(self) -> typing.Any:
        def render_text() -> bool:
            content = gl.nondet.web.render(
                "https://example.com/",
                mode="text",
            )
            return "Example Domain" in content

        self.render_text_match = gl.eq_principle.strict_eq(render_text)

    @gl.public.write
    def probe_render_html(self) -> typing.Any:
        def render_html() -> bool:
            content = gl.nondet.web.render(
                "https://example.com/",
                mode="html",
            )
            return "<title>Example Domain</title>" in content

        self.render_html_match = gl.eq_principle.strict_eq(render_html)

    @gl.public.write
    def probe_unavailable_source(self) -> typing.Any:
        """Exercise retrieval failure without creating a semantic boolean."""
        def fetch_unavailable() -> typing.Any:
            return gl.nondet.web.get("https://resultline-stage1.invalid/")

        gl.eq_principle.strict_eq(fetch_unavailable)

    @gl.public.view
    def show_probe_results(self) -> dict[str, bool]:
        return {
            "get_text_match": self.get_text_match,
            "render_text_match": self.render_text_match,
            "render_html_match": self.render_html_match,
        }
