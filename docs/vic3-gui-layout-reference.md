# Vic3 GUI Layout Reference

A practical guide to spacing, margin, alignment, and anchoring in the Clausewitz GUI system, written from hard experience.

---

## Container Types

Before anything else, you need to know which container you are working in — the layout rules change completely depending on the type.

| Container | Layout behavior |
|-----------|----------------|
| `widget` | **Flat/absolute.** Children stack on top of each other at {0,0} unless repositioned. No automatic flow. |
| `hbox` | **Horizontal flow.** Children placed left-to-right automatically. |
| `vbox` | **Vertical flow.** Children placed top-to-bottom automatically. |
| `flowcontainer` | Like hbox/vbox but wraps. Set `direction = horizontal` or `direction = vertical`. |
| `scrollarea` | Wraps a `scrollwidget`, which wraps a flow container. |

---

## spacing

Only works in flow containers (hbox, vbox, flowcontainer). Sets the gap in pixels between each child.

```
hbox = {
    spacing = 10      # 10px gap between each child
}
```

Has no effect inside a flat `widget`.

---

## margin

Sets internal padding inside any container. Children are pushed inward.

```
# Two values: { horizontal vertical }
margin = { 14 10 }     # 14px left+right, 10px top+bottom

# Four values: { left top right bottom }
margin = { 10 5 10 5 }
```

Unlike CSS, margin here is INWARD padding (what CSS calls `padding`). There is no equivalent of CSS `margin` (outward spacing from the element itself) — use `spacing` on the parent instead.

---

## size

```
size = { 540 360 }      # fixed: 540px wide, 360px tall
size = { 50% 360 }      # 50% of parent width, 360px tall
size = { 100% 100% }    # fill parent entirely
size = { 0 360 }        # used with layoutpolicy_horizontal = expanding (see below)
```

**Percentage sizes only work if the parent has a known pixel width.** If the parent uses `layoutpolicy_horizontal = expanding` with `size = { 0 H }`, percentage children inside it work correctly because the parent's size is resolved at layout time.

---

## layoutpolicy

Controls how a widget behaves in a flow container when there is leftover space.

```
layoutpolicy_horizontal = expanding    # stretch to fill available horizontal space
layoutpolicy_vertical = expanding      # stretch to fill available vertical space
```

The canonical pattern for "fill remaining width":
```
widget = {
    layoutpolicy_horizontal = expanding
    size = { 0 360 }     # 0 width = resolved by layoutpolicy, 360 fixed height
}
```

You need BOTH the `layoutpolicy` AND `size = { 0 H }`. Using only `size = { 100% H }` inside an hbox gives you a fixed percentage, not a "fill rest" behavior.

---

## parentanchor

This is where things get weird. `parentanchor` tells the system **which point of the parent** the child's corresponding edge/corner aligns to.

```
parentanchor = right           # child's right edge → parent's right edge
parentanchor = bottom          # child's bottom edge → parent's bottom edge
parentanchor = hcenter         # child's horizontal center → parent's horizontal center
parentanchor = vcenter         # child's vertical center → parent's vertical center
parentanchor = center          # shorthand for hcenter|vcenter
parentanchor = top|right       # child's top-right corner → parent's top-right corner
parentanchor = left|vcenter    # child's left edge, vertically centered in parent
```

Combine values with `|`:
```
parentanchor = hcenter|vcenter    # centered in both axes (most common)
parentanchor = top|right          # stuck to top-right corner
```

### parentanchor in flat `widget` containers

This is the main use case and it works predictably:

```
widget = {
    size = { 1280 360 }

    # LEFT portrait: sits at top-left (default, no parentanchor needed)
    character_portrait = { size = { 270 360 } }

    # RIGHT portrait: right edge aligns to parent's right edge
    character_portrait = { size = { 270 360 } parentanchor = right }

    # Centered element
    textbox = { size = { 400 40 } parentanchor = hcenter }
}
```

### parentanchor in hbox / vbox

**Only the cross-axis anchor has any effect.** In an `hbox`, horizontal position is controlled by the layout flow — `parentanchor = left/right/hcenter` is ignored. Only vertical anchors (`top`, `bottom`, `vcenter`) work.

```
hbox = {
    size = { 0 60 }
    layoutpolicy_horizontal = expanding

    icon = {
        size = { 32 32 }
        parentanchor = vcenter    # works: centers vertically in the hbox
        parentanchor = right      # IGNORED: hbox controls horizontal position
    }
}
```

### The flat widget inversion trap

If you have two 50%-wide hboxes side by side inside a flat `widget`, and you try to push the second one to the right with `parentanchor = right`:

