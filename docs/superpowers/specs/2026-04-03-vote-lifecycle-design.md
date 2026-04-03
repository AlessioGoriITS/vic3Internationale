# Internationale Vote Lifecycle — Design Spec
**Date:** 2026-04-03
**Subsystem:** 1 of 3 — Backend (implement first)

## Overview

A global variable system tracking one active vote at a time. A vote is a motion to replace a currently permanent law (value = 2) with a proposed challenger. Countries cast stances, prestige is tallied monthly, and after 6 months the side with higher total prestige wins.

---

## 1. Global Variables (Vote State)

| Variable | Type | Meaning |
|---|---|---|
| `intl_vote_active` | flag (present/absent) | 1 if a vote is ongoing |
| `intl_vote_law_current` | flag value | Key of the law being challenged |
| `intl_vote_law_proposed` | flag value | Key of the challenger law |
| `intl_vote_months_left` | integer | Countdown from 6 to 0 |
| `intl_vote_prestige_current` | integer | Running prestige total supporting current |
| `intl_vote_prestige_proposed` | integer | Running prestige total supporting proposed |
| `intl_vote_count_current` | integer | Count of countries supporting current |
| `intl_vote_count_proposed` | integer | Count of countries supporting proposed |

## 2. Per-Country Variables

| Variable | Value | Meaning |
|---|---|---|
| `intl_vote_stance` | 1 | Country supports current law |
| `intl_vote_stance` | 2 | Country supports proposed law |
| absent | — | Country abstains |

---

## 3. Scripted Triggers

**File:** `common/scripted_triggers/intl_vote_triggers.txt`

| Trigger | Params | Logic |
|---|---|---|
| `intl_vote_is_active` | none | `has_global_variable = intl_vote_active` |
| `intl_vote_can_start` | `CURRENT`, `PROPOSED` | No active vote AND `intl_law_permanently_enabled = { LAW = $CURRENT$ }` AND `$CURRENT$ != $PROPOSED$` |
| `intl_country_has_voted` | none | `has_variable = intl_vote_stance` |
| `intl_country_supports_current` | none | `has_variable = intl_vote_stance`, `var:intl_vote_stance = 1` |
| `intl_country_supports_proposed` | none | `has_variable = intl_vote_stance`, `var:intl_vote_stance = 2` |

---

## 4. Scripted Effects

**File:** `common/scripted_effects/intl_vote_effects.txt`

### `intl_start_vote = { CURRENT = <key> PROPOSED = <key> }`
- Guards: fails silently if `intl_vote_is_active`
- Sets all 8 global vote variables
- Fires `intl_vote_events.1` (vote started) to all Internationale countries

### `intl_update_vote_prestige`
- Resets the 4 count/prestige globals to 0
- Iterates all countries with `je_internationale` or `je_mp_faction_world`
- Adds their `prestige` to the appropriate side based on `intl_vote_stance`
- Called monthly by the leader country's on_action

### `intl_cast_vote = { SIDE = <1 or 2> }`
- Sets `intl_vote_stance = $SIDE$` on the calling country scope
- Immediately calls `intl_update_vote_prestige` (so GUI is current)

### `intl_resolve_vote`
- Compares `intl_vote_prestige_proposed` vs `intl_vote_prestige_current`
- **If proposed wins:** iterates all 25 law cases — sets proposed law to value 2, removes current law variable
- **If current wins:** no change to law variables
- Fires `intl_vote_events.2` or `intl_vote_events.3` to all Internationale countries
- Clears all 8 global vote variables and all per-country `intl_vote_stance` variables

### `intl_cancel_vote` (debug/admin)
- Clears all vote state without resolution

---

## 5. Notification Events

**File:** `events/intl_vote_events.txt`

| Event | Trigger | Content |
|---|---|---|
| `intl_vote_events.1` | Vote starts | "A motion has been raised at the Congress" — shows current vs proposed law |
| `intl_vote_events.2` | Vote ends, proposed wins | "The Congress has voted to adopt [proposed law]" |
| `intl_vote_events.3` | Vote ends, current law holds | "The Congress has rejected the motion — [current law] stands" |

All events: `type = country_event`, `popup = yes`, sent to all `je_internationale` / `je_mp_faction_world` countries.

---

## 6. Monthly Pulse Integration

**File:** `common/on_actions/intl_on_actions.txt` (modify)

Add `intl_vote_monthly_pulse_on_action` to `on_monthly_pulse_country`. It runs only on the country with `je_internationale` (the leader). Each month it:
1. Calls `intl_update_vote_prestige`
2. Decrements `intl_vote_months_left` by 1
3. If `intl_vote_months_left <= 0`, calls `intl_resolve_vote`

---

## 7. Resolution: All 25 Law Cases

The resolve effect must enumerate all 25 `flag:<key>` comparisons to set/remove the correct global variables. This is verbose but required since Vic3 cannot use flag variable values as substitution parameters.

---

## 8. Out of Scope

- GUI rendering (Subsystem 2)
- Character interaction to start a vote (Subsystem 3)
- AI vote stance logic
