# vm-reconnect-checklist

A shell / facade for reconnecting accounts after a VM is replaced —
distilled from rebuilding a whole working setup from a self-backup,
more than once, in one night.

This repository is only the shell: architecture, config shape and
interfaces. No passwords, no API keys, no tokens, no account ids,
no real account names. Values are never written in the checklist.

## Where the idea comes from

- A VM replacement does not keep the credential vault. The accounts
  survive; the stored logins do not. A missing credential is not a
  missing account — treat the two differently, or you will re-register
  accounts that already exist.
- Reconnect in grades, not in the order you remember them. P0 is
  what you use every day, P1 is model lanes, P2 is daily check-in
  stations, P3 is cloud machines, P4 is do-not-connect-yet. On
  migration day, do P0 and P1 only; connect the rest when you need
  them.
- The only original for a key lives outside the backup: in the
  owner's password manager, or at the provider console where a new
  one can be generated. A key that is lost is rebuilt, never hunted
  for in old files.
- Verify each item once with a read-only check (list models, pong,
  status) and tick it off. If it fails, check the do-not-connect
  list first — do not re-enter the same key five times.
- A sandbox or permission error (for example a 403 when fetching a
  credential) does not prove the key is dead. It proves the fetch
  did not reach the provider. Re-verify through the proper
  secure-entry flow before declaring anything dead.

## Architecture

```
config.example.yaml   graded items (placeholders only)
src/reconnect.py      grading, sorting, verify and report interfaces
```

Flow: `restore backup -> read checklist -> reconnect P0 -> verify
each -> reconnect P1 -> verify each -> P2/P3 on demand, P4 never
on migration day -> report`.

## Config

Copy `config.example.yaml` to `config.yaml` and fill in your own
items. Never commit a real value. See the example file for the shape.

## Lessons baked into the interfaces

- `verify_item()` is read-only by design: it never writes, never
  spends, never re-registers.
- `sort_by_grade()` puts P0 first; `report()` shows what is verified,
  what is blocked, and what was deliberately skipped.
- `is_blocked()` separates "fetch did not reach the provider" from
  "provider said no", so a sandbox error never becomes a false
  "key is dead". It takes a structured status code and error kind,
  never free-form text, so an unrelated message cannot be
  misclassified as blocked.

## What makes this different

Most backup tools back up files. This one is built around the
breakthrough that actually got a setup back after a replacement:
graded reconnection, not a flat list. The grade decides the order,
the verify step decides the tick, and the do-not-connect list
decides what not to waste time on. A flat checklist of fifty
accounts, worked top to bottom, is how a migration day is lost.

## License

MIT (see LICENSE)
