#!/bin/sh
FONT='ohsnap-9'
conky -c "./.config/herbstluftwm/conkyrc" | dzen2 -bg "#2a2437" -ta right -w 1280 -h 14 -x 0 -y -1 -fn $FONT &
exit
