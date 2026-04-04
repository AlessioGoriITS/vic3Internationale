# Victoria 3 `.gui` File Documentation

All syntax in this document is confirmed from vanilla game files (`F:\SteamLibrary\steamapps\common\Victoria 3\game\gui\`) and mod `.gui` files in this workspace. Nothing is assumed or hallucinated.

---

## 1. File Location & Mod Override

- Vanilla files live under `game/gui/`.
- Subdirectories: `shared/` (reusable templates, textures, animations), `frontend/` and `frontend/shared/`, `jomini/`, `achievements/`, `notifications/`, `tools/layouts/`.
- Most panel `.gui` files sit directly under `gui/`.
- **Mod override rule:** A mod file at the **same relative path** (e.g. `gui/production_methods.gui`) **replaces the entire vanilla file**. It is not merged.
- New `.gui` files with unique names are **additive** (e.g. `gui/internationale_gui.gui` adds a new window without touching vanilla).

---

## 2. Top-Level Constructs

### 2.1 `@` Variables (constants)

```
@panel_width = 530
@entry_height = 50
```

Used anywhere a numeric value is expected: `size = { @panel_width 400 }`.

### 2.2 `template`

Reusable property bundles. Included with `using = template_name`.

```
template dark_area {
    background = {
        texture = "gfx/interface/backgrounds/dark_area.dds"
        spriteType = Corneredstretched
        spriteborder = { 20 20 }
    }
}
```

Multiple `using =` lines can be stacked on a single widget. Templates can chain other templates:

```
template rotate_glow_red {
    using = rotate_glow_blue
    texture = "gfx/interface/animation/glow_red.dds"
}
```

### 2.3 `types` + `type`

Named widget types grouped under a `types` block. A type extends a base widget:

```
types console_widgets {
    type console_button = button {
        size = { 100 30 }
        using = default_button
    }
}
```

Types support inheritance: `type default_notification = notification_popup { blockoverride ... }`.

### 2.4 Root widget instances

Widgets declared outside `types` are instantiated directly:

```
widget = {
    name = "error_deer"
    size = { 64 64 }
    visible = "[And(ErrorDeer.HasErrors, IsInGame)]"
}
```

```
window = {
    name = "internationale_window"
    size = { 800 600 }
    layer = windows_layer
}
```

```
right_click_menu = {
    name = "switch_production_method_menu"
    parentanchor = top|right
    widgetanchor = top|left
}
```

---

## 3. Widget / Element Types (confirmed)

### Layout containers
| Type | Description |
|------|-------------|
| `widget` | Generic container |
| `container` | Lightweight grouping |
| `window` | Top-level window with layer support |
| `hbox` | Horizontal box layout |
| `vbox` | Vertical box layout |
| `flowcontainer` | Flow layout with `direction` |
| `scrollarea` | Scrollable region |
| `fixedgridbox` | Fixed-size grid |
| `dynamicgridbox` | Data-bound grid with `datamodel_wrap` |
| `background` | Background texture element |

### Interactive / display
| Type | Description |
|------|-------------|
| `button` | Clickable element |
| `icon` | Image/texture display |
| `textbox` | Text display |
| `editbox` | Text input field |
| `scrollbar` | Scroll control (used in templates) |
| `progressbar` | Progress indicator |
| `right_click_menu` | Context menu |

---

## 4. Properties Reference

### 4.1 Geometry & Layout

| Property | Example | Notes |
|----------|---------|-------|
| `size` | `{ 400 300 }` | Width, height |
| `position` | `{ 10 20 }` | X, Y offset |
| `position_y` | `-50` | Y offset only |
| `position` | `"[SomeObject.CalcPosition]"` | Dynamic expression |
| `parentanchor` | `top\|right`, `center`, `vcenter` | Pipe-separated |
| `widgetanchor` | `top\|left` | Used on menus/popups |
| `margin` | `{ 10 5 }` | |
| `margin_left` | `8` | Individual sides |
| `margin_right` | `8` | |
| `margin_top` | `5` | |
| `margin_bottom` | `5` | |
| `minimumsize` | `{ -1 20 }` | `-1` = unconstrained |
| `maximumsize` | `{ 300 -1 }` | |
| `spacing` | `5` | Gap between children |
| `direction` | `vertical` / `horizontal` | On `flowcontainer` |
| `flipdirection` | `yes` | Reverse layout direction |
| `layoutpolicy_horizontal` | `expanding` | On hbox/vbox children |
| `layoutpolicy_vertical` | `expanding` | |
| `resizeparent` | `yes` | Child drives parent size |
| `ignoreinvisible` | `yes` | Skip invisible children in layout |
| `datamodel_wrap` | `4` | Wrap count for `dynamicgridbox` |

### 4.2 Visual

| Property | Example | Notes |
|----------|---------|-------|
| `texture` | `"gfx/interface/icons/foo.dds"` | Static path |
| `texture` | `"[BuildingType.GetIcon]"` | Dynamic binding |
| `framesize` | `{ 40 40 }` | Sprite sheet frame |
| `scale` | `0.5` | |
| `alpha` | `0.2` | 0.0 transparent, 1.0 opaque |
| `color` | `{ 1.0 0.5 0.5 1.0 }` | RGBA float |
| `color` | `"[InterestGroup.GetColor]"` | Dynamic |
| `spriteType` | `Corneredstretched` | 9-slice |
| `spriteborder` | `{ 20 20 }` | 9-slice insets |
| `blend_mode` | `alphamultiply` | |
| `shaderfile` | `"gfx/FX/pdxgui_default.shader"` | |
| `scissor` | `yes` | Clip children to bounds |
| `layer` | `windows_layer`, `confirmation`, `top` | Render order |
| `alwaystransparent` | `yes` | Pass-through mouse |

### 4.3 Text

| Property | Example | Notes |
|----------|---------|-------|
| `text` | `"LOCALIZATION_KEY"` | Localization lookup |
| `raw_text` | `"literal text"` | No localization |
| `align` | `nobaseline`, `center`, `left`, `right` | |
| `multiline` | `yes` | |
| `autoresize` | `yes` | Size to content |
| `max_width` | `300` | |
| `fontsize` | `16` | |
| `fontsize_min` | `10` | Minimum when shrinking |
| `font` | `"font_name"` | |
| `default_format` | `"#variable"` | Color format tag |
| `elide` | `right` | Truncation |

Format tags in `raw_text`: `#bold`, `#variable`, `#N` (newline), `#p`, `#v`, `#gold`, `#i`, `#!` (reset).

### 4.4 Interaction / Input

| Property | Example | Notes |
|----------|---------|-------|
| `onclick` | `"[SomeAction]"` | Multiple `onclick` lines = sequential |
| `onrightclick` | `"[SomeAction]"` | |
| `onmousehierarchyenter` | `"[PdxGuiInterruptThenTriggerAllAnimations('hide','show')]"` | Hover enter |
| `onmousehierarchyleave` | `"[...]"` | Hover leave |
| `shortcut` | `"close_window"` | Keyboard binding |
| `input_action` | `"back"` | Named input action |
| `enabled` | `"[BoolExpression]"` | |
| `focuspolicy` | `all` | |
| `filter_mouse` | `all` / `none` | |
| `allow_outside` | `yes` | |

Multiple `onclick` on the same widget fire sequentially:
```
onclick = "[GetVariableSystem.Clear('tab_a')]"
onclick = "[GetVariableSystem.Set('tab_b', 'true')]"
```

### 4.5 Button frame properties

| Property | Notes |
|----------|-------|
| `upframe` | Default frame index |
| `overframe` | Hover frame index |
| `downframe` | Pressed frame index |
| `distribute_visual_state` | Propagate state to children |
| `inherit_visual_state` | Inherit from parent |

### 4.6 Scrollarea

| Property | Example |
|----------|---------|
| `scrollbarpolicy_horizontal` | `always_off` |
| `scrollbar_vertical` | reference to scrollbar template |
| `scrollwidget` | `= { ... }` (content container) |
| `scrollbaralign_vertical` | alignment |
| `wheelstep` | scroll increment |

---

## 5. Data Binding

### 5.1 `datacontext`

Binds a widget tree to a game object:

```
datacontext = "[GetPlayer]"
datacontext = "[BuildingBrowserBuildingTypeItem.GetBuildingType]"
datacontext = "[GetPlayer.MakeScope.Var('ideologyleader_scope_gui').GetCharacter]"
```

### 5.2 `datamodel` + `item`

Repeats a child widget for each entry in a list:

```
dynamicgridbox = {
    datamodel = "[State.AccessUrbanBuildings]"
    datamodel_wrap = 4
    item = {
        building_item = {}
    }
}
```

### 5.3 Square-bracket expressions

Used in most string-valued properties:

```
visible = "[And(ErrorDeer.HasErrors, IsInGame)]"
text = "[Country.GetInfamyDesc]"
alpha = "[TransparentIfZero_int64(...)]"
enabled = "[Not(IsDataModelEmpty(...))]"
```

### 5.4 Typed literals in expressions

Explicit casts for comparison functions:

```
visible = "[GreaterThan_int32(SomeValue, '(int32)0')]"
visible = "[GreaterThan_CFixedPoint(Value, '(CFixedPoint)0')]"
visible = "[LessThan_float(GetCurrentFps, '(float)30')]"
```

### 5.5 Data model introspection

```
visible = "[Not(IsDataModelEmpty(SomeList))]"
visible = "[GreaterThan_int32(GetDataModelSize(SomeList), '(int32)0')]"
datacontext = "[SomeList.GetItem0.GetFirstPop]"
```

### 5.6 `GetVariableSystem`

Tab/toggle state management via named variables:

```
visible = "[GetVariableSystem.Exists('tab_name')]"
onclick = "[GetVariableSystem.Set('tab_name', 'true')]"
onclick = "[GetVariableSystem.Clear('tab_name')]"
```

### 5.7 Scope helpers

```
ProductionMethod.Self
GetPlayer.MakeScope.Var('varname').GetCharacter
PopupManager.CloseMessage(PlayerMessageItem.AccessSelf)
```

---

## 6. Templates, Types, Blocks

### 6.1 `block` (slot definition)

Defines a named override point inside a type or template:

```
block "visible" {}
block "text" { text = "DEFAULT_LOC_KEY" }
block "datamodel" { datamodel = "[DefaultList]" }
block "extra_info" {}
```

### 6.2 `blockoverride` (slot fill)

Overrides a named block when using a type or template:

```
blockoverride "text" {
    text = "[ProductionMethod.GetNameNoFormatting]"
}
```

Alternate syntax seen: `blockoverride = "identifier" { ... }`

### 6.3 `expand = {}`

Spacer element in `hbox`/`vbox` (like CSS `flex-grow`):

```
vbox = {
    expand = {}
    textbox = { text = "TOP_ALIGNED" }
    expand = {}
}
```

---

## 7. Tooltips

### 7.1 Simple localization key

```
tooltip = "EXPAND"
```

### 7.2 Dynamic expression

```
tooltip = "[Country.GetInfamyDesc]"
tooltip = "[ErrorDeer.GetTooltip]"
```

### 7.3 Raw tooltip (literal text)

```
raw_tooltip = "Current FPS is under 30!"
```

### 7.4 Custom tooltip widget

```
tooltipwidget = {
    FancyTooltip_BuildingType = {}
}
```

### 7.5 Tooltip placement (via templates)

```
using = tooltip_below
using = tooltip_above
using = tooltip_es
using = tooltip_ne
```

---

## 8. Animations & States

### 8.1 `state` block

```
state = {
    name = _show
    next = _idle
    trigger_on_create = yes
    duration = 0.25
    alpha = 1
    position_y = 0
    using = Animation_Curve_Default
    on_start = "[InformationPanelBar.ClosePanel]"
    start_sound = {
        soundeffect = "event:/SFX/UI/SideBar/politics"
    }
}
```

### 8.2 Common state names

`_show`, `_hide`, `_mouse_enter`, `_mouse_leave`, `_mouse_press`, `_mouse_release`, `tutorial_highlight_start`, `show_sidebar_labels`, `hide_sidebar_labels`.

### 8.3 Sound in states

```
start_sound = {
    soundeffect = "event:/SFX/UI/SideBar/politics"
}
start_sound = {
    soundeffect = "snapshot:/Dynamic/mute_world_80"
}
```

Multiple `start_sound` blocks can appear in one state.

### 8.4 State chaining

```
state = { name = 1  next = 2  alpha = 0  trigger_on_create = yes }
state = { name = 2  duration = 0.25  alpha = 1  using = Animation_Curve_Default }
```

---

## 9. `modify_texture` (Texture Layering)

Nested inside widgets to layer/blend textures:

```
modify_texture = {
    texture = "gfx/interface/masks/fade_vertical_center.dds"
    spriteType = Corneredstretched
    spriteborder = { 0 0 }
    blend_mode = alphamultiply
}
```

```
modify_texture = {
    using = texture_velvet
}
```

---

## 10. Panel Navigation API

Confirmed patterns for the information panel system:

```
onclick = "[InformationPanelBar.OpenPanel('politics')]"
onclick = "[InformationPanelBar.OpenPanelCycleTabs('power_bloc_panel', 'default|members|modifiers')]"
onclick = "[InformationPanel.SelectTab('default')]"
onclick = "[InformationPanelBar.OpenPreviousPanel]"
on_start = "[InformationPanelBar.ClosePanel]"
```

---

## 11. Scripted Widget Registration

File: `gui/scripted_widgets/*.txt`

Maps a `.gui` file path to a script trigger name:

```
gui/internationale_gui.gui = internationale_gui_trigger
```

This connects the GUI to the scripted trigger system so the window can be opened/closed from game scripts.

---

## 12. `visible` Patterns

```
visible = yes
visible = no
visible = "[InDebugMode]"
visible = "[And(A, B)]"
visible = "[Not(IsDataModelEmpty(List))]"
visible = "[GetVariableSystem.Exists('tab_name')]"
visible = "[GreaterThan_int32(Value, '(int32)0')]"
visible = "[LessThan_float(GetCurrentFps, '(float)30')]"
visible = "[BuildingType.IsBeingTutorialHighlighted]"
```

---

## 13. Comments

Standard `#` line comments:

```
# This is a comment
size = { 400 300 } # inline comment
```

---

## 14. Quick Reference: Minimal Window

```
window = {
    name = "my_window"
    size = { 500 400 }
    position = { 100 100 }
    layer = windows_layer
    visible = "[GetVariableSystem.Exists('my_window_open')]"

    using = dark_area

    state = {
        name = _show
        using = default_show_properties
    }
    state = {
        name = _hide
        using = default_hide_properties
    }

    vbox = {
        layoutpolicy_horizontal = expanding
        layoutpolicy_vertical = expanding

        textbox = {
            text = "MY_WINDOW_TITLE"
            using = fontsize_xl
            align = center
        }

        expand = {}

        button = {
            size = { 120 35 }
            text = "CLOSE"
            onclick = "[GetVariableSystem.Clear('my_window_open')]"
        }
    }
}
```

---

*Generated from confirmed code in vanilla Victoria 3 v1.8+ and workspace mods. No syntax was assumed beyond what was directly read from files.*
