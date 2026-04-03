# Vote Character Interaction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a character interaction on the 5 Internationale delegates that lets a player raise a motion (start a vote) by selecting a current law to challenge and a proposed challenger.

**Architecture:** A single character interaction `intl_raise_motion` opens a two-step event chain: the interaction triggers a selection event on the player's country, the selection event presents available vote pairs as options, and the chosen option calls `intl_start_vote`.

**Tech Stack:** Victoria 3 Paradox scripting. Character interactions + country events.

**Read first:** `docs/superpowers/specs/2026-04-03-vote-character-interaction-design.md`

**Prerequisites:** Both vote-lifecycle and vote-gui plans must be implemented first.

---

## File Map

| Action | Path |
|---|---|
| Create | `common/character_interactions/intl_raise_motion.txt` |
| Modify | `events/intl_vote_events.txt` — add events 10–20 (selection + pairs) |
| Modify | `localization/english/intl_vote_l_english.yml` |

---

## Task 1: Character Interaction Definition

**Files:**
- Create: `common/character_interactions/intl_raise_motion.txt`

- [ ] **Step 1: Create the file**

```pdx
intl_raise_motion = {
	category = interaction_category_friendly

	icon = "gfx/interface/icons/event_icons/waving_flag.dds"

	is_shown = {
		OR = {
			target = { has_variable = bakunin_var }
			target = { has_variable = proudhon_var }
			target = { has_variable = bel_de_paepe_var }
			target = { has_variable = blanqui_var }
			target = { has_variable = karl_marx_var }
		}
		scope:actor = {
			OR = {
				has_journal_entry = je_internationale
				has_journal_entry = je_mp_faction_world
			}
		}
	}

	is_valid = {
		scope:actor = {
			NOT = { intl_vote_is_active = yes }
			NOT = { has_variable = intl_motion_cooldown_months }
		}
		# At least one law is permanently enabled (there is something to challenge)
		OR = {
			has_global_variable = intl_vote_active  # already checked NOT above — this is a fallback
			# True if any intl_law_* is at value 2
			global_var:intl_law_blanquist_presidential_republic >= 2
			global_var:intl_law_blanquist_technocracy >= 2
			global_var:intl_law_blanquist_state_atheism >= 2
			global_var:intl_law_blanquist_bureaucracy >= 2
			global_var:intl_law_blanquist_economy >= 2
			global_var:intl_law_anarchist_council_republic >= 2
			global_var:intl_law_anarchist_anarchy >= 2
			global_var:intl_law_anarchist_bureaucracy >= 2
			global_var:intl_law_anarchist_economy >= 2
			global_var:intl_law_anarchist_multiculturalism >= 2
			global_var:intl_law_marxist_council_republic >= 2
			global_var:intl_law_marxist_army >= 2
			global_var:intl_law_marxist_bureaucracy >= 2
			global_var:intl_law_marxist_economy >= 2
			global_var:intl_law_marxist_one_party_state >= 2
			global_var:intl_law_mutualist_council_republic >= 2
			global_var:intl_law_mutualist_armed_neutrality >= 2
			global_var:intl_law_mutualist_economy >= 2
			global_var:intl_law_mutualist_healthcare >= 2
			global_var:intl_law_mutualist_oligarchy >= 2
			global_var:intl_law_syndicalist_council_republic >= 2
			global_var:intl_law_syndicalist_single_party >= 2
			global_var:intl_law_syndicalist_bureaucracy >= 2
			global_var:intl_law_syndicalist_economy >= 2
			global_var:intl_law_syndicalist_land_reform >= 2
		}
	}

	effect = {
		scope:actor = {
			trigger_event = { id = intl_vote_events.10 popup = yes }
		}
	}

	localization = {
		INTERACTION_NAME = intl_raise_motion_name
		INTERACTION_DESC = intl_raise_motion_desc
		INTERACTION_TOOLTIP = intl_raise_motion_tt
	}
}
```

- [ ] **Step 2: Add loc keys**

