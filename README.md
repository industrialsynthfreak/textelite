# Pytextelite
Fork of pytextelite code for python 3.

Originally based on [this code](http://automaticromantic.com/static/misc/pytxtelite.txt) which, in turn, uses Ian Bell's Text Elite [C code](http://www.elitehomepage.org/text/index.htm)
Classic Elite galaxy (not Elite+) should be pretty similar to which this code generates (at least system names and their descriptions are correct).

The [ncurses](http://www.gnu.org/software/ncurses/ncurses.html) version is implemented to represent the Classic Elite interface look.

The original text-elite code does not contain any battle or smuggling mechanics, ship upgrades, ratings or missions. I probably will add this parts later.

All cheats removed. Hey, you already have the source codes! Make cheats by yourself.

# Requirements
- python 3 (3.5.0 approved)
- ncurses version: [urwid](http://urwid.org/index.html), but it's already included. I'm not related with urwid lib in any way
- ncurses version: Linux, OSX, Cygwin or other unix-like console

# The ncurses version (preferred)
Run the main app.
```python
python3 app_cursed.py
```
It's recommended to set quite a big console window for this mode (otherwise the galaxy map or/and buttons may be drawn incorrectly)

## Hotkeys
- arrows - move the cursor
- num 1-0 - menu switch
- space - press a button
- esc - quit

# The original version
First, run the main app.
```python
python3 app.py
```
Now you may use console commands for info, trading or travelling. You start at Lave like in the original game.

# TODO
- ship upgrades
- smuggling mechanics
- battle mechanics (?)
- DONE: `ncurses` interface port
