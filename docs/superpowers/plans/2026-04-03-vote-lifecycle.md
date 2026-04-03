# Vote Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the global vote state machine — start, monthly update, prestige tally, and resolution for the Internationale Conference voting system.

**Architecture:** Global variables track vote state. One parameterized `intl_start_vote` effect launches the vote. A monthly on_action (leader country only) counts down and resolves. Resolution iterates all 25 law cases since flag values cannot be used as substitution parameters.

**Tech Stack:** Victoria 3 Paradox scripting. Files in `vic3Internationale/`. No unit tests — verify via `error.log` on game load and console commands.

**Read first:** `docs/superpowers/specs/2026-04-03-vote-lifecycle-design.md`

---

## File Map

| Action | Path |
|---|---|
| Create | `common/scripted_triggers/intl_vote_triggers.txt` |
| Create | `common/scripted_effects/intl_vote_effects.txt` |
| Create | `events/intl_vote_events.txt` |
| Modify | `common/on_actions/intl_on_actions.txt` |

---

## Task 1: Scripted Triggers

**Files:**
- Create: `common/scripted_triggers/intl_vote_triggers.txt`

- [ ] **Step 1: Create the file**

```pdx
# Internationale Conference — Vote State Triggers

## script_parameter = CURRENT
## script_parameter = PROPOSED
intl_vote_can_start = {
	NOT = { has_global_variable = intl_vote_active }
	intl_law_permanently_enabled = { LAW = $CURRENT$ }
	NOT = { always = yes }    # placeholder: $CURRENT$ != $PROPOSED$ (always check caller)
}

intl_vote_is_active = {
	has_global_variable = intl_vote_active
}

intl_country_has_voted = {
	has_variable = intl_vote_stance
}

intl_country_supports_current = {
	has_variable = intl_vote_stance
	var:intl_vote_stance = 1
}

intl_country_supports_proposed = {
	has_variable = intl_vote_stance
	var:intl_vote_stance = 2
}
```

- [ ] **Step 2: Verify**

Load game, check `error.log` for `intl_vote_triggers`. No errors expected.

- [ ] **Step 3: Commit**

```bash
git add common/scripted_triggers/intl_vote_triggers.txt
git commit -m "feat: add intl_vote scripted triggers"
```

---

## Task 2: Notification Events

**Files:**
- Create: `events/intl_vote_events.txt`

- [ ] **Step 1: Create the file**

```pdx
namespace = intl_vote_events

# Vote started notification
intl_vote_events.1 = {
	type = country_event
	placement = ROOT

	title = intl_vote_events.1.t
	desc = intl_vote_events.1.d
	flavor = intl_vote_events.1.f

	event_image = { video = "gfx/event_pictures/unspecific_ruler_speaking_to_people.bk2" }

	icon = "gfx/interface/icons/event_icons/waving_flag.dds"

	duration = 3

	option = {
		name = intl_vote_events.1.a
		default_option = yes
	}
}

# Vote ended — proposed law wins
intl_vote_events.2 = {
	type = country_event
	placement = ROOT

	title = intl_vote_events.2.t
	desc = intl_vote_events.2.d
	flavor = intl_vote_events.2.f

	event_image = { video = "gfx/event_pictures/unspecific_ruler_speaking_to_people.bk2" }

	icon = "gfx/interface/icons/event_icons/waving_flag.dds"

	duration = 3

	option = {
		name = intl_vote_events.2.a
		default_option = yes
	}
}

# Vote ended — current law holds
intl_vote_events.3 = {
	type = country_event
	placement = ROOT

	title = intl_vote_events.3.t
	desc = intl_vote_events.3.d
	flavor = intl_vote_events.3.f

	event_image = { video = "gfx/event_pictures/unspecific_ruler_speaking_to_people.bk2" }

	icon = "gfx/interface/icons/event_icons/waving_flag.dds"

	duration = 3

	option = {
		name = intl_vote_events.3.a
		default_option = yes
	}
}
```

- [ ] **Step 2: Add localization stubs**

