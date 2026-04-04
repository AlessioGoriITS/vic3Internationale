# Debate Panel Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the active vote widget in the Internationale GUI to match the HTML mockup: a 3-column debate panel with law cards on the sides, faction-tagged VS portrait stage in the center, and a left/right filled support bar — replacing the current overlaid full-body portrait approach.

**Architecture:** The active vote `widget` in `internationale_gui.gui` is replaced entirely: full-body `character_portrait_front_vs_left/right` overlays are removed and replaced with a title bar + 3-column `hbox`. The left and right columns are law cards styled with per-faction color accent bars and per-faction law name/description textboxes. The center column has a VS header row with faction name tags, two `character_portrait_small2` portraits facing each other, and a `gold_progressbar_horizontal` support bar. Two new globals track which specific law is current/proposed (for conditional law-name display). All new text is localized.

**Tech Stack:** Vic3 Clausewitz GUI (`.gui`), Vic3 scripted effects (`.txt`), Vic3 YAML localization (`.yml`)

**Faction color palette (Vic3 `color = { r g b a }` format):**
| Faction    | Color                      |
|------------|----------------------------|
| Anarchist  | `{ 0.15 0.15 0.15 1 }`    |
| Mutualist  | `{ 0.13 0.33 0.67 1 }`    |
| Syndicalist| `{ 0.75 0.18 0.12 1 }`    |
| Blanquist  | `{ 0.45 0.12 0.55 1 }`    |
| Marxist    | `{ 0.55 0.08 0.08 1 }`    |

---

## File Map

| File | Change |
|------|--------|
| `common/scripted_effects/intl_vote_effects.txt` | Add `intl_vote_current_law_$CURRENT$` and `intl_vote_proposed_law_$PROPOSED$` globals in `intl_start_vote`; clean them in `intl_cancel_vote` |
| `localization/english/intl_vote_l_english.yml` | Add law name keys, law description keys (per faction), faction tag keys, panel title key |
| `gui/internationale_gui.gui` | Replace the active vote widget block (~lines 539–745) with the new debate panel layout |

---

## Task 1 — Law-specific globals in scripted effect

**Goal:** When a vote starts, set a boolean global for the specific current and proposed law (e.g., `intl_vote_current_law_marxist_council_republic`). This lets the GUI show the correct law name via a `visible` check without needing flag-comparison expressions.

**Files:**
- Modify: `common/scripted_effects/intl_vote_effects.txt`

The laws that can appear as CURRENT (from the events): `anarchist_council_republic`, `marxist_council_republic`, `mutualist_economy`, `marxist_economy`

The laws that can appear as PROPOSED (from the events): `marxist_council_republic`, `mutualist_council_republic`, `syndicalist_council_republic`, `blanquist_presidential_republic`, `anarchist_council_republic`, `syndicalist_council_republic`, `marxist_economy`, `mutualist_economy`, `anarchist_economy`, `syndicalist_economy`, `blanquist_economy`

- [ ] **Step 1: Add law globals to `intl_start_vote`**

In `intl_vote_effects.txt`, after line 19 (the two existing faction globals), add:

```
set_global_variable = intl_vote_current_law_$CURRENT$
set_global_variable = intl_vote_proposed_law_$PROPOSED$
```

The full `intl_start_vote` block should now look like:
```
intl_start_vote = {
    if = {
        limit = { NOT = { has_global_variable = intl_vote_active } }
        set_global_variable = intl_vote_active
        set_global_variable = { name = intl_vote_law_current value = flag:$CURRENT$ }
        set_global_variable = { name = intl_vote_law_proposed value = flag:$PROPOSED$ }
        set_global_variable = { name = intl_vote_months_left value = 6 }
        set_global_variable = { name = intl_vote_prestige_current value = 0 }
        set_global_variable = { name = intl_vote_prestige_proposed value = 0 }
        set_global_variable = { name = intl_vote_count_current value = 0 }
        set_global_variable = { name = intl_vote_count_proposed value = 0 }
        set_global_variable = intl_vote_current_faction_$CURRENT_FACTION$
        set_global_variable = intl_vote_proposed_faction_$PROPOSED_FACTION$
        set_global_variable = intl_vote_current_law_$CURRENT$
        set_global_variable = intl_vote_proposed_law_$PROPOSED$
        every_country = {
            ...
        }
    }
}
```

- [ ] **Step 2: Add cleanup for law globals to `intl_cancel_vote`**

In `intl_cancel_vote`, after the 10 existing faction cleanup lines, add cleanup for all possible current law globals:

