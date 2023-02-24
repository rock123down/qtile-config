# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile

import os
import subprocess

home = os.path.expanduser('~')
mod = "mod4"
terminal = guess_terminal()


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.client_new
def follow_window(client):
    for group in groups:
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[group.name]
            targetgroup.cmd_toscreen(toggle=False)
            break

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Brightness Control
    #Key([], "XF86MonBrightnessUp", lazy.spawn("backlight_control +10"), desc="incesase brightness by 10%"),
    #Key([], "XF86MonBrightnessDown", lazy.spawn("backlight_control -10"), desc="descrease brightness by 10%"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+"), desc="incesase brightness by 10%"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-"), desc="descrease brightness by 10%"),

    # Volume control
    #Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="incesase brightness by 10%"),
    #Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="descrease brightness by 10%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5"), desc="incesase brightness by 10%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5"), desc="descrease brightness by 10%"),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t"), desc="descrease brightness by 10%"),


    # Launch pcmanfm
    Key([mod], "f", lazy.spawn("pcmanfm"), desc="launch pcmanfm"),

    # Launch qutebrowser
    Key([mod, "shift"], "b", lazy.spawn("qutebrowser"), desc="launch browser"),

    # Launch Brvae
    Key([mod], "b", lazy.spawn("firefox"), desc="Launch Firefox Browser"),

    # Launch Dmenu
    Key([mod, "shift"], "p", lazy.spawn("dmenu_run -p 'Run: '"),
        desc='Run Launcher'),

    # Launch slock
    Key([mod], "l", lazy.spawn("slock"), desc='Run slock'),

    # Emacs programs launched using the key chord mod+e followed by 'key'
    KeyChord([mod], "e", [
        Key([], "e", lazy.spawn("emacsclient -c -a 'emacs'")),
        Key([], "b", lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"), desc="Launch ibuffer"),
        Key([], "d", lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"), desc='Launch dired inside Emacs'),
        Key([], "i", lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"), desc='Launch erc inside Emacs'),
        Key([], "m", lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"), desc='Launch mu4e inside Emacs'),
        Key([], "n", lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"), desc='Launch elfeed inside Emacs'),
        Key([], "s", lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"), desc='Launch the eshell inside Emacs'),
        Key([], "v", lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"), desc='Launch vterm inside Emacs'),
        ]),

    # Dmenu Propmpts
    KeyChord([mod], "p",[
        Key([], "h", lazy.spawn("dm-hub")),
        Key([], "a", lazy.spawn("dm-sounds")),
        Key([], "b", lazy.spawn("dm-setbg")),
        Key([], "c", lazy.spawn("dm-colpick")),
        Key([], "e", lazy.spawn("dm-confedit")),
        Key([], "i", lazy.spawn("dm-maim")),
        Key([], "k", lazy.spawn("dm-kill")),
        Key([], "m", lazy.spawn("dm-man")),
        Key([], "n", lazy.spawn("dm-note")),
        Key([], "o", lazy.spawn("dm-bookman")),
        Key([], "p", lazy.spawn("passmenu")),
        Key([], "q", lazy.spawn("dm-logout")),
        Key([], "r", lazy.spawn("dm-reddit")),
        Key([], "s", lazy.spawn("dm-websearch")),
        Key([], "t", lazy.spawn("dm-translate")),
    ]),
]

# groups = [Group(i) for i in "123456789"]
#
# for i in groups:
#     keys.extend(
#         [
#             # mod1 + letter of group = switch to group
#             Key(
#                 [mod],
#                 i.name,
#                 lazy.group[i.name].toscreen(),
#                 desc="Switch to group {}".format(i.name),
#             ),
#             # mod1 + shift + letter of group = switch to & move focused window to group
#             Key(
#                 [mod, "shift"],
#                 i.name,
#                 lazy.window.togroup(i.name, switch_group=True),
#                 desc="Switch to & move focused window to group {}".format(i.name),
#             ),
#             # Or, use below if you prefer not to switch to that group.
#             # # mod1 + shift + letter of group = move focused window to group
#             # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
#             #     desc="move focused window to group {}".format(i.name)),
#         ]
#     )

groups = [
    Group("1", matches = [Match(wm_class=[""])]),
    Group("2", matches = [Match(wm_class=["firefox", ""])]),
    Group("3", matches = [Match(wm_class=[""])]),
    Group("4", matches = [Match(wm_class=[""])]),
    Group("5", matches = [Match(wm_class=["virt-manager"])]),
    Group("6", matches = [Match(wm_class=[""])]),
    Group("7", matches = [Match(wm_class=["deadbeef"])]),
    Group("8", matches = [Match(wm_class=["mpv", "vlc"])]),
    Group("9", matches = [Match(wm_class=[""])]),
]

def toscreen(qtile, group_name):
    if group_name  == qtile.current_screen.group.name:
        qtile.current_screen.set_group(qtile.current_screen.previous_group)
    else:
        for i in range(len(qtile.groups)):
            if group_name == qtile.groups[i].name:
                qtile.current_screen.set_group(qtile.groups[i])
                break

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        # Key([mod]), i.name, lazy.group[i.name].toscreen(),
        # switch to group with ability to go to previous group if pressed again
        Key([mod], i.name, lazy.function(toscreen, i.name),
            desc="Switch to & move focused window to group {}".format(i.name)),

        #mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ]),

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=3,
                   margin=5,
                   border_on_single=True,
                   border_normal='#220000',
                   border_focus='#881111'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

widget_defaults = dict(
    font="Source Code Pro",
    fontsize=12,
    padding=2,
    background=colors[1]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                    background = colors[0]),
                widget.Image(
                    filename = '~/.config/qtile/icons/python.png',
                    scale = 'False',
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
                ),
                widget.GroupBox(
                    font = "Source Code Pro",
                    fontsize=14,
                    margin_y = 3,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors[3],
                    inactive = colors[7],
                    rounded = True,
                    highlight_color = colors[1],
                    highlight_method = "line",
                    this_current_screen_border = colors[6],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[6],
                    other_screen_border = colors[4],
                    foreground = colors[2],
                    background = colors[0]),
                widget.Prompt(
                    font = 'Source Code Pro',
                    padding = 10,
                    fontsize = 14,),
                widget.Sep(
                    linewidth = 0,
                    padding = 10,
                    foreground = colors[2],
                    #background = colors[0],
                ),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                 widget.TextBox(
                    text = '',
                    #background = colors[0],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37),
                widget.TextBox(
                    text = 'Uptime:',
                    background = colors[5],
                    foreground = colors[1],
                    fontsize = 14
                ),
                widget.GenPollText(
                    update_interval = 1,
                    func = lambda: subprocess.check_output(os.path.expanduser(home + "/.local/bin/upt")).decode('utf-8').strip(),
                    background = colors[5],
                    foreground = colors[1],
                    fontsize = 14,),
               widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37),
                widget.CPU(
                    foreground = colors[1],
                    background = colors[4],
                    threshold = 98,
                    padding = 5,
                    update_interval = 1.0,
                    fontsize = 14,),
               widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37),
                widget.CheckUpdates(
                    displaay_format = '{updates}',
                    distro = 'Arch_checkupdates',
                    color_have_update=colors[3],
                    color_no_update=colors[1],
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
                    update_interval = 3600,
                    background = colors[5],
                    foreground = colors[1],
                    fontsize = 14,),
                widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37),
                widget.GenPollText(
                    update_interval = 1,
                    func = lambda: subprocess.check_output(os.path.expanduser(home + "/.local/bin/vol")).decode('utf-8').strip(),
                    background = colors[4],
                    foreground = colors[1],
                    fontsize = 14,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37),
                widget.TextBox(
                    text = 'Barightness:',
                    background = colors[5],
                    foreground = colors[1],
                    fontsize = 14,
                ),
                widget.Backlight(
                    backlight_name = 'amdgpu_bl1',
                    format = '{percent:2.0%}',
                    foreground = colors[1],
                    background = colors[5],
                    fontsize = 14,
                    ),
                widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37
                ),
                widget.TextBox(
                    text = 'Bat:',
                    background = colors[4],
                    foreground = colors[1],
                    fontsize = 14,
                ),
                widget.Battery(
                    charge_char = 'CHG',
                    discharge_char = 'DIS',
                    update_interval = 0.2,
                    format = '{char}->{percent:2.0%}',
                    foreground = colors[1],
                    background = colors[4],
                    fontsize = 14,
                    ),
                widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37
                ),
                widget.Clock(
                    format="%a, %b %d %G, %I:%M %p",
                    background=colors[5],
                    foreground=colors[1],
                    fontsize=14,
                ),
                widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37
                ),
                widget.CurrentLayout(
                    foreground=colors[1],
                    background=colors[4],
                    padding=5,
                    fontsize=14,
                ),
                widget.Systray(
                    padding=1,
                    fontsize=14,
                    background=colors[0],
                ),
                #widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
    ]
)
auto_fullscreen = False
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
