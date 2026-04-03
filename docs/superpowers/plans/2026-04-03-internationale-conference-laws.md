# Internationale Conference Law System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a global variable system that tracks 25 ideological laws through conference candidacy (value=1) and permanent enablement (value=2), gating each law's `can_enact` on permanent enablement.

**Architecture:** Two new files (scripted triggers + scripted effects) using a single `$LAW$` parameter for full reusability. Each of the 25 laws in `internationale_laws.txt` gets `intl_law_permanently_enabled = { LAW = <key> }` inserted as the first condition in its `can_enact` block. All state lives in global variables so any country can check or enact without scope juggling.

**Tech Stack:** Victoria 3 Paradox scripting language. No external tools. Verification via game error log (`Documents/Paradox Interactive/Victoria 3/logs/error.log`) and in-game console.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `common/scripted_triggers/intl_conference_triggers.txt` | 2 parameterized triggers: `intl_law_in_conference`, `intl_law_permanently_enabled` |
| Create | `common/scripted_effects/intl_conference_effects.txt` | 3 effects: `intl_add_law_to_conference`, `intl_remove_law_from_conference`, `finalize_internationale_conference` (stub) |
| Modify | `common/laws/internationale_laws.txt` | Add conference gate to `can_enact` in all 25 laws |

All paths are relative to `vic3Internationale/`.

---

## Task 1: Create Scripted Triggers

**Files:**
- Create: `common/scripted_triggers/intl_conference_triggers.txt`

- [ ] **Step 1: Create the file**

```pdx
# Internationale Conference — Law State Triggers
# $LAW$ = law key without the "law_" prefix
# e.g. intl_law_in_conference = { LAW = blanquist_economy }

# True when a law is a live conference candidate (value = 1, not yet finalized)
intl_law_in_conference = {
	has_global_variable = intl_law_$LAW$
	global_var:intl_law_$LAW$ >= 1
	global_var:intl_law_$LAW$ < 2
}

# True when a law has been permanently enabled by the conference (value >= 2)
# This is the gate used in each law's can_enact block
intl_law_permanently_enabled = {
	has_global_variable = intl_law_$LAW$
	global_var:intl_law_$LAW$ >= 2
}
```

- [ ] **Step 2: Verify syntax**

Launch the game, load any save, then check:
`Documents/Paradox Interactive/Victoria 3/logs/error.log`

Search for `intl_conference_triggers`. No errors should appear. If you see `unknown trigger`, the file path is wrong — confirm it is inside `vic3Internationale/common/scripted_triggers/`.

- [ ] **Step 3: Commit**

```bash
git add common/scripted_triggers/intl_conference_triggers.txt
git commit -m "feat: add intl_law_in_conference and intl_law_permanently_enabled scripted triggers"
```

---

## Task 2: Create Scripted Effects

**Files:**
- Create: `common/scripted_effects/intl_conference_effects.txt`

- [ ] **Step 1: Create the file**

```pdx
# Internationale Conference — Law State Effects
# $LAW$ = law key without the "law_" prefix
# e.g. intl_add_law_to_conference = { LAW = blanquist_economy }

# Set law to conference candidate (value = 1)
# No-op if already permanently enabled (value = 2) — permanent laws cannot be demoted
intl_add_law_to_conference = {
	if = {
		limit = {
			NOT = { intl_law_permanently_enabled = { LAW = $LAW$ } }
		}
		set_global_variable = { name = intl_law_$LAW$ value = 1 }
	}
}

# Remove law from conference (clears the global variable)
# No-op if permanently enabled — permanent laws cannot be removed
intl_remove_law_from_conference = {
	if = {
		limit = {
			has_global_variable = intl_law_$LAW$
			global_var:intl_law_$LAW$ < 2
		}
		remove_global_variable = intl_law_$LAW$
	}
}

# STUB — voting and selection system to be implemented later
# Intended: iterate all laws with value = 1, select exactly 5 by faction vote weight,
# set those to value = 2, remove_global_variable for all others
finalize_internationale_conference = {
}
```

- [ ] **Step 2: Verify syntax**

Launch game, check `error.log` for `intl_conference_effects`. No errors should appear.

- [ ] **Step 3: Commit**

```bash
git add common/scripted_effects/intl_conference_effects.txt
git commit -m "feat: add intl_add_law_to_conference, intl_remove_law_from_conference, finalize stub effects"
```

