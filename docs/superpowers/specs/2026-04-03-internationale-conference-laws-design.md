# Internationale Conference Law System — Design Spec
**Date:** 2026-04-03

## Overview

A global variable system to track ideological laws through two phases of the Internationale Conference: temporary candidacy during the conference, and permanent enablement after finalization. All 25 laws across 5 ideologies participate. Once finalized, a law is passable by **any country in the world** — the variables are global scope and require no country-level scoping.

---

## 1. Global Variables

One global variable per law: `intl_law_<law_key>` where `<law_key>` is the law's identifier **without** the `law_` prefix.

| Value | Meaning |
|---|---|
| absent / 0 | Law is not active |
| 1 | Law is a conference candidate (temporary, not yet passable) |
| 2 | Law is permanently enabled (passable by all countries) |

### All 25 variables

**Blanquist**
- `intl_law_blanquist_presidential_republic`
- `intl_law_blanquist_technocracy`
- `intl_law_blanquist_state_atheism`
- `intl_law_blanquist_bureaucracy`
- `intl_law_blanquist_economy`

**Anarchist**
- `intl_law_anarchist_council_republic`
- `intl_law_anarchist_anarchy`
- `intl_law_anarchist_bureaucracy`
- `intl_law_anarchist_economy`
- `intl_law_anarchist_multiculturalism`

**Marxist**
- `intl_law_marxist_council_republic`
- `intl_law_marxist_army`
- `intl_law_marxist_bureaucracy`
- `intl_law_marxist_economy`
- `intl_law_marxist_one_party_state`

**Mutualist**
- `intl_law_mutualist_council_republic`
- `intl_law_mutualist_armed_neutrality`
- `intl_law_mutualist_economy`
- `intl_law_mutualist_healthcare`
- `intl_law_mutualist_oligarchy`

**Syndicalist**
- `intl_law_syndicalist_council_republic`
- `intl_law_syndicalist_single_party`
- `intl_law_syndicalist_bureaucracy`
- `intl_law_syndicalist_economy`
- `intl_law_syndicalist_land_reform`

---

## 2. Scripted Triggers

**File:** `common/scripted_triggers/intl_conference_triggers.txt`

Two parameterized triggers using `$LAW$` (the law key without `law_` prefix).

### `intl_law_in_conference`
True when a law is a live conference candidate (value = 1). Used for GUI visibility and conference tracking. A law at value 2 is NOT considered "in conference" — it has graduated.

### `intl_law_permanently_enabled`
True when a law has been finalized (value >= 2). This is the gate used in each law's `can_enact` block.

**Call syntax:**
```pdx
intl_law_permanently_enabled = { LAW = blanquist_economy }
```

---

## 3. Scripted Effects

**File:** `common/scripted_effects/intl_conference_effects.txt`

### `intl_add_law_to_conference`
Sets the variable to 1. Skips silently if the law is already permanently enabled (value = 2) — a finalized law cannot be demoted back to candidate status.

### `intl_remove_law_from_conference`
Removes the global variable (clears the law from conference). Skips silently if the law is permanently enabled — permanent laws cannot be removed.

### `finalize_internationale_conference`
**STUB.** Intended future behavior: iterate all laws with value = 1, select exactly 5 (by voting/faction weight logic to be designed), set those to value 2, remove the rest. No implementation until the voting system is designed.

**Call syntax:**
```pdx
intl_add_law_to_conference = { LAW = marxist_economy }
intl_remove_law_from_conference = { LAW = marxist_economy }
finalize_internationale_conference = yes
```

---

## 4. Law Integration

Each of the 25 laws in `common/laws/internationale_laws.txt` gets `intl_law_permanently_enabled` added to its `can_enact` block as the first condition. Existing conditions (technology unlocks, unlocking laws, etc.) are preserved beneath it.

**Example:**
```pdx
law_blanquist_presidential_republic = {
    ...
    can_enact = {
        intl_law_permanently_enabled = { LAW = blanquist_presidential_republic }
        # existing conditions follow
    }
    ...
}
```

Because `has_global_variable` and `global_var:` work from any scope in Victoria 3, this condition is country-agnostic — any country in the world can enact the law once it is finalized at the conference.

---

## 5. New Files

| File | Purpose |
|---|---|
| `common/scripted_triggers/intl_conference_triggers.txt` | New file — 2 parameterized triggers |
| `common/scripted_effects/intl_conference_effects.txt` | New file — 3 effects (2 active + 1 stub) |
| `common/laws/internationale_laws.txt` | Modified — `can_enact` updated in all 25 laws |

---

## 6. Out of Scope

- Finalization/voting logic (future system)
- GUI bindings (to be built against these variables later)
- AI behaviour for conference laws
