path = r"c:\Users\goria\Documents\Paradox Interactive\Victoria 3\mod\vic3Internationale\gui\internationale_gui.gui"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

no_tab = "Not(Or(Or(Or(Or(GetVariableSystem.Exists('intl_tab_anarchist'), GetVariableSystem.Exists('intl_tab_mutualist')), GetVariableSystem.Exists('intl_tab_syndicalist')), GetVariableSystem.Exists('intl_tab_blanquist')), GetVariableSystem.Exists('intl_tab_marxist')))"

# Find the placeholder widget — from "### Placeholder" to closing "}"
# We know lines 516-535 from earlier inspection
# Use string markers
start_marker = "\t\t\t\t\t### Placeholder when nothing selected\n\t\t\t\t\twidget = {"
end_marker = "\t\t\t\t\t}\n\n\n\t\t\t\t\t### Anarchist doctrine"

assert start_marker in content, "START NOT FOUND"
assert end_marker in content, "END NOT FOUND"

old_block = content[content.index(start_marker):content.index(end_marker)]
print("OLD BLOCK length:", len(old_block))

t5 = "\t\t\t\t\t"
t6 = "\t\t\t\t\t\t"
t7 = "\t\t\t\t\t\t\t"
t8 = "\t\t\t\t\t\t\t\t"
t9 = "\t\t\t\t\t\t\t\t\t"

new_block = (
    t5 + "### CURRENT MOTION — no active vote\n" +
    t5 + "widget = {\n" +
    t6 + "layoutpolicy_horizontal = expanding\n" +
    t6 + "size = { 0 180 }\n" +
    t6 + 'visible = "[And(' + no_tab + ', Not(GetGlobalVariable(\'intl_vote_active\').IsSet))]"\n' +
    "\n" +
    t6 + "background = {\n" +
    t7 + "using = entry_bg_fancy\n" +
    t7 + "alpha = 0.3\n" +
    t6 + "}\n" +
    "\n" +
    t6 + "vbox = {\n" +
    t7 + "parentanchor = center\n" +
    t7 + "spacing = 8\n" +
    t7 + "textbox = {\n" +
    t8 + "size = { 700 40 }\n" +
    t8 + 'text = "intl_no_current_motion"\n' +
    t8 + "using = fontsize_large\n" +
    t8 + "align = hcenter|nobaseline\n" +
    t8 + "parentanchor = hcenter\n" +
    t8 + "alpha = 0.6\n" +
    t7 + "}\n" +
    t7 + "textbox = {\n" +
    t8 + "size = { 700 30 }\n" +
    t8 + 'text = "intl_no_current_motion_hint"\n' +
    t8 + "using = fontsize_small\n" +
    t8 + "align = hcenter|nobaseline\n" +
    t8 + "parentanchor = hcenter\n" +
    t8 + "alpha = 0.4\n" +
    t7 + "}\n" +
    t6 + "}\n" +
    t5 + "}\n" +
    "\n" +
    t5 + "### CURRENT MOTION — active vote interface\n" +
    t5 + "widget = {\n" +
    t6 + "layoutpolicy_horizontal = expanding\n" +
    t6 + "size = { 0 310 }\n" +
    t6 + 'visible = "[And(' + no_tab + ', GetGlobalVariable(\'intl_vote_active\').IsSet)]"\n' +
    "\n" +
    t6 + "hbox = {\n" +
    t7 + "layoutpolicy_horizontal = expanding\n" +
    t7 + "spacing = 8\n" +
    t7 + "margin = { 10 8 }\n" +
    "\n" +
    t7 + "### LEFT — current law\n" +
    t7 + "widget = {\n" +
    t8 + "size = { 350 290 }\n" +
    t8 + "background = { using = entry_bg_fancy alpha = 0.4 }\n" +
    t8 + "vbox = {\n" +
    t9 + "parentanchor = center\n" +
    t9 + "spacing = 8\n" +
    t9 + "margin = { 10 10 }\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 320 28 }\n" +
    t9 + '\ttext = "intl_vote_current_label"\n' +
    t9 + "\tusing = fontsize_medium\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "\talpha = 0.7\n" +
    t9 + "}\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 320 60 }\n" +
    t9 + '\ttext = "intl_vote_law_name_placeholder"\n' +
    t9 + "\tusing = fontsize_large\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "}\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 320 28 }\n" +
    t9 + '\ttext = "intl_vote_count_current_label"\n' +
    t9 + "\tusing = fontsize_small\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "\talpha = 0.6\n" +
    t9 + "}\n" +
    t9 + "button_standard = {\n" +
    t9 + "\tsize = { 220 36 }\n" +
    t9 + "\tparentanchor = hcenter\n" +
    t9 + '\ttext = "intl_vote_keep_button"\n' +
    t9 + "}\n" +
    t8 + "}\n" +
    t7 + "}\n" +
    "\n" +
    t7 + "### CENTER — status\n" +
    t7 + "widget = {\n" +
    t8 + "size = { 160 290 }\n" +
    t8 + "vbox = {\n" +
    t9 + "parentanchor = center\n" +
    t9 + "spacing = 10\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 140 50 }\n" +
    t9 + '\ttext = "VS"\n' +
    t9 + "\tusing = fontsize_xxl\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "\talpha = 0.5\n" +
    t9 + "}\n" +
    t9 + "progressbar = {\n" +
    t9 + "\tsize = { 140 20 }\n" +
    t9 + "\tvalue = \"[GetGlobalVariable('intl_vote_prestige_current').GetValue(int32)]\"\n" +
    t9 + "\tmax = \"[Add(GetGlobalVariable('intl_vote_prestige_current').GetValue(int32), GetGlobalVariable('intl_vote_prestige_proposed').GetValue(int32))]\"\n" +
    t9 + "}\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 140 24 }\n" +
    t9 + '\ttext = "intl_vote_months_left_label"\n' +
    t9 + "\tusing = fontsize_small\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "}\n" +
    t8 + "}\n" +
    t7 + "}\n" +
    "\n" +
    t7 + "### RIGHT — proposed law\n" +
    t7 + "widget = {\n" +
    t8 + "size = { 350 290 }\n" +
    t8 + "background = { using = entry_bg_fancy alpha = 0.4 }\n" +
    t8 + "vbox = {\n" +
    t9 + "parentanchor = center\n" +
    t9 + "spacing = 8\n" +
    t9 + "margin = { 10 10 }\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 320 28 }\n" +
    t9 + '\ttext = "intl_vote_proposed_label"\n' +
    t9 + "\tusing = fontsize_medium\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "\talpha = 0.7\n" +
    t9 + "}\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 320 60 }\n" +
    t9 + '\ttext = "intl_vote_law_name_placeholder"\n' +
    t9 + "\tusing = fontsize_large\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "}\n" +
    t9 + "textbox = {\n" +
    t9 + "\tsize = { 320 28 }\n" +
    t9 + '\ttext = "intl_vote_count_proposed_label"\n' +
    t9 + "\tusing = fontsize_small\n" +
    t9 + "\talign = hcenter|nobaseline\n" +
    t9 + "\talpha = 0.6\n" +
    t9 + "}\n" +
    t9 + "button_standard = {\n" +
    t9 + "\tsize = { 220 36 }\n" +
    t9 + "\tparentanchor = hcenter\n" +
    t9 + '\ttext = "intl_vote_support_button"\n' +
    t9 + "}\n" +
    t8 + "}\n" +
    t7 + "}\n" +
    t6 + "}\n" +
    t5 + "}"
)

content = content.replace(old_block, new_block, 1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("DONE")