---

## Task 3: Gate Blanquist Laws

**Files:**
- Modify: `common/laws/internationale_laws.txt`

Five laws: `blanquist_presidential_republic`, `blanquist_technocracy`, `blanquist_state_atheism`, `blanquist_bureaucracy`, `blanquist_economy`.

- [ ] **Step 1: `law_blanquist_presidential_republic` — replace empty `can_enact`**

Find (line 22):
```pdx
	can_enact = {
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = blanquist_presidential_republic }
	}
```

- [ ] **Step 2: `law_blanquist_technocracy` — replace empty `can_enact`**

Find (line 71):
```pdx
	can_enact = {
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = blanquist_technocracy }
	}
```

- [ ] **Step 3: `law_blanquist_state_atheism` — prepend to existing `can_enact`**

Find (line 126):
```pdx
	can_enact = {
		ig:ig_devout ?= {
			is_in_government = no
		}
		OR = {
			is_power_bloc_leader = no
			power_bloc ?= {
				NOT = { has_identity = identity:identity_religious }
			}
		}
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = blanquist_state_atheism }
		ig:ig_devout ?= {
			is_in_government = no
		}
		OR = {
			is_power_bloc_leader = no
			power_bloc ?= {
				NOT = { has_identity = identity:identity_religious }
			}
		}
	}
```

- [ ] **Step 4: `law_blanquist_bureaucracy` — add `can_enact` block (none exists)**

Find (line 200) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert the new block immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = blanquist_bureaucracy }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 5: `law_blanquist_economy` — prepend to existing `can_enact`**

Find (line 241):
```pdx
	can_enact = {
		OR = {
			has_law_or_variant = law_type:law_single_party_state
			has_law_or_variant = law_type:law_technocracy
			has_law_or_variant = law_type:law_state_atheism
		}
		
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = blanquist_economy }
		OR = {
			has_law_or_variant = law_type:law_single_party_state
			has_law_or_variant = law_type:law_technocracy
			has_law_or_variant = law_type:law_state_atheism
		}
	}
```

- [ ] **Step 6: Verify syntax**

Check `error.log` for any errors referencing `blanquist` laws.

- [ ] **Step 7: Commit**

```bash
git add common/laws/internationale_laws.txt
git commit -m "feat: gate blanquist laws on intl_law_permanently_enabled"
```

---

## Task 4: Gate Anarchist Laws

**Files:**
- Modify: `common/laws/internationale_laws.txt`

Five laws: `anarchist_council_republic`, `anarchist_anarchy`, `anarchist_bureaucracy`, `anarchist_economy`, `anarchist_multiculturalism`.

- [ ] **Step 1: `law_anarchist_council_republic` — prepend to existing `can_enact`**

Find (line 291):
```pdx
	can_enact = {
		NOT = { has_government_type = gov_chartered_company }
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = anarchist_council_republic }
		NOT = { has_government_type = gov_chartered_company }
	}
```

- [ ] **Step 2: `law_anarchist_anarchy` — prepend to existing `can_enact`**

Find (line 333):
```pdx
	can_enact = {
		has_law_or_variant = law_type:law_council_republic
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = anarchist_anarchy }
		has_law_or_variant = law_type:law_council_republic
	}
```

- [ ] **Step 3: `law_anarchist_bureaucracy` — add `can_enact` block (none exists)**

Find (line 376) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = anarchist_bureaucracy }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 4: `law_anarchist_economy` — prepend to existing `can_enact`**

Find (line 417):
```pdx
	can_enact = {
		has_law_or_variant = law_type:law_council_republic
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = anarchist_economy }
		has_law_or_variant = law_type:law_council_republic
	}
```

- [ ] **Step 5: `law_anarchist_multiculturalism` — prepend to existing `can_enact`**

Find (line 483):
```pdx
	can_enact = {
		has_law_or_variant = law_type:law_council_republic
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = anarchist_multiculturalism }
		has_law_or_variant = law_type:law_council_republic
	}
```

- [ ] **Step 6: Verify syntax**

Check `error.log` for any errors referencing `anarchist` laws.

- [ ] **Step 7: Commit**

```bash
git add common/laws/internationale_laws.txt
git commit -m "feat: gate anarchist laws on intl_law_permanently_enabled"
```