```
# Current law globals
if = { limit = { has_global_variable = intl_vote_current_law_anarchist_council_republic } remove_global_variable = intl_vote_current_law_anarchist_council_republic }
if = { limit = { has_global_variable = intl_vote_current_law_marxist_council_republic } remove_global_variable = intl_vote_current_law_marxist_council_republic }
if = { limit = { has_global_variable = intl_vote_current_law_mutualist_economy } remove_global_variable = intl_vote_current_law_mutualist_economy }
if = { limit = { has_global_variable = intl_vote_current_law_marxist_economy } remove_global_variable = intl_vote_current_law_marxist_economy }
# Proposed law globals
if = { limit = { has_global_variable = intl_vote_proposed_law_marxist_council_republic } remove_global_variable = intl_vote_proposed_law_marxist_council_republic }
if = { limit = { has_global_variable = intl_vote_proposed_law_mutualist_council_republic } remove_global_variable = intl_vote_proposed_law_mutualist_council_republic }
if = { limit = { has_global_variable = intl_vote_proposed_law_syndicalist_council_republic } remove_global_variable = intl_vote_proposed_law_syndicalist_council_republic }
if = { limit = { has_global_variable = intl_vote_proposed_law_blanquist_presidential_republic } remove_global_variable = intl_vote_proposed_law_blanquist_presidential_republic }
if = { limit = { has_global_variable = intl_vote_proposed_law_anarchist_council_republic } remove_global_variable = intl_vote_proposed_law_anarchist_council_republic }
if = { limit = { has_global_variable = intl_vote_proposed_law_mutualist_economy } remove_global_variable = intl_vote_proposed_law_mutualist_economy }
if = { limit = { has_global_variable = intl_vote_proposed_law_anarchist_economy } remove_global_variable = intl_vote_proposed_law_anarchist_economy }
if = { limit = { has_global_variable = intl_vote_proposed_law_syndicalist_economy } remove_global_variable = intl_vote_proposed_law_syndicalist_economy }
if = { limit = { has_global_variable = intl_vote_proposed_law_blanquist_economy } remove_global_variable = intl_vote_proposed_law_blanquist_economy }
```

- [ ] **Step 3: Verify in-game via debug event**

Trigger a vote via `intl_vote_events.10` → choose any option. Open console and check:
```
global_var:intl_vote_current_law_marxist_council_republic
```
(or whichever law was chosen). It should be set.

---

## Task 2 — Localization keys

**Goal:** Add all new string keys needed by the redesigned GUI.

**Files:**
- Modify: `localization/english/intl_vote_l_english.yml`

- [ ] **Step 1: Add law name keys, law description keys, faction tags, and panel title**

Append the following entries to `intl_vote_l_english.yml`:

```yaml
  # Panel title
  intl_vote_panel_title: "Current Policy Being Voted"

  # Faction tags (short labels shown beside VS)
  intl_faction_tag_anarchist: "Anarchist"
  intl_faction_tag_mutualist: "Mutualist"
  intl_faction_tag_syndicalist: "Syndicalist"
  intl_faction_tag_blanquist: "Blanquist"
  intl_faction_tag_marxist: "Marxist"

  # Law display names (shown as law card title)
  intl_lawname_anarchist_council_republic: "Anarchist Council Republic"
  intl_lawname_marxist_council_republic: "Marxist Council Republic"
  intl_lawname_mutualist_council_republic: "Mutualist Council Republic"
  intl_lawname_syndicalist_council_republic: "Syndicalist Council Republic"
  intl_lawname_blanquist_presidential_republic: "Blanquist Presidential Republic"
  intl_lawname_mutualist_economy: "Mutualist Cooperative Economy"
  intl_lawname_marxist_economy: "Marxist Planned Economy"
  intl_lawname_anarchist_economy: "Anarchist Cooperative Economy"
  intl_lawname_syndicalist_economy: "Syndicalist Economy"
  intl_lawname_blanquist_economy: "Blanquist Command Economy"

  # Law descriptions (shown as law card body text, by faction ideology)
  intl_lawdesc_anarchist_council_republic: "Power dispersed to freely associating communes. No central authority, no hierarchy — governance through direct federation."
  intl_lawdesc_marxist_council_republic: "The revolutionary vanguard leads through a democratic council of workers' representatives until class conflict is resolved."
  intl_lawdesc_mutualist_council_republic: "Governance through federated worker cooperatives, balancing free association with mutual credit institutions."
  intl_lawdesc_syndicalist_council_republic: "Industrial unions form the organs of state. Each syndicate governs its sphere — coordination through congress."
  intl_lawdesc_blanquist_presidential_republic: "A disciplined revolutionary party seizes the state and holds it until the conditions for socialism are secured."
  intl_lawdesc_mutualist_economy: "Enterprises reorganised as worker cooperatives, self-governed through mutual credit and free association."
  intl_lawdesc_marxist_economy: "The proletarian state directs key industries through centralised planning, ensuring rational allocation of resources."
  intl_lawdesc_anarchist_economy: "All productive property held in common by free communes. No wages, no markets — contribution by ability, access by need."
  intl_lawdesc_syndicalist_economy: "Workers' unions hold collective ownership of industries, coordinating production through syndicate councils."
  intl_lawdesc_blanquist_economy: "State command over the commanding heights, with disciplined allocation subordinated to the revolutionary programme."

  # Support bar labels
  intl_vote_bar_center_label: "Congress Support"
  intl_vote_count_current_pct: "[GetGlobalVariable('intl_vote_count_current').GetValue(int32).ToString] countries"
  intl_vote_count_proposed_pct: "[GetGlobalVariable('intl_vote_count_proposed').GetValue(int32).ToString] countries"
```

