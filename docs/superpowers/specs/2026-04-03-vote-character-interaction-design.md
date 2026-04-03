# Internationale Vote Character Interaction — Design Spec
**Date:** 2026-04-03
**Subsystem:** 3 of 3 — Character Interaction (implement last)
**Depends on:** vote-lifecycle-design.md

## Overview

Adds a Victoria 3 character interaction that allows players to trigger a vote through their Internationale delegate characters (leaders and agitators). The interaction selects which law to challenge and which law to propose, then calls `intl_start_vote`.

---

## 1. Eligible Characters

Interaction is available on characters that have any of:
- `has_variable = bakunin_var`
- `has_variable = proudhon_var`
- `has_variable = bel_de_paepe_var`
- `has_variable = blanqui_var`
- `has_variable = karl_marx_var`

These are the 5 Internationale delegate characters defined in the existing mod.

---

## 2. Interaction: `intl_raise_motion`

**File:** `common/character_interactions/intl_raise_motion.txt`

### Visibility
- Character is one of the 5 delegates (checked via their variables above)
- Player has `je_internationale` OR `je_mp_faction_world`

### Is Valid (can execute)
- `NOT intl_vote_is_active`
- There is at least one law at value = 2 in the same law group as the character's ideology's laws
- Player country has not already raised a motion this year (optional cooldown, TBD)

### Interaction Flow

Because Vic3 character interactions are single-step (no multi-step wizard), the selection of CURRENT and PROPOSED laws uses a two-event chain:

**Step 1 — `intl_raise_motion` interaction fires:**
- Sets a temporary country variable `intl_motion_initiator = <character_id>` 
- Triggers `intl_vote_events.10` (selection event) on the initiating country

**Step 2 — `intl_vote_events.10` (selection event):**
- `type = country_event`, `popup = yes`, visible only to initiating country
- Presents options: one option per available law pair (current vs proposed)
- Each option calls `intl_start_vote = { CURRENT = <key> PROPOSED = <key> }` and clears `intl_motion_initiator`

### Option Generation
Since there are 25 laws and the relevant vote pairs depend on what's currently at value = 2, the event pre-checks which laws are permanently enabled and only shows viable options. Each option corresponds to one proposed law (challenger) vs the current law in the same group.

---

## 3. Cooldown (Optional)

To prevent spamming, after a vote resolves, set `intl_motion_cooldown_months = 3` on the leader country. The `is_valid` block checks `NOT has_variable = intl_motion_cooldown_months`. The monthly pulse decrements and removes it.

---

## 4. Files

| Action | File |
|---|---|
| Create | `common/character_interactions/intl_raise_motion.txt` |
| Modify | `events/intl_vote_events.txt` — add event 10 (selection event) |

---

## 5. Out of Scope

- AI using this interaction
- Multiple simultaneous motions
- Non-delegate characters raising motions