Add to `localization/english/intl_vote_l_english.yml` (create file if it doesn't exist):

```yaml
 l_english:
  intl_vote_events.1.t: "A Motion Before the Congress"
  intl_vote_events.1.d: "A delegate has raised a motion to challenge the current law. The Congress has six months to deliberate."
  intl_vote_events.1.f: "The workers of the world are watching."
  intl_vote_events.1.a: "Let the debate begin."
  intl_vote_events.2.t: "The Congress Has Spoken"
  intl_vote_events.2.d: "The motion has passed. The Congress adopts the new law."
  intl_vote_events.2.f: "A new chapter for the International."
  intl_vote_events.2.a: "So be it."
  intl_vote_events.3.t: "The Motion Has Failed"
  intl_vote_events.3.d: "The motion has been rejected. The current law stands."
  intl_vote_events.3.f: "The status quo holds."
  intl_vote_events.3.a: "Very well."
```

- [ ] **Step 3: Verify**

Load game, check `error.log` for `intl_vote_events`. No errors expected.

- [ ] **Step 4: Commit**

```bash
git add events/intl_vote_events.txt localization/english/intl_vote_l_english.yml
git commit -m "feat: add intl_vote notification events and localization stubs"
```

---

## Task 3: Core Vote Effects

**Files:**
- Create: `common/scripted_effects/intl_vote_effects.txt`

- [ ] **Step 1: Create the file with `intl_start_vote` and helpers**

```pdx
# Internationale Conference — Vote Effects

## script_parameter = CURRENT
## script_parameter = PROPOSED
intl_start_vote = {
	if = {
		limit = { has_global_variable = intl_vote_active }
		# Already active — no-op
	}
	else = {
		set_global_variable = intl_vote_active
		set_global_variable = { name = intl_vote_law_current value = flag:$CURRENT$ }
		set_global_variable = { name = intl_vote_law_proposed value = flag:$PROPOSED$ }
		set_global_variable = { name = intl_vote_months_left value = 6 }
		set_global_variable = { name = intl_vote_prestige_current value = 0 }
		set_global_variable = { name = intl_vote_prestige_proposed value = 0 }
		set_global_variable = { name = intl_vote_count_current value = 0 }
		set_global_variable = { name = intl_vote_count_proposed value = 0 }
		every_country = {
			limit = {
				OR = {
					has_journal_entry = je_internationale
					has_journal_entry = je_mp_faction_world
				}
			}
			trigger_event = { id = intl_vote_events.1 popup = yes }
		}
	}
}

## script_parameter = SIDE
intl_cast_vote = {
	set_variable = { name = intl_vote_stance value = $SIDE$ }
	intl_update_vote_prestige = yes
}

intl_update_vote_prestige = {
	set_global_variable = { name = intl_vote_prestige_current value = 0 }
	set_global_variable = { name = intl_vote_prestige_proposed value = 0 }
	set_global_variable = { name = intl_vote_count_current value = 0 }
	set_global_variable = { name = intl_vote_count_proposed value = 0 }
	every_country = {
		limit = {
			OR = {
				has_journal_entry = je_internationale
				has_journal_entry = je_mp_faction_world
			}
			has_variable = intl_vote_stance
		}
		if = {
			limit = { intl_country_supports_current = yes }
			change_global_variable = {
				name = intl_vote_prestige_current
				add = { value = prestige }
			}
			change_global_variable = { name = intl_vote_count_current add = 1 }
		}
		if = {
			limit = { intl_country_supports_proposed = yes }
			change_global_variable = {
				name = intl_vote_prestige_proposed
				add = { value = prestige }
			}
			change_global_variable = { name = intl_vote_count_proposed add = 1 }
		}
	}
}

intl_cancel_vote = {
	every_country = {
		limit = { has_variable = intl_vote_stance }
		remove_variable = intl_vote_stance
	}
	if = { limit = { has_global_variable = intl_vote_active } remove_global_variable = intl_vote_active }
	if = { limit = { has_global_variable = intl_vote_law_current } remove_global_variable = intl_vote_law_current }
	if = { limit = { has_global_variable = intl_vote_law_proposed } remove_global_variable = intl_vote_law_proposed }
	if = { limit = { has_global_variable = intl_vote_months_left } remove_global_variable = intl_vote_months_left }
	if = { limit = { has_global_variable = intl_vote_prestige_current } remove_global_variable = intl_vote_prestige_current }
	if = { limit = { has_global_variable = intl_vote_prestige_proposed } remove_global_variable = intl_vote_prestige_proposed }
	if = { limit = { has_global_variable = intl_vote_count_current } remove_global_variable = intl_vote_count_current }
	if = { limit = { has_global_variable = intl_vote_count_proposed } remove_global_variable = intl_vote_count_proposed }
}
```

- [ ] **Step 2: Verify syntax**

Load game, check `error.log` for `intl_vote_effects`. No errors expected.

- [ ] **Step 3: Commit**

```bash
git add common/scripted_effects/intl_vote_effects.txt
git commit -m "feat: add intl_start_vote, intl_cast_vote, intl_update_vote_prestige, intl_cancel_vote effects"
```

---

## Task 4: Resolution Effect (All 25 Law Cases)

**Files:**
- Modify: `common/scripted_effects/intl_vote_effects.txt`

- [ ] **Step 1: Append `intl_resolve_vote` to the effects file**

This effect is long because flag variable values cannot be used as substitution parameters — each of the 25 laws must be explicitly checked.

```pdx
intl_resolve_vote = {
	if = {
		limit = {
			global_var:intl_vote_prestige_proposed > global_var:intl_vote_prestige_current
		}

		### PROPOSED LAW WINS — set proposed to 2 ###

		# Blanquist
		if = { limit = { global_var:intl_vote_law_proposed = flag:blanquist_presidential_republic }
			set_global_variable = { name = intl_law_blanquist_presidential_republic value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:blanquist_technocracy }
			set_global_variable = { name = intl_law_blanquist_technocracy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:blanquist_state_atheism }
			set_global_variable = { name = intl_law_blanquist_state_atheism value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:blanquist_bureaucracy }
			set_global_variable = { name = intl_law_blanquist_bureaucracy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:blanquist_economy }
			set_global_variable = { name = intl_law_blanquist_economy value = 2 } }
		# Anarchist
		if = { limit = { global_var:intl_vote_law_proposed = flag:anarchist_council_republic }
			set_global_variable = { name = intl_law_anarchist_council_republic value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:anarchist_anarchy }
			set_global_variable = { name = intl_law_anarchist_anarchy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:anarchist_bureaucracy }
			set_global_variable = { name = intl_law_anarchist_bureaucracy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:anarchist_economy }
			set_global_variable = { name = intl_law_anarchist_economy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:anarchist_multiculturalism }
			set_global_variable = { name = intl_law_anarchist_multiculturalism value = 2 } }
		# Marxist
		if = { limit = { global_var:intl_vote_law_proposed = flag:marxist_council_republic }
			set_global_variable = { name = intl_law_marxist_council_republic value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:marxist_army }
			set_global_variable = { name = intl_law_marxist_army value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:marxist_bureaucracy }
			set_global_variable = { name = intl_law_marxist_bureaucracy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:marxist_economy }
			set_global_variable = { name = intl_law_marxist_economy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:marxist_one_party_state }
			set_global_variable = { name = intl_law_marxist_one_party_state value = 2 } }
		# Mutualist
		if = { limit = { global_var:intl_vote_law_proposed = flag:mutualist_council_republic }
			set_global_variable = { name = intl_law_mutualist_council_republic value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:mutualist_armed_neutrality }
			set_global_variable = { name = intl_law_mutualist_armed_neutrality value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:mutualist_economy }
			set_global_variable = { name = intl_law_mutualist_economy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:mutualist_healthcare }
			set_global_variable = { name = intl_law_mutualist_healthcare value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:mutualist_oligarchy }
			set_global_variable = { name = intl_law_mutualist_oligarchy value = 2 } }
		# Syndicalist
		if = { limit = { global_var:intl_vote_law_proposed = flag:syndicalist_council_republic }
			set_global_variable = { name = intl_law_syndicalist_council_republic value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:syndicalist_single_party }
			set_global_variable = { name = intl_law_syndicalist_single_party value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:syndicalist_bureaucracy }
			set_global_variable = { name = intl_law_syndicalist_bureaucracy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:syndicalist_economy }
			set_global_variable = { name = intl_law_syndicalist_economy value = 2 } }
		if = { limit = { global_var:intl_vote_law_proposed = flag:syndicalist_land_reform }
			set_global_variable = { name = intl_law_syndicalist_land_reform value = 2 } }

		### CURRENT LAW LOSES — remove its variable ###

		# Blanquist
		if = { limit = { global_var:intl_vote_law_current = flag:blanquist_presidential_republic
			has_global_variable = intl_law_blanquist_presidential_republic }
			remove_global_variable = intl_law_blanquist_presidential_republic }
		if = { limit = { global_var:intl_vote_law_current = flag:blanquist_technocracy
			has_global_variable = intl_law_blanquist_technocracy }
			remove_global_variable = intl_law_blanquist_technocracy }
		if = { limit = { global_var:intl_vote_law_current = flag:blanquist_state_atheism
			has_global_variable = intl_law_blanquist_state_atheism }
			remove_global_variable = intl_law_blanquist_state_atheism }
		if = { limit = { global_var:intl_vote_law_current = flag:blanquist_bureaucracy
			has_global_variable = intl_law_blanquist_bureaucracy }
			remove_global_variable = intl_law_blanquist_bureaucracy }
		if = { limit = { global_var:intl_vote_law_current = flag:blanquist_economy
			has_global_variable = intl_law_blanquist_economy }
			remove_global_variable = intl_law_blanquist_economy }
		# Anarchist
		if = { limit = { global_var:intl_vote_law_current = flag:anarchist_council_republic
			has_global_variable = intl_law_anarchist_council_republic }
			remove_global_variable = intl_law_anarchist_council_republic }
		if = { limit = { global_var:intl_vote_law_current = flag:anarchist_anarchy
			has_global_variable = intl_law_anarchist_anarchy }
			remove_global_variable = intl_law_anarchist_anarchy }
		if = { limit = { global_var:intl_vote_law_current = flag:anarchist_bureaucracy
			has_global_variable = intl_law_anarchist_bureaucracy }
			remove_global_variable = intl_law_anarchist_bureaucracy }
		if = { limit = { global_var:intl_vote_law_current = flag:anarchist_economy
			has_global_variable = intl_law_anarchist_economy }
			remove_global_variable = intl_law_anarchist_economy }
		if = { limit = { global_var:intl_vote_law_current = flag:anarchist_multiculturalism
			has_global_variable = intl_law_anarchist_multiculturalism }
			remove_global_variable = intl_law_anarchist_multiculturalism }
		# Marxist
		if = { limit = { global_var:intl_vote_law_current = flag:marxist_council_republic
			has_global_variable = intl_law_marxist_council_republic }
			remove_global_variable = intl_law_marxist_council_republic }
		if = { limit = { global_var:intl_vote_law_current = flag:marxist_army
			has_global_variable = intl_law_marxist_army }
			remove_global_variable = intl_law_marxist_army }
		if = { limit = { global_var:intl_vote_law_current = flag:marxist_bureaucracy
			has_global_variable = intl_law_marxist_bureaucracy }
			remove_global_variable = intl_law_marxist_bureaucracy }
		if = { limit = { global_var:intl_vote_law_current = flag:marxist_economy
			has_global_variable = intl_law_marxist_economy }
			remove_global_variable = intl_law_marxist_economy }
		if = { limit = { global_var:intl_vote_law_current = flag:marxist_one_party_state
			has_global_variable = intl_law_marxist_one_party_state }
			remove_global_variable = intl_law_marxist_one_party_state }
		# Mutualist
		if = { limit = { global_var:intl_vote_law_current = flag:mutualist_council_republic
			has_global_variable = intl_law_mutualist_council_republic }
			remove_global_variable = intl_law_mutualist_council_republic }
		if = { limit = { global_var:intl_vote_law_current = flag:mutualist_armed_neutrality
			has_global_variable = intl_law_mutualist_armed_neutrality }
			remove_global_variable = intl_law_mutualist_armed_neutrality }
		if = { limit = { global_var:intl_vote_law_current = flag:mutualist_economy
			has_global_variable = intl_law_mutualist_economy }
			remove_global_variable = intl_law_mutualist_economy }
		if = { limit = { global_var:intl_vote_law_current = flag:mutualist_healthcare
			has_global_variable = intl_law_mutualist_healthcare }
			remove_global_variable = intl_law_mutualist_healthcare }
		if = { limit = { global_var:intl_vote_law_current = flag:mutualist_oligarchy
			has_global_variable = intl_law_mutualist_oligarchy }
			remove_global_variable = intl_law_mutualist_oligarchy }
		# Syndicalist
		if = { limit = { global_var:intl_vote_law_current = flag:syndicalist_council_republic
			has_global_variable = intl_law_syndicalist_council_republic }
			remove_global_variable = intl_law_syndicalist_council_republic }
		if = { limit = { global_var:intl_vote_law_current = flag:syndicalist_single_party
			has_global_variable = intl_law_syndicalist_single_party }
			remove_global_variable = intl_law_syndicalist_single_party }
		if = { limit = { global_var:intl_vote_law_current = flag:syndicalist_bureaucracy
			has_global_variable = intl_law_syndicalist_bureaucracy }
			remove_global_variable = intl_law_syndicalist_bureaucracy }
		if = { limit = { global_var:intl_vote_law_current = flag:syndicalist_economy
			has_global_variable = intl_law_syndicalist_economy }
			remove_global_variable = intl_law_syndicalist_economy }
		if = { limit = { global_var:intl_vote_law_current = flag:syndicalist_land_reform
			has_global_variable = intl_law_syndicalist_land_reform }
			remove_global_variable = intl_law_syndicalist_land_reform }

		# Notify all — proposed wins
		every_country = {
			limit = {
				OR = {
					has_journal_entry = je_internationale
					has_journal_entry = je_mp_faction_world
				}
			}
			trigger_event = { id = intl_vote_events.2 popup = yes }
		}
	}
	else = {
		# Current law wins — no law variable changes
		every_country = {
			limit = {
				OR = {
					has_journal_entry = je_internationale
					has_journal_entry = je_mp_faction_world
				}
			}
			trigger_event = { id = intl_vote_events.3 popup = yes }
		}
	}

	# Clear all vote state
	intl_cancel_vote = yes
}
```

- [ ] **Step 2: Verify syntax**

Load game, check `error.log` for `intl_resolve_vote`. No errors expected.

- [ ] **Step 3: Smoke test via console**

In-game console (launch with `debugmode`):
```
# Start a test vote
effect intl_start_vote = { CURRENT = mutualist_economy PROPOSED = marxist_economy }

# Check variable was set
effect log = "[GetGlobalVariable('intl_vote_active').IsSet]"

# Cast vote for proposed
effect intl_cast_vote = { SIDE = 2 }

# Check prestige totals updated
effect log = "[GetGlobalVariable('intl_vote_prestige_proposed').GetValue(int32).ToString]"

# Resolve immediately
effect intl_resolve_vote = yes

# Confirm marxist_economy is now at 2
effect log = "[GetGlobalVariable('intl_law_marxist_economy').GetValue(int32).ToString]"
```

Expected: `intl_law_marxist_economy` = 2, `intl_law_mutualist_economy` absent.

- [ ] **Step 4: Commit**

```bash
git add common/scripted_effects/intl_vote_effects.txt
git commit -m "feat: add intl_resolve_vote with all 25 law cases"
```

---

## Task 5: Monthly Pulse Integration

**Files:**
- Modify: `common/on_actions/intl_on_actions.txt`

- [ ] **Step 1: Add to the on_actions file**

Append to the existing file (after the existing `intl_parliament_update_on_action`):

```pdx
on_monthly_pulse_country = {
	on_actions = {
		intl_vote_monthly_pulse_on_action
	}
}

intl_vote_monthly_pulse_on_action = {
	effect = {
		if = {
			limit = {
				is_player = yes
				has_journal_entry = je_internationale
				intl_vote_is_active = yes
			}
			intl_update_vote_prestige = yes
			change_global_variable = { name = intl_vote_months_left add = -1 }
			if = {
				limit = { global_var:intl_vote_months_left <= 0 }
				intl_resolve_vote = yes
			}
		}
	}
}
```

- [ ] **Step 2: Verify**

Load game, check `error.log`. No errors expected.

- [ ] **Step 3: Smoke test timer**

```
effect intl_start_vote = { CURRENT = mutualist_economy PROPOSED = marxist_economy }
# Fast-forward 7 months (or manually decrement)
effect change_global_variable = { name = intl_vote_months_left add = -6 }
# Next monthly pulse should trigger intl_resolve_vote
```

- [ ] **Step 4: Commit**

```bash
git add common/on_actions/intl_on_actions.txt
git commit -m "feat: add vote monthly pulse — countdown and auto-resolve at 0 months"
```