---

## Task 5: Gate Marxist Laws

**Files:**
- Modify: `common/laws/internationale_laws.txt`

Five laws: `marxist_council_republic`, `marxist_army`, `marxist_bureaucracy`, `marxist_economy`, `marxist_one_party_state`.

- [ ] **Step 1: `law_marxist_council_republic` — prepend to existing `can_enact`**

Find (line 532):
```pdx
	can_enact = {
		NOT = { has_government_type = gov_chartered_company }
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = marxist_council_republic }
		NOT = { has_government_type = gov_chartered_company }
	}
```

- [ ] **Step 2: `law_marxist_army` — prepend to existing `can_enact`**

Find (line 568):
```pdx
	can_enact = {
		has_law_or_variant = law_type:law_council_republic
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = marxist_army }
		has_law_or_variant = law_type:law_council_republic
	}
```

- [ ] **Step 3: `law_marxist_bureaucracy` — add `can_enact` block (none exists)**

Find (line 604) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = marxist_bureaucracy }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 4: `law_marxist_economy` — prepend to existing `can_enact`**

Find (line 644):
```pdx
	can_enact = {
		has_law_or_variant = law_type:law_council_republic
		OR = {
			has_law_or_variant = law_type:law_single_party_state
			has_law_or_variant = law_type:law_autocracy
			has_law_or_variant = law_type:law_oligarchy
			has_law_or_variant = law_type:law_technocracy
		}
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = marxist_economy }
		has_law_or_variant = law_type:law_council_republic
		OR = {
			has_law_or_variant = law_type:law_single_party_state
			has_law_or_variant = law_type:law_autocracy
			has_law_or_variant = law_type:law_oligarchy
			has_law_or_variant = law_type:law_technocracy
		}
	}
```

- [ ] **Step 5: `law_marxist_one_party_state` — prepend to existing `can_enact`**

Find (line 704):
```pdx
	can_enact = {
		OR = {
			ig:ig_trade_unions ?= {
					has_party = yes
				}
			custom_tooltip = {
				text = sps_no_party_tt
				country_has_voting_franchise = no
			}
		}
		trigger_if = {
			limit = {
				c:BIC ?= ROOT
				is_subject = yes
				NOT = { has_law = scope:law }
			}
			custom_tooltip = {
				text = BIC_not_able_to_change_distribution_of_power_tt
				has_variable = britain_granted_dop_permission
			}
		}
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = marxist_one_party_state }
		OR = {
			ig:ig_trade_unions ?= {
					has_party = yes
				}
			custom_tooltip = {
				text = sps_no_party_tt
				country_has_voting_franchise = no
			}
		}
		trigger_if = {
			limit = {
				c:BIC ?= ROOT
				is_subject = yes
				NOT = { has_law = scope:law }
			}
			custom_tooltip = {
				text = BIC_not_able_to_change_distribution_of_power_tt
				has_variable = britain_granted_dop_permission
			}
		}
	}
```

- [ ] **Step 6: Verify syntax**

Check `error.log` for any errors referencing `marxist` laws.

- [ ] **Step 7: Commit**

```bash
git add common/laws/internationale_laws.txt
git commit -m "feat: gate marxist laws on intl_law_permanently_enabled"
```

---

## Task 6: Gate Mutualist Laws

**Files:**
- Modify: `common/laws/internationale_laws.txt`

Five laws: `mutualist_council_republic`, `mutualist_armed_neutrality`, `mutualist_economy`, `mutualist_healthcare`, `mutualist_oligarchy`.

- [ ] **Step 1: `law_mutualist_council_republic` — prepend to existing `can_enact`**

Find (line 818):
```pdx
	can_enact = {
		NOT = { has_government_type = gov_chartered_company }
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = mutualist_council_republic }
		NOT = { has_government_type = gov_chartered_company }
	}
```

- [ ] **Step 2: `law_mutualist_armed_neutrality` — add `can_enact` block (none exists)**

Find (line 856) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = mutualist_armed_neutrality }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 3: `law_mutualist_economy` — prepend to existing `can_enact`**