```yaml
  intl_raise_motion_name: "Raise a Motion"
  intl_raise_motion_desc: "Call upon the Congress to vote on a new law."
  intl_raise_motion_tt: "Start a vote to replace an existing Congress law with a new one."
```

- [ ] **Step 3: Verify**

Load game, find a delegate character (Bakunin, Marx, etc.), open interactions. "Raise a Motion" should appear. Clicking should fire `intl_vote_events.10`.

- [ ] **Step 4: Commit**

```bash
git add common/character_interactions/intl_raise_motion.txt localization/english/intl_vote_l_english.yml
git commit -m "feat: add intl_raise_motion character interaction"
```

---

## Task 2: Law Pair Selection Event

**Files:**
- Modify: `events/intl_vote_events.txt`

This event presents all valid vote pairs. Each option corresponds to replacing one permanently enabled law with a different law from the same law group.

> **Design note:** There are 5 law groups: governance_principles, distribution_of_power, economic_system, bureaucracy, citizenship/army/health (varies). For each group, the event shows one option per ideology whose law in that group is currently permanent (value=2), proposing to replace it with each other ideology's law in that group. This can produce many options — limit displayed options to the most relevant (same-group challengers only).

- [ ] **Step 1: Append event 10 to `events/intl_vote_events.txt`**

```pdx
# Motion selection event — fired on actor country when raising a motion
# Shows all valid current-vs-proposed pairs for laws at value = 2
intl_vote_events.10 = {
	type = country_event
	placement = ROOT

	title = intl_vote_events.10.t
	desc = intl_vote_events.10.d

	icon = "gfx/interface/icons/event_icons/waving_flag.dds"
	event_image = { video = "gfx/event_pictures/unspecific_ruler_speaking_to_people.bk2" }

	### GOVERNANCE — challenge existing governance law with each ideology's alternative
	# Anarchist council_republic currently enabled — challenge it
	option = {
		name = intl_vote_events.10.propose_marxist_council_republic
		visible = {
			intl_law_permanently_enabled = { LAW = anarchist_council_republic }
			NOT = { intl_law_permanently_enabled = { LAW = marxist_council_republic } }
		}
		intl_start_vote = { CURRENT = anarchist_council_republic PROPOSED = marxist_council_republic }
	}
	option = {
		name = intl_vote_events.10.propose_mutualist_council_republic
		visible = {
			intl_law_permanently_enabled = { LAW = anarchist_council_republic }
			NOT = { intl_law_permanently_enabled = { LAW = mutualist_council_republic } }
		}
		intl_start_vote = { CURRENT = anarchist_council_republic PROPOSED = mutualist_council_republic }
	}
	option = {
		name = intl_vote_events.10.propose_syndicalist_council_republic
		visible = {
			intl_law_permanently_enabled = { LAW = anarchist_council_republic }
			NOT = { intl_law_permanently_enabled = { LAW = syndicalist_council_republic } }
		}
		intl_start_vote = { CURRENT = anarchist_council_republic PROPOSED = syndicalist_council_republic }
	}
	option = {
		name = intl_vote_events.10.propose_blanquist_presidential_republic
		visible = {
			intl_law_permanently_enabled = { LAW = anarchist_council_republic }
			NOT = { intl_law_permanently_enabled = { LAW = blanquist_presidential_republic } }
		}
		intl_start_vote = { CURRENT = anarchist_council_republic PROPOSED = blanquist_presidential_republic }
	}

	### (Repeat above pattern for each currently-enabled governance, economy, power, bureaucracy law)
	### See full matrix below — add one option block per valid CURRENT/PROPOSED pair.
	### Only show option if CURRENT is at value=2 and PROPOSED is NOT at value=2.

	### ECONOMY — challenge existing economy law
	option = {
		name = intl_vote_events.10.propose_marxist_economy
		visible = {
			intl_law_permanently_enabled = { LAW = mutualist_economy }
			NOT = { intl_law_permanently_enabled = { LAW = marxist_economy } }
		}
		intl_start_vote = { CURRENT = mutualist_economy PROPOSED = marxist_economy }
	}
	option = {
		name = intl_vote_events.10.propose_anarchist_economy
		visible = {
			intl_law_permanently_enabled = { LAW = mutualist_economy }
			NOT = { intl_law_permanently_enabled = { LAW = anarchist_economy } }
		}
		intl_start_vote = { CURRENT = mutualist_economy PROPOSED = anarchist_economy }
	}
	# ... continue for all economy law pairs ...

	### CANCEL option (always visible)
	option = {
		name = intl_vote_events.10.cancel
		default_option = yes
	}
}
```

