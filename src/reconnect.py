"""VM replacement reconnect checklist — shell / facade only.

No real credentials, no real account names, no network calls.
The verify and load functions are stubs; the pure functions
(sort, grade, report) are real and tested.
"""
from __future__ import annotations

from dataclasses import dataclass, field

GRADES = ("P0", "P1", "P2", "P3", "P4")
METHODS = ("connect-link", "rebuild-at-console", "reuse-bound-key", "do-not-connect")
VERIFY_KINDS = ("status", "models", "pong", "none")


@dataclass
class AccountItem:
    name: str
    grade: str = "P1"
    kind: str = "api-key"  # oauth | api-key | system-token | ssh-key
    method: str = "rebuild-at-console"
    verify: str = "status"
    status: str = "pending"  # pending | verified | blocked | skipped


def sort_by_grade(items: list[AccountItem]) -> list[AccountItem]:
    """Reconnect order: P0 first, P4 last. Pure function, no I/O.

    Raises ValueError on an unknown grade instead of silently
    mis-ordering it. Does not mutate the input list.
    """
    unknown = [i.grade for i in items if i.grade not in GRADES]
    if unknown:
        raise ValueError(f"bad grade: {unknown[0]!r}")
    return sorted(items, key=lambda i: GRADES.index(i.grade))


def grade_order(items: list[AccountItem]) -> list[AccountItem]:
    """Migration-day order is grade order; P4 is never first."""
    return sort_by_grade(items)


def is_blocked(status_code: int | None = None, error_kind: str = "") -> bool:
    """Separate 'fetch did not reach the provider' from 'provider said no'.

    Takes structured inputs only — an HTTP status code and a short
    error kind — never free-form text. A sandbox / permission error
    when fetching a credential (status 403, or kind "sandbox" /
    "permission") is a fetch failure, not proof the key is dead.
    A 401 (provider said no) is not blocked.
    """
    if status_code == 403:
        return True
    return error_kind.strip().lower() in {"sandbox", "permission"}


def load_checklist(path: str) -> list[AccountItem]:
    """Load graded items from a checklist file. Stub."""
    raise NotImplementedError("Implement load_checklist(); never read values from the checklist file.")


def verify_item(item: AccountItem) -> str:
    """One read-only verification for one item. Stub.

    Must be read-only: list models, pong, or status only. Never
    writes, never spends, never re-registers an account.
    """
    raise NotImplementedError("Implement verify_item(); return verified, blocked or skipped.")


def report(items: list[AccountItem]) -> dict:
    """Summary: how many verified, blocked, skipped, pending, by grade."""
    out = {"verified": 0, "blocked": 0, "skipped": 0, "pending": 0, "by_grade": {}}
    for item in items:
        out[item.status] = out.get(item.status, 0) + 1
        out["by_grade"].setdefault(item.grade, 0)
        out["by_grade"][item.grade] += 1
    return out


if __name__ == "__main__":
    print("vm-reconnect-checklist shell: restore -> grade -> verify -> report")
