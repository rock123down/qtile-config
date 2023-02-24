#!/usr/bin/env bash

#nitrogen --restore &

nm-applet &

/usr/bin/emacs --daemon &

feh --randomize --bg-fill $HOME/Pictures/*

xset s off