```
# BROKEN: the right hbox appears on the LEFT
widget = {
    size = { 100% 360 }
    hbox = { size = { 50% 360 }  ...left content... }
    hbox = { size = { 50% 360 } parentanchor = right  ...right content... }
}
```

This breaks because in a flat `widget`, both hboxes default to position {0,0}. The second hbox overlaps the first. Adding `parentanchor = right` places the second hbox's right edge at the parent's right — but its children still lay out LEFT-TO-RIGHT from the hbox's own left edge, which is now at 50%.

**Use `position = { 50% 0 }` instead:**

```
# WORKS: second hbox starts at exactly the midpoint
widget = {
    size = { 100% 360 }
    hbox = { size = { 50% 360 }  ...left content... }
    hbox = { size = { 50% 360 } position = { 50% 0 }  ...right content... }
}
```

---

## position

Offsets a widget from where it would naturally sit (either {0,0} for flat containers, or the flow position in hbox/vbox, or the anchor point set by `parentanchor`).

```
position = { 10 -5 }     # 10px right, 5px up
position = { 50% 0 }     # 50% of parent width to the right, no vertical offset
position = { -4 4 }      # nudge: 4px left, 4px down
```

### position + parentanchor together

`position` is applied AFTER `parentanchor` resolves. Use this to fine-tune:

```
widget = {
    size = { 200 40 }
    parentanchor = right|top
    position = { -8 8 }     # 8px inset from right, 8px down from top
}
```

### NEVER use position for major layout

`position` moves a widget without affecting any other element's layout. It does not push siblings around. Use it only for small adjustments and overlays, not to position primary content.

---

## align (text only)

Only applies to `textbox`. Controls text alignment within the textbox bounds.

```
align = hcenter            # horizontally centered
align = left               # left-aligned
align = right              # right-aligned
align = nobaseline         # disable baseline grid (almost always needed for correct vertical positioning)
align = hcenter|nobaseline # combined
```

`nobaseline` removes the Vic3 internal baseline offset. Without it, text often sits a few pixels too low. **Always use `nobaseline` unless you explicitly need baseline alignment.**

---

## minimumsize / maximumsize

Clamp the resolved size of a widget:

```
minimumsize = { 0 90 }     # at least 90px tall, no minimum width
maximumsize = { 600 -1 }   # at most 600px wide, no maximum height (-1 = unclamped)
```

---

## Common patterns

### Fill remaining width in hbox
```
hbox = {
    layoutpolicy_horizontal = expanding
    size = { 0 50 }

    icon = { size = { 32 32 } parentanchor = vcenter }

    # this widget takes all remaining horizontal space
    textbox = {
        layoutpolicy_horizontal = expanding
        size = { 0 50 }
    }

    button = { size = { 80 40 } parentanchor = vcenter }
}
```

### Center something inside a flat widget
```
widget = {
    size = { 600 300 }

    vbox = {
        parentanchor = center    # hcenter|vcenter
        spacing = 8
        textbox = { ... }
        button = { ... }
    }
}
```

### Overlay element at a corner
```
widget = {
    size = { 400 300 }

    # main content
    ...

    # badge at top-right, 8px inset
    icon = {
        size = { 32 32 }
        parentanchor = top|right
        position = { -8 8 }
    }
}
```

### Two equal columns in a flat widget
```
widget = {
    size = { 100% 400 }

    hbox = {
        size = { 50% 400 }
        # left column content
    }

    hbox = {
        size = { 50% 400 }
        position = { 50% 0 }    # offset by 50% of parent width
        # right column content
    }
}
```

### Portrait right-aligned (vanilla battle.gui pattern)
```
widget = {
    size = { 540 360 }

    character_portrait_front_vs_left = {
        # left portrait: sits at {0,0} by default
    }

    character_portrait_front_vs_right = {
        parentanchor = right    # right edge of portrait → right edge of parent
    }
}
```

---

## Known bugs / gotchas

- `parentanchor = right|vcenter` — the combined value is **not supported** in most contexts. Use `parentanchor = right` alone and accept the vertical default, or use `position` to compensate.
- `position = { 0 -100 }` in a vbox inside a flow panel will push text **above the visible area** of its parent. Don't use negative position for major layout.
- `size = { 50% H }` inside an `hbox` gives you a fixed percentage of the hbox's resolved width. But if the hbox is itself `layoutpolicy_horizontal = expanding` with `size = { 0 H }`, the 50% resolves correctly at layout time.
- In flat `widget` containers, all children default to position `{0,0}` — they overlap. You must manually position everything.
- `expand = {}` inside a vbox/hbox acts like a spacer that consumes all remaining space, similar to CSS `flex-grow: 1`.