---

## Task 3 — Active vote widget rewrite

**Goal:** Replace the entire active vote widget block in `internationale_gui.gui` (currently lines ~539–745: the `widget` with overlaid full-body portraits + hbox with margin=280) with the new 3-column debate panel design matching the HTML mockup.

**Files:**
- Modify: `gui/internationale_gui.gui` (the active vote widget, second `widget` child of the scrollarea content vbox)

The new widget must:
- Keep the exact same `visible` condition as the current widget
- Keep the exact same `layoutpolicy_horizontal = expanding` and `size = { 0 380 }` (height increased to 380 to fit title bar + content)
- Use an inner `vbox` with: title bar row + main content hbox

- [ ] **Step 1: Locate and replace the active vote widget**

The block to replace starts at approximately line 539:
```
widget = {
    layoutpolicy_horizontal = expanding
    size = { 0 360 }
    visible = "[And(Not(Or(Or(Or(Or(GetVariableSystem.Exists('intl_tab_anarchist'), ...
```
and ends at approximately line 745 (closing `}` of the widget, after the RIGHT law card's closing `}`).

Replace the entire block with:

```
widget = {
    layoutpolicy_horizontal = expanding
    size = { 0 380 }
    visible = "[And(Not(Or(Or(Or(Or(GetVariableSystem.Exists('intl_tab_anarchist'), GetVariableSystem.Exists('intl_tab_mutualist')), GetVariableSystem.Exists('intl_tab_syndicalist')), GetVariableSystem.Exists('intl_tab_blanquist')), GetVariableSystem.Exists('intl_tab_marxist'))), GetGlobalVariable('intl_vote_active').IsSet)]"

    background = {
        using = entry_bg_fancy
        alpha = 0.5
    }

    vbox = {
        layoutpolicy_horizontal = expanding
        layoutpolicy_vertical = expanding

        ### TITLE BAR
        widget = {
            layoutpolicy_horizontal = expanding
            size = { 0 26 }
            background = {
                using = default_header_bg
                alpha = 0.7
            }
            textbox = {
                layoutpolicy_horizontal = expanding
                size = { 0 26 }
                text = "intl_vote_panel_title"
                using = fontsize_small
                align = hcenter|nobaseline
                parentanchor = vcenter
                alpha = 0.6
            }
        }

        ### MAIN 3-COLUMN ROW
        hbox = {
            layoutpolicy_horizontal = expanding
            size = { 0 354 }
            spacing = 6
            margin = { 6 6 }

            ########################################
            ### LEFT LAW CARD — current law
            ########################################
            widget = {
                layoutpolicy_horizontal = expanding
                size = { 0 342 }

                background = {
                    using = entry_bg_fancy
                    alpha = 0.35
                }

                ### Faction-colored top accent bar (2px) — one per faction, only one visible
                icon = {
                    size = { 100% 2 }
                    color = { 0.15 0.15 0.15 1 }
                    visible = "[GetGlobalVariable('intl_vote_current_faction_anarchist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.13 0.33 0.67 1 }
                    visible = "[GetGlobalVariable('intl_vote_current_faction_mutualist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.75 0.18 0.12 1 }
                    visible = "[GetGlobalVariable('intl_vote_current_faction_syndicalist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.45 0.12 0.55 1 }
                    visible = "[GetGlobalVariable('intl_vote_current_faction_blanquist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.55 0.08 0.08 1 }
                    visible = "[GetGlobalVariable('intl_vote_current_faction_marxist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }

                vbox = {
                    layoutpolicy_horizontal = expanding
                    spacing = 6
                    margin = { 10 10 }

                    ### "CURRENT LAW" label
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 18 }
                        text = "intl_vote_current_label"
                        using = fontsize_small
                        align = left|nobaseline
                        alpha = 0.55
                    }

                    ### Law title — one textbox per law, only the active one visible
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_anarchist_council_republic"
                        using = fontsize_large
                        align = left|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_current_law_anarchist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_marxist_council_republic"
                        using = fontsize_large
                        align = left|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_current_law_marxist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_mutualist_economy"
                        using = fontsize_large
                        align = left|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_current_law_mutualist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_marxist_economy"
                        using = fontsize_large
                        align = left|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_current_law_marxist_economy').IsSet]"
                    }

                    ### Divider
                    icon = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 1 }
                        texture = "gfx/interface/icons/generic_icons/transparent.dds"
                        using = solid_panel
                        color = { 0.35 0.32 0.2 0.3 }
                    }

                    ### Law description — one per law
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_anarchist_council_republic"
                        using = fontsize_small
                        align = left|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_current_law_anarchist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_marxist_council_republic"
                        using = fontsize_small
                        align = left|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_current_law_marxist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_mutualist_economy"
                        using = fontsize_small
                        align = left|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_current_law_mutualist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_marxist_economy"
                        using = fontsize_small
                        align = left|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_current_law_marxist_economy').IsSet]"
                    }

                    expand = {}

                    ### Vote button — keep current law
                    button_standard = {
                        size = { 100% 36 }
                        text = "intl_vote_keep_button"
                        enabled = "[Not(GetPlayer.MakeScope.Var('intl_vote_stance').IsSet)]"
                        onclick = "[GetScriptedGui('intl_cast_vote_current_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
                    }
                }
            }

            ########################################
            ### CENTER STAGE
            ########################################
            vbox = {
                size = { 210 342 }
                spacing = 6

                ### VS ROW with faction names
                hbox = {
                    layoutpolicy_horizontal = expanding
                    spacing = 4

                    ### Current faction tag — one per faction
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_anarchist"
                        using = fontsize_small
                        align = left|nobaseline
                        color = { 0.15 0.15 0.15 1 }
                        visible = "[GetGlobalVariable('intl_vote_current_faction_anarchist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_mutualist"
                        using = fontsize_small
                        align = left|nobaseline
                        color = { 0.13 0.33 0.67 1 }
                        visible = "[GetGlobalVariable('intl_vote_current_faction_mutualist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_syndicalist"
                        using = fontsize_small
                        align = left|nobaseline
                        color = { 0.75 0.18 0.12 1 }
                        visible = "[GetGlobalVariable('intl_vote_current_faction_syndicalist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_blanquist"
                        using = fontsize_small
                        align = left|nobaseline
                        color = { 0.45 0.12 0.55 1 }
                        visible = "[GetGlobalVariable('intl_vote_current_faction_blanquist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_marxist"
                        using = fontsize_small
                        align = left|nobaseline
                        color = { 0.55 0.08 0.08 1 }
                        visible = "[GetGlobalVariable('intl_vote_current_faction_marxist').IsSet]"
                    }

                    ### VS
                    textbox = {
                        size = { 40 20 }
                        text = "VS"
                        using = fontsize_medium
                        align = hcenter|nobaseline
                        alpha = 0.35
                    }

                    ### Proposed faction tag — one per faction
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_anarchist"
                        using = fontsize_small
                        align = right|nobaseline
                        color = { 0.15 0.15 0.15 1 }
                        visible = "[GetGlobalVariable('intl_vote_proposed_faction_anarchist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_mutualist"
                        using = fontsize_small
                        align = right|nobaseline
                        color = { 0.13 0.33 0.67 1 }
                        visible = "[GetGlobalVariable('intl_vote_proposed_faction_mutualist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_syndicalist"
                        using = fontsize_small
                        align = right|nobaseline
                        color = { 0.75 0.18 0.12 1 }
                        visible = "[GetGlobalVariable('intl_vote_proposed_faction_syndicalist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_blanquist"
                        using = fontsize_small
                        align = right|nobaseline
                        color = { 0.45 0.12 0.55 1 }
                        visible = "[GetGlobalVariable('intl_vote_proposed_faction_blanquist').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 20 }
                        text = "intl_faction_tag_marxist"
                        using = fontsize_small
                        align = right|nobaseline
                        color = { 0.55 0.08 0.08 1 }
                        visible = "[GetGlobalVariable('intl_vote_proposed_faction_marxist').IsSet]"
                    }
                }

                ### PORTRAITS ROW
                hbox = {
                    layoutpolicy_horizontal = expanding
                    spacing = 6

                    ### LEFT portrait (current law faction)
                    vbox = {
                        spacing = 4

                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('bakunin_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_current_faction_anarchist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('proudhon_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_current_faction_mutualist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('bel_de_paepe_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_current_faction_syndicalist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('blanqui_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_current_faction_blanquist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('karl_marx_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_current_faction_marxist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }

                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_anarchist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_current_faction_anarchist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_mutualist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_current_faction_mutualist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_syndicalist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_current_faction_syndicalist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_blanquist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_current_faction_blanquist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_marxist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_current_faction_marxist').IsSet]"
                        }
                    }

                    expand = {}

                    ### RIGHT portrait (proposed law faction)
                    vbox = {
                        spacing = 4

                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('bakunin_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_anarchist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('proudhon_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_mutualist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('bel_de_paepe_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_syndicalist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('blanqui_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_blanquist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }
                        character_portrait_small2 = {
                            parentanchor = hcenter
                            datacontext = "[GetPlayer.MakeScope.Var('karl_marx_scope_gui').GetCharacter]"
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_marxist').IsSet]"
                            blockoverride "portrait_icons" {}
                            blockoverride "portrait_button_onclick" { onclick = "" }
                            blockoverride "portrait_button_onrightclick" { onrightclick = "" }
                        }

                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_anarchist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_anarchist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_mutualist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_mutualist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_syndicalist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_syndicalist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_blanquist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_blanquist').IsSet]"
                        }
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 90 18 }
                            text = "intl_faction_tag_marxist"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.7
                            visible = "[GetGlobalVariable('intl_vote_proposed_faction_marxist').IsSet]"
                        }
                    }
                }

                expand = {}

                ### SUPPORT BAR
                widget = {
                    layoutpolicy_horizontal = expanding
                    size = { 0 72 }

                    vbox = {
                        layoutpolicy_horizontal = expanding
                        spacing = 4

                        ### Labels row
                        hbox = {
                            layoutpolicy_horizontal = expanding
                            textbox = {
                                layoutpolicy_horizontal = expanding
                                size = { 0 16 }
                                text = "intl_vote_count_current_pct"
                                using = fontsize_small
                                align = left|nobaseline
                                alpha = 0.7
                            }
                            textbox = {
                                size = { 90 16 }
                                text = "intl_vote_bar_center_label"
                                using = fontsize_small
                                align = hcenter|nobaseline
                                alpha = 0.35
                            }
                            textbox = {
                                layoutpolicy_horizontal = expanding
                                size = { 0 16 }
                                text = "intl_vote_count_proposed_pct"
                                using = fontsize_small
                                align = right|nobaseline
                                alpha = 0.7
                            }
                        }

                        ### Bar track
                        gold_progressbar_horizontal = {
                            layoutpolicy_horizontal = expanding
                            size = { 0 12 }
                            blockoverride "values" {
                                value = "[GetGlobalVariable('intl_vote_count_current').GetValue(int32)]"
                                min = 0
                                max = "[Add(GetGlobalVariable('intl_vote_count_current').GetValue(int32), GetGlobalVariable('intl_vote_count_proposed').GetValue(int32))]"
                            }
                        }

                        ### Months remaining
                        textbox = {
                            layoutpolicy_horizontal = expanding
                            size = { 0 18 }
                            text = "intl_vote_months_left_label"
                            using = fontsize_small
                            align = hcenter|nobaseline
                            alpha = 0.45
                        }
                    }
                }
            }

            ########################################
            ### RIGHT LAW CARD — proposed law
            ########################################
            widget = {
                layoutpolicy_horizontal = expanding
                size = { 0 342 }

                background = {
                    using = entry_bg_fancy
                    alpha = 0.35
                }

                ### Faction-colored top accent bar — proposed faction
                icon = {
                    size = { 100% 2 }
                    color = { 0.15 0.15 0.15 1 }
                    visible = "[GetGlobalVariable('intl_vote_proposed_faction_anarchist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.13 0.33 0.67 1 }
                    visible = "[GetGlobalVariable('intl_vote_proposed_faction_mutualist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.75 0.18 0.12 1 }
                    visible = "[GetGlobalVariable('intl_vote_proposed_faction_syndicalist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.45 0.12 0.55 1 }
                    visible = "[GetGlobalVariable('intl_vote_proposed_faction_blanquist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }
                icon = {
                    size = { 100% 2 }
                    color = { 0.55 0.08 0.08 1 }
                    visible = "[GetGlobalVariable('intl_vote_proposed_faction_marxist').IsSet]"
                    texture = "gfx/interface/icons/generic_icons/transparent.dds"
                    using = solid_panel
                }

                vbox = {
                    layoutpolicy_horizontal = expanding
                    spacing = 6
                    margin = { 10 10 }

                    ### "PROPOSED LAW" label
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 18 }
                        text = "intl_vote_proposed_label"
                        using = fontsize_small
                        align = right|nobaseline
                        alpha = 0.55
                    }

                    ### Law title — proposed
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_marxist_council_republic"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_marxist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_mutualist_council_republic"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_mutualist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_syndicalist_council_republic"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_syndicalist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_blanquist_presidential_republic"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_blanquist_presidential_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_anarchist_council_republic"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_anarchist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_mutualist_economy"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_mutualist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_anarchist_economy"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_anarchist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_syndicalist_economy"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_syndicalist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 46 }
                        text = "intl_lawname_blanquist_economy"
                        using = fontsize_large
                        align = right|nobaseline
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_blanquist_economy').IsSet]"
                    }

                    ### Divider
                    icon = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 1 }
                        texture = "gfx/interface/icons/generic_icons/transparent.dds"
                        using = solid_panel
                        color = { 0.35 0.32 0.2 0.3 }
                    }

                    ### Law description — proposed
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_marxist_council_republic"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_marxist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_mutualist_council_republic"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_mutualist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_syndicalist_council_republic"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_syndicalist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_blanquist_presidential_republic"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_blanquist_presidential_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_anarchist_council_republic"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_anarchist_council_republic').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_mutualist_economy"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_mutualist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_anarchist_economy"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_anarchist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_syndicalist_economy"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_syndicalist_economy').IsSet]"
                    }
                    textbox = {
                        layoutpolicy_horizontal = expanding
                        size = { 0 90 }
                        text = "intl_lawdesc_blanquist_economy"
                        using = fontsize_small
                        align = right|nobaseline
                        autoresize = yes
                        alpha = 0.55
                        visible = "[GetGlobalVariable('intl_vote_proposed_law_blanquist_economy').IsSet]"
                    }

                    expand = {}

                    ### Vote button — support proposed law
                    button_standard = {
                        size = { 100% 36 }
                        text = "intl_vote_support_button"
                        enabled = "[Not(GetPlayer.MakeScope.Var('intl_vote_stance').IsSet)]"
                        onclick = "[GetScriptedGui('intl_cast_vote_proposed_sgui').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
                    }
                }
            }

        }
    }
}
```

- [ ] **Step 2: Verify brace count**

After pasting, manually count that the new widget block opens 1 `widget {` and closes exactly 1 matching `}`. The simplest check: reload the mod in-game and look for `Error: gui file` messages in the game log.

- [ ] **Step 3: Verify in-game layout**

Trigger a vote through the motion event. The Internationale window should show:
- A narrow title bar "Current Policy Being Voted"
- Left card: "CURRENT LAW" label + law name + description + Keep button
- Center: faction tags flanking VS + two small circle portraits + gold fill bar
- Right card: "PROPOSED LAW" label + law name (right-aligned) + description + Support button

---

## Known Limitations / Follow-up

1. **Faction top accent bar**: The `using = solid_panel` may not exist; if it fails to render, replace with `texture = "gfx/interface/flat_bg.dds"`. Adjust as needed after in-game testing.

2. **`intl_lawdesc_mutualist_council_republic`** localization key is added in Task 2 but never used as a proposed law description in the current event set — it is included for completeness as this law will be added in future events.

3. **VS row faction tags**: The `hbox` containing faction name tags on left and right uses `layoutpolicy_horizontal = expanding` on each tag. Because multiple tags are stacked in the same hbox (only one per side visible at a time), this should work — only the visible one expands. If both somehow show, recheck faction boolean globals.

4. **`color = {}` on textbox**: Vic3 `textbox` supports `color = { r g b a }` for faction-colored faction tag text. If the color property doesn't work on a textbox, wrap each textbox in a `widget` with the color applied via `color` on the widget (which tints children).
