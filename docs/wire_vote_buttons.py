path = r"c:\Users\goria\Documents\Paradox Interactive\Victoria 3\mod\vic3Internationale\gui\internationale_gui.gui"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

t9  = "\t\t\t\t\t\t\t\t\t"
t10 = "\t\t\t\t\t\t\t\t\t\t"

# Wire the "Keep Current Law" button (current law / SIDE=1)
old_keep = (
    t9  + 'button_standard = {\n' +
    t10 + 'size = { 220 36 }\n' +
    t10 + 'parentanchor = hcenter\n' +
    t10 + 'text = "intl_vote_keep_button"\n' +
    t9  + '}'
)
new_keep = (
    t9  + 'button_standard = {\n' +
    t10 + 'size = { 220 36 }\n' +
    t10 + 'parentanchor = hcenter\n' +
    t10 + 'text = "intl_vote_keep_button"\n' +
    t10 + 'enabled = "[Not(GetPlayer.MakeScope.Var(\'intl_vote_stance\').IsSet)]"\n' +
    t10 + 'onclick = "[GetScriptedGui(\'intl_cast_vote_current_sgui\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"\n' +
    t9  + '}'
)

assert old_keep in content, "KEEP BUTTON NOT FOUND"
content = content.replace(old_keep, new_keep, 1)

# Wire the "Support Proposal" button (proposed law / SIDE=2)
old_support = (
    t9  + 'button_standard = {\n' +
    t10 + 'size = { 220 36 }\n' +
    t10 + 'parentanchor = hcenter\n' +
    t10 + 'text = "intl_vote_support_button"\n' +
    t9  + '}'
)
new_support = (
    t9  + 'button_standard = {\n' +
    t10 + 'size = { 220 36 }\n' +
    t10 + 'parentanchor = hcenter\n' +
    t10 + 'text = "intl_vote_support_button"\n' +
    t10 + 'enabled = "[Not(GetPlayer.MakeScope.Var(\'intl_vote_stance\').IsSet)]"\n' +
    t10 + 'onclick = "[GetScriptedGui(\'intl_cast_vote_proposed_sgui\').Execute(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"\n' +
    t9  + '}'
)

assert old_support in content, "SUPPORT BUTTON NOT FOUND"
content = content.replace(old_support, new_support, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("DONE")
