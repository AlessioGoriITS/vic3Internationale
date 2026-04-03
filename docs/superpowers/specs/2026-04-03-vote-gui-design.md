# Internationale Vote GUI — Design Spec
**Date:** 2026-04-03
**Subsystem:** 2 of 3 — GUI (implement after vote lifecycle)
**Depends on:** vote-lifecycle-design.md

## Overview

Extends the existing `internationale_gui.gui` window with two new screens:
1. **Neutral "Current Motion" screen** — shown when no faction tab is active, displays vote state or "no active motion"
2. **Active vote interface** — left vs right layout with prestige bar, visible when `intl_vote_active` is set

---

## 1. Navigation Change

The existing faction tab row (Anarchist, Mutualist, Syndicalist, Blanquist, Marxist) gets a sixth button: **"Current Motion"** (leftmost or rightmost, TBD by feel).

- Clicking it clears all `intl_tab_*` VariableSystem flags
- When no `intl_tab_*` flag is set, the neutral screen is visible
- The neutral screen replaces the delegate detail area (below the parliament graph)

---

## 2. Neutral Screen (No Active Vote)

Visible when: `NOT GetVariableSystem.Exists('intl_tab_*')` AND `NOT GetGlobalVariable('intl_vote_active').IsSet`

Content:
- Label: "No current motion before the Congress"
- Subtext: "A motion can be raised through a delegate interaction"

---

## 3. Neutral Screen (Active Vote — Summary)

Visible when: `NOT GetVariableSystem.Exists('intl_tab_*')` AND `GetGlobalVariable('intl_vote_active').IsSet`

Switches to the full voting interface (see section 4).

---

## 4. Active Vote Interface

Layout: three-column `hbox`

### Left Column — Current Law
- Law name (loc key from `intl_vote_law_current` flag)
- Ideology color strip
- Ideology leader portrait (from `ideologyleader_scope_gui` or equivalent stored scope)
- "Supports: [count]" — from `intl_vote_count_current`
- "Cast Vote: Keep" button — calls `intl_cast_vote = { SIDE = 1 }` on player country

### Center Column — Status
- "VS" separator
- Prestige bar: horizontal bar split by relative prestige shares
  - Left (current): width proportional to `intl_vote_prestige_current / total`
  - Right (proposed): width proportional to `intl_vote_prestige_proposed / total`
- Months remaining: `intl_vote_months_left`
- Total prestige numbers on each side

### Right Column — Proposed Law
- Mirror of left column
- Uses `intl_vote_law_proposed` flag
- "Cast Vote: Support" button — calls `intl_cast_vote = { SIDE = 2 }` on player country

---

## 5. Vote Button Logic

- "Cast Vote" buttons visible only if `NOT intl_country_has_voted` (player hasn't voted yet)
- After voting, buttons replaced with "You voted: [side]" label
- Player can change vote: buttons re-appear with "Change vote" label (same effect, overwrites `intl_vote_stance`)

---

## 6. Prestige Bar Implementation

Victoria 3 progress bars use `progressbar` widget. The bar fills from left.

Two overlapping `progressbar` widgets:
1. Bottom bar: full width, color = proposed law ideology color
2. Top bar: width = `intl_vote_prestige_current / (intl_vote_prestige_current + intl_vote_prestige_proposed)`, color = current law ideology color

Data binding uses `GetGlobalVariable` expressions in the `value` field.

---

## 7. Law Name / Ideology Display

Since law keys are stored as flag values in global variables, the GUI uses a scripted widget approach:
- `intl_vote_effects.txt` stores an additional integer variable per side: `intl_vote_ideology_current` and `intl_vote_ideology_proposed` (1=anarchist, 2=mutualist, 3=syndicalist, 4=blanquist, 5=marxist)
- These drive ideology-colored borders and portraits
- Law name is stored in a separate variable: `intl_vote_lawname_current` and `intl_vote_lawname_proposed` using `set_variable = { name = ... value = flag:<lawname_loc_key> }` for custom localization lookup

---

## 8. Files to Create/Modify

| Action | File |
|---|---|
| Modify | `gui/internationale_gui.gui` — add "Current Motion" tab, neutral screen, vote interface |
| Create | `gui/scripted_widgets/intl_vote_widgets.txt` — prestige bar widget, vote column widget |

---

## 9. Out of Scope

- Vote lifecycle logic (Subsystem 1)
- Character interaction (Subsystem 3)
- Localization strings (add to existing loc files)