Find (line 898):
```pdx
	can_enact = {
			OR = {
				has_law_or_variant = law_type:law_council_republic
				has_law_or_variant = law_type:law_corporate_state
			}
			OR = {
				has_law_or_variant = law_type:law_single_party_state
				has_law_or_variant = law_type:law_technocracy
				has_law_or_variant = law_type:law_autocracy
				has_law_or_variant = law_type:law_oligarchy
			}
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = mutualist_economy }
			OR = {
				has_law_or_variant = law_type:law_council_republic
				has_law_or_variant = law_type:law_corporate_state
			}
			OR = {
				has_law_or_variant = law_type:law_single_party_state
				has_law_or_variant = law_type:law_technocracy
				has_law_or_variant = law_type:law_autocracy
				has_law_or_variant = law_type:law_oligarchy
			}
	}
```

- [ ] **Step 4: `law_mutualist_healthcare` — prepend to existing `can_enact`**

Find (line 958):
```pdx
	can_enact = {
		OR = {
			has_law_or_variant = law_type:law_single_party_state
			has_law = law_type:law_mutualist_oligarchy
			has_law_or_variant = law_type:law_census_voting
			has_law_or_variant = law_type:law_universal_suffrage
			has_law_or_variant = law_type:law_anarchy
		}
		
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = mutualist_healthcare }
		OR = {
			has_law_or_variant = law_type:law_single_party_state
			has_law = law_type:law_mutualist_oligarchy
			has_law_or_variant = law_type:law_census_voting
			has_law_or_variant = law_type:law_universal_suffrage
			has_law_or_variant = law_type:law_anarchy
		}
	}
```

- [ ] **Step 5: `law_mutualist_oligarchy` — add `can_enact` block (none exists)**

Find (line 1000) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = mutualist_oligarchy }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 6: Verify syntax**

Check `error.log` for any errors referencing `mutualist` laws.

- [ ] **Step 7: Commit**

```bash
git add common/laws/internationale_laws.txt
git commit -m "feat: gate mutualist laws on intl_law_permanently_enabled"
```

---

## Task 7: Gate Syndicalist Laws

**Files:**
- Modify: `common/laws/internationale_laws.txt`

Five laws: `syndicalist_council_republic`, `syndicalist_single_party`, `syndicalist_bureaucracy`, `syndicalist_economy`, `syndicalist_land_reform`.

- [ ] **Step 1: `law_syndicalist_council_republic` — prepend to existing `can_enact`**

Find (line 1040):
```pdx
	can_enact = {
		NOT = { has_government_type = gov_chartered_company }
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = syndicalist_council_republic }
		NOT = { has_government_type = gov_chartered_company }
	}
```

- [ ] **Step 2: `law_syndicalist_single_party` — add `can_enact` block (none exists)**

Find (line 1073) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = syndicalist_single_party }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 3: `law_syndicalist_bureaucracy` — add `can_enact` block (none exists)**

Find (line 1107) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = syndicalist_bureaucracy }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 4: `law_syndicalist_economy` — prepend to existing `can_enact`**

Find (line 1149):
```pdx
	can_enact = {
		OR = {
			has_law_or_variant = law_type:law_council_republic
			has_law_or_variant = law_type:law_corporate_state
		}
	}
```
Replace with:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = syndicalist_economy }
		OR = {
			has_law_or_variant = law_type:law_council_republic
			has_law_or_variant = law_type:law_corporate_state
		}
	}
```

- [ ] **Step 5: `law_syndicalist_land_reform` — add `can_enact` block (none exists)**

Find (line 1216) — `can_enact` is absent; the block starts with `can_impose`:
```pdx
	can_impose = {
		always = no
	}
```
Insert immediately before it:
```pdx
	can_enact = {
		intl_law_permanently_enabled = { LAW = syndicalist_land_reform }
	}

	can_impose = {
		always = no
	}
```

- [ ] **Step 6: Verify syntax**

Check `error.log` for any errors referencing `syndicalist` laws.

- [ ] **Step 7: Final smoke test**

In-game console (enable with `debugmode` on launch):
```
effect set_global_variable = { name = intl_law_syndicalist_economy value = 2 }
```
Then open the laws panel for a country. `law_syndicalist_economy` should now show as enactable (subject to its other conditions). Set the variable back to 0 and confirm it is no longer enactable:
```
effect remove_global_variable = intl_law_syndicalist_economy
```

- [ ] **Step 8: Commit**

```bash
git add common/laws/internationale_laws.txt
git commit -m "feat: gate syndicalist laws on intl_law_permanently_enabled"
```
