# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }

import typing

import genlayer as gl


MAX_TEXT = 512
MAX_URL = 512
MAX_EVIDENCE = 4


class Resultline(gl.contract.Contract):
    """Narrow V1, two-party, binary entertainment-outcome agreement.

    Evidence is frozen separately from semantic resolution. This contract stores
    bounded text and deterministic state only; model output never selects an
    arbitrary transfer amount.
    """

    agreement_count: gl.u256
    states: gl.storage.DynArray[str]
    outcome_types: gl.storage.DynArray[str]
    propositions: gl.storage.DynArray[str]
    subjects: gl.storage.DynArray[str]
    categories: gl.storage.DynArray[str]
    organizers: gl.storage.DynArray[str]
    event_ids: gl.storage.DynArray[str]
    primary_hosts: gl.storage.DynArray[str]
    primary_paths: gl.storage.DynArray[str]
    positions: gl.storage.DynArray[str]
    creators: gl.storage.DynArray[gl.Address]
    counterparties: gl.storage.DynArray[gl.Address]
    stakes: gl.storage.DynArray[gl.u256]
    betting_closes: gl.storage.DynArray[gl.u256]
    expected_events: gl.storage.DynArray[gl.u256]
    resolution_not_before: gl.storage.DynArray[gl.u256]
    resolution_deadlines: gl.storage.DynArray[gl.u256]
    correction_windows: gl.storage.DynArray[gl.u256]
    evidence_counts: gl.storage.DynArray[gl.u256]
    evidence_urls: gl.storage.DynArray[str]
    evidence_text: gl.storage.DynArray[str]
    evidence_fingerprints: gl.storage.DynArray[str]
    evidence_agreements: gl.storage.DynArray[gl.u256]
    evidence_frozen_at: gl.storage.DynArray[gl.u256]
    resolution_outcomes: gl.storage.DynArray[str]
    owed: gl.storage.TreeMap[gl.Address, gl.u256]

    def __init__(self):
        self.agreement_count = 0
        self.states = []
        self.outcome_types = []
        self.propositions = []
        self.subjects = []
        self.categories = []
        self.organizers = []
        self.event_ids = []
        self.primary_hosts = []
        self.primary_paths = []
        self.positions = []
        self.creators = []
        self.counterparties = []
        self.stakes = []
        self.betting_closes = []
        self.expected_events = []
        self.resolution_not_before = []
        self.resolution_deadlines = []
        self.correction_windows = []
        self.evidence_counts = []
        self.evidence_urls = []
        self.evidence_text = []
        self.evidence_fingerprints = []
        self.evidence_agreements = []
        self.evidence_frozen_at = []
        self.resolution_outcomes = []
        self.owed = {}

    def _bounded(self, value: str, name: str) -> None:
        if not value or len(value) > MAX_TEXT:
            raise gl.vm.UserError(f"invalid {name}")

    def _now(self) -> gl.u256:
        return gl.u256(int(gl.vm.get_timestamp().timestamp()))

    def _valid_id(self, agreement_id: gl.u256) -> int:
        idx = int(agreement_id)
        if idx < 0 or idx >= int(self.agreement_count):
            raise gl.vm.UserError("unknown agreement")
        return idx

    def _credit(self, account: gl.Address, amount: gl.u256) -> None:
        self.owed[account] = self.owed.get(account, gl.u256(0)) + amount

    @gl.public.write.payable
    def create_agreement(
        self,
        outcome_type: str,
        proposition: str,
        subject: str,
        category: str,
        organizer: str,
        event_id: str,
        primary_host: str,
        primary_path: str,
        position: str,
        betting_closes_at: gl.u256,
        expected_event_at: gl.u256,
        resolution_not_before_at: gl.u256,
        resolution_deadline_at: gl.u256,
        correction_window: gl.u256,
    ) -> gl.u256:
        if outcome_type not in ("AWARD_WINNER", "COMPETITION_WINNER"):
            raise gl.vm.UserError("unsupported outcome type")
        if position not in ("YES", "NO"):
            raise gl.vm.UserError("invalid position")
        for value, name in ((proposition, "proposition"), (subject, "subject"),
                            (category, "category"), (organizer, "organizer"),
                            (event_id, "event_id"), (primary_host, "primary_host")):
            self._bounded(value, name)
        if len(primary_host) > MAX_URL or not primary_host or "." not in primary_host:
            raise gl.vm.UserError("invalid host")
        if primary_path and len(primary_path) > MAX_URL or primary_path and not primary_path.startswith("/"):
            raise gl.vm.UserError("invalid path")
        stake = gl.u256(gl.message.value)
        if stake <= 0:
            raise gl.vm.UserError("positive stake required")
        if not (betting_closes_at <= expected_event_at <= resolution_not_before_at < resolution_deadline_at):
            raise gl.vm.UserError("invalid time ordering")
        idx = int(self.agreement_count)
        self.agreement_count += 1
        self.states.append("OPEN")
        self.outcome_types.append(outcome_type)
        self.propositions.append(proposition)
        self.subjects.append(subject)
        self.categories.append(category)
        self.organizers.append(organizer)
        self.event_ids.append(event_id)
        self.primary_hosts.append(primary_host)
        self.primary_paths.append(primary_path)
        self.positions.append(position)
        self.creators.append(gl.message.sender_address)
        self.counterparties.append(gl.message.sender_address)
        self.stakes.append(stake)
        self.betting_closes.append(betting_closes_at)
        self.expected_events.append(expected_event_at)
        self.resolution_not_before.append(resolution_not_before_at)
        self.resolution_deadlines.append(resolution_deadline_at)
        self.correction_windows.append(correction_window)
        self.evidence_counts.append(0)
        self.resolution_outcomes.append("")
        return gl.u256(idx)

    @gl.public.write.payable
    def match_agreement(self, agreement_id: gl.u256) -> None:
        idx = self._valid_id(agreement_id)
        if self.states[idx] != "OPEN" or self.creators[idx] == gl.message.sender_address:
            raise gl.vm.UserError("agreement cannot be matched")
        if self._now() > self.betting_closes[idx]:
            raise gl.vm.UserError("betting closed")
        if gl.message.value != self.stakes[idx]:
            raise gl.vm.UserError("exact equal stake required")
        if self.positions[idx] == "YES":
            self.counterparties[idx] = gl.message.sender_address
        else:
            self.counterparties[idx] = gl.message.sender_address
        self.states[idx] = "MATCHED"

    @gl.public.write
    def cancel_agreement(self, agreement_id: gl.u256) -> None:
        idx = self._valid_id(agreement_id)
        if self.states[idx] != "OPEN" or self.creators[idx] != gl.message.sender_address:
            raise gl.vm.UserError("only unmatched creator may cancel")
        self.states[idx] = "CANCELLED"
        self._credit(self.creators[idx], self.stakes[idx])

    @gl.public.write
    def freeze_evidence(self, agreement_id: gl.u256, source_url: str) -> gl.u256:
        idx = self._valid_id(agreement_id)
        if self.states[idx] not in ("MATCHED", "AWAITING_EVENT", "EVIDENCE_FROZEN"):
            raise gl.vm.UserError("evidence not allowed")
        if self._now() < self.resolution_not_before[idx]:
            raise gl.vm.UserError("too early")
        if len(source_url) == 0 or len(source_url) > MAX_URL or not source_url.startswith("https://"):
            raise gl.vm.UserError("HTTPS source required")
        host_prefix = "https://" + self.primary_hosts[idx]
        if not source_url.startswith(host_prefix):
            raise gl.vm.UserError("source host not permitted")
        if self.primary_paths[idx] and not source_url.startswith(host_prefix + self.primary_paths[idx]):
            raise gl.vm.UserError("source path not permitted")
        if int(self.evidence_counts[idx]) >= MAX_EVIDENCE:
            raise gl.vm.UserError("evidence limit")
        def fetch() -> str:
            return gl.nondet.web.render(source_url, mode="text")
        bounded = gl.eq_principle.strict_eq(fetch)
        if len(bounded) > MAX_TEXT:
            raise gl.vm.UserError("evidence exceeds bound")
        evidence_id = len(self.evidence_urls)
        self.evidence_urls.append(source_url)
        self.evidence_text.append(bounded)
        self.evidence_fingerprints.append(str(len(bounded)) + ":" + bounded[:32])
        self.evidence_agreements.append(agreement_id)
        self.evidence_frozen_at.append(self._now())
        self.evidence_counts[idx] += 1
        self.states[idx] = "EVIDENCE_FROZEN"
        return gl.u256(evidence_id)

    @gl.public.write
    def resolve(self, agreement_id: gl.u256, outcome: str, evidence_id: gl.u256) -> None:
        idx = self._valid_id(agreement_id)
        if self.states[idx] != "EVIDENCE_FROZEN":
            raise gl.vm.UserError("evidence required")
        if outcome not in ("CONFIRMED_TRUE", "CONFIRMED_FALSE", "UNRESOLVED", "INVALID_EVENT"):
            raise gl.vm.UserError("invalid outcome")
        evidence_idx = int(evidence_id)
        if evidence_idx < 0 or evidence_idx >= len(self.evidence_urls) or self.evidence_agreements[evidence_idx] != agreement_id:
            raise gl.vm.UserError("evidence does not belong to agreement")
        if self._now() > self.resolution_deadlines[idx] and outcome not in ("UNRESOLVED", "INVALID_EVENT"):
            raise gl.vm.UserError("resolution deadline passed")
        self.resolution_outcomes[idx] = outcome
        self.states[idx] = "RESOLVED"

    @gl.public.write
    def settle(self, agreement_id: gl.u256) -> None:
        idx = self._valid_id(agreement_id)
        if self.states[idx] != "RESOLVED":
            raise gl.vm.UserError("not resolved")
        outcome = self.resolution_outcomes[idx]
        pot = self.stakes[idx] * (2 if self.counterparties[idx] != self.creators[idx] else 1)
        if outcome == "CONFIRMED_TRUE":
            self._credit(self.creators[idx] if self.positions[idx] == "YES" else self.counterparties[idx], pot)
        elif outcome == "CONFIRMED_FALSE":
            self._credit(self.creators[idx] if self.positions[idx] == "NO" else self.counterparties[idx], pot)
        else:
            self._credit(self.creators[idx], self.stakes[idx])
            if self.counterparties[idx] != self.creators[idx]:
                self._credit(self.counterparties[idx], self.stakes[idx])
        self.states[idx] = "SETTLED"

    @gl.public.write
    def withdraw(self) -> None:
        amount = self.owed.get(gl.message.sender_address, gl.u256(0))
        if amount <= 0:
            raise gl.vm.UserError("nothing owed")
        self.owed[gl.message.sender_address] = 0
        gl.contract.get_at(gl.message.sender_address).emit_transfer(amount, on="finalized")

    @gl.public.view
    def get_agreement(self, agreement_id: gl.u256) -> dict[str, typing.Any]:
        idx = self._valid_id(agreement_id)
        return {
            "id": agreement_id,
            "state": self.states[idx],
            "outcome_type": self.outcome_types[idx],
            "proposition": self.propositions[idx],
            "subject": self.subjects[idx],
            "category": self.categories[idx],
            "organizer": self.organizers[idx],
            "event_id": self.event_ids[idx],
            "position": self.positions[idx],
            "stake": self.stakes[idx],
            "creator": self.creators[idx],
            "counterparty": self.counterparties[idx],
            "evidence_count": self.evidence_counts[idx],
            "resolution": self.resolution_outcomes[idx],
        }

    @gl.public.view
    def get_agreement_count(self) -> gl.u256:
        return self.agreement_count

    @gl.public.view
    def get_evidence(self, evidence_id: gl.u256) -> dict[str, typing.Any]:
        idx = int(evidence_id)
        if idx < 0 or idx >= len(self.evidence_urls):
            raise gl.vm.UserError("unknown evidence")
        return {
            "id": evidence_id,
            "agreement_id": self.evidence_agreements[idx],
            "url": self.evidence_urls[idx],
            "mode": "text",
            "text": self.evidence_text[idx],
            "length": gl.u256(len(self.evidence_text[idx])),
            "fingerprint": self.evidence_fingerprints[idx],
            "frozen_at": self.evidence_frozen_at[idx],
        }

    @gl.public.view
    def get_withdrawable(self, account: gl.Address) -> gl.u256:
        return self.owed.get(account, gl.u256(0))