> **Implementer note:** The full option matrix covers every valid pair across all 5 law groups. There are up to ~20 meaningful pairs. Follow the pattern above: one option per (CURRENT, PROPOSED) combination where CURRENT is at value=2 and PROPOSED is not. Each option has a `visible` block checking those conditions.

> The `## script_parameter` annotation issue from prior work (CW262) will appear on the `intl_law_permanently_enabled` calls in `visible` blocks. These are harmless false positives — the game engine handles them correctly.

- [ ] **Step 2: Add loc keys for all options**

```yaml
  intl_vote_events.10.t: "Raise a Motion"
  intl_vote_events.10.d: "Which law shall be brought before the Congress for a vote?"
  intl_vote_events.10.propose_marxist_council_republic: "Propose Marxist Council Republic"
  intl_vote_events.10.propose_mutualist_council_republic: "Propose Mutualist Council Republic"
  intl_vote_events.10.propose_syndicalist_council_republic: "Propose Syndicalist Council Republic"
  intl_vote_events.10.propose_blanquist_presidential_republic: "Propose Blanquist Presidential Republic"
  intl_vote_events.10.propose_marxist_economy: "Propose Marxist Planned Economy"
  intl_vote_events.10.propose_anarchist_economy: "Propose Anarchist Cooperative Economy"
  intl_vote_events.10.cancel: "Withdraw — raise no motion"
  # Add one entry per option
```

- [ ] **Step 3: Verify**

Load game. Fire the interaction on a delegate. `intl_vote_events.10` should open. Options should show/hide based on which laws are at value=2. Selecting an option should set `intl_vote_active`.

- [ ] **Step 4: Commit**

```bash
git add events/intl_vote_events.txt localization/english/intl_vote_l_english.yml
git commit -m "feat: add motion selection event (intl_vote_events.10) with governance and economy pairs"
```

---

## Task 3: Post-Vote Cooldown

**Files:**
- Modify: `common/scripted_effects/intl_vote_effects.txt`
- Modify: `common/on_actions/intl_on_actions.txt`

- [ ] **Step 1: Add cooldown set in `intl_resolve_vote`**

At the end of `intl_resolve_vote` (just before `intl_cancel_vote`), add:

```pdx
# Set 3-month cooldown on all Internationale countries
every_country = {
	limit = {
		OR = {
			has_journal_entry = je_internationale
			has_journal_entry = je_mp_faction_world
		}
	}
	set_variable = { name = intl_motion_cooldown_months value = 3 }
}
```

- [ ] **Step 2: Add cooldown decrement in `intl_vote_monthly_pulse_on_action`**

Append to the monthly pulse effect (in `intl_on_actions.txt`):

```pdx
# Decrement cooldown on all countries
every_country = {
	limit = {
		has_variable = intl_motion_cooldown_months
	}
	change_variable = { name = intl_motion_cooldown_months add = -1 }
	if = {
		limit = { var:intl_motion_cooldown_months <= 0 }
		remove_variable = intl_motion_cooldown_months
	}
}
```

- [ ] **Step 3: Verify**

After a vote resolves, the "Raise a Motion" interaction should be unavailable for 3 months.

- [ ] **Step 4: Commit**

```bash
git add common/scripted_effects/intl_vote_effects.txt common/on_actions/intl_on_actions.txt
git commit -m "feat: add 3-month cooldown after vote resolves"
```
