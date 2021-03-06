#!/usr/bin/python3
"""
This is ncurses (urwid) based console interface for textelite.
It should work fine on any modern posix console.
The interface provide more flexibility such as menus, buttons, color schemes.
"""
import argparse

import urwid

from telite import TradingGame

__VERSION__ = '1.0'


class Interface:
    """Console interface class"""
    styles = {
        'dark': [('info', 'dark green', 'black'),
                 ('button', 'light cyan, bold', 'dark blue')],
        'norton': [('info', 'light gray', 'dark blue'),
                   ('button', 'white, bold', 'dark blue')],
        'light': [('info', 'black', 'light gray'),
                  ('button', 'white, bold', 'dark red')]
    }
    palette = styles['dark']
    map_scale = 2

    def __init__(self):
        self.game = TradingGame()

        self._parse_init_args()
        self.question = 'NAME'
        self.selected_system = None
        self.menu = self._create_command_menu()
        self.info_head = urwid.Pile([urwid.Text(u'')])
        self.info = urwid.Pile([urwid.Text(u'')])
        self.screen = urwid.Pile([self.menu, self.info_head, self.info])
        self.button_show_status()
        self.do_question_change_name()
        self.fill = urwid.Filler(self.screen, 'top')
        self.fill = urwid.AttrMap(self.fill, 'info')
        self.loop = urwid.MainLoop(self.fill, palette=self.palette, unhandled_input=self.process_events)
        self.loop.screen.set_terminal_properties(colors=16)

    def run(self):
        """Run the game."""
        self.loop.run()

    @staticmethod
    def do_terminate():
        """Quit the game."""
        raise urwid.ExitMainLoop()

    def process_events(self, key):
        """Keys processing."""
        binds = {
            'esc': self.do_terminate,
            '1': self.button_show_jump,
            '2': self.button_show_sell,
            '3': self.button_show_buy,
            '4': self.button_show_equip,
            '5': self.button_show_galaxy,
            '6': self.button_show_locals,
            '7': self.button_show_planet_info,
            '8': self.button_show_market,
            '9': self.button_show_status,
            '0': self.button_show_cargo,
        }
        if key in binds:
            return binds[key]()

    def process_question(self, edit=None, text=None):
        """Question box text processing (used only for commander's name input)"""
        if text.endswith(' '):
            self.info_head.widget_list.pop(-1)
            self.screen.focus_position = 0
            if self.question == 'NAME':
                self.game.change_name(text[:-1])
                self.button_show_status()
            self.question = None

    def do_question_change_name(self):
        self.question = 'NAME'
        self._show_question_box('Enter your name, commander: ')

    def button_show_jump(self, button=None):
        status, (head, desc) = self.game.info_local_systems()
        menu = self._create_button_list(desc, self.do_jump)
        self._set_screen(urwid.Pile(menu), head)
        self.screen.focus_position = 2

    def do_jump(self, button=None, planet=None):
        status, message = self.game.jump(planet)
        if status:
            self.button_show_galaxy()
        self._set_head(message)

    def button_show_sell(self, button=None):
        self.menu.focus_position = 2
        status, (head, desc) = self.game.info_sell()
        menu = urwid.Pile(self._create_button_list(desc, self.do_sell))
        self._set_screen(menu, head)
        self.screen.focus_position = 2

    def do_sell(self, button=None, name=None):
        focus = self.info.widget_list[-1].focus_position
        status, msg = self.game.sell(name, amt=1)
        if status:
            self.button_show_sell(button)
            focus = min(focus, len(self.info.widget_list[-1].widget_list) - 1)
            self.info.widget_list[-1].focus_position = focus
        self._set_head(msg)

    def button_show_buy(self, button=None):
        status, (head, desc) = self.game.info_buy()
        menu = urwid.Pile(self._create_button_list(desc, self.do_buy))
        self._set_screen(menu, head)
        self.screen.focus_position = 2

    def do_buy(self, button=None, name=None):
        focus = self.info.widget_list[-1].focus_position
        status, msg = self.game.buy(name, amt=1)
        if status:
            self.button_show_buy(button)
            focus = min(focus, len(self.info.widget_list[-1].widget_list) - 1)
            self.info.widget_list[-1].focus_position = focus
        self._set_head(msg)

    def button_show_equip(self, button=None):
        status, (head, desc) = self.game.info_equip()
        menu = urwid.Pile(self._create_button_list(desc, self.do_upgrade))
        self._set_screen(menu, head)
        self.screen.focus_position = 2

    def do_upgrade(self, button=None, name=None):
        if name.lower() == 'fuel':
            status, msg = self.game.buy_fuel()
        else:
            status, msg = self.game.install_upgrade(name.lower())
        if status:
            self.button_show_equip(button)
        self._set_head(msg)

    def button_show_galaxy(self, button=None):
        status, (head, desc) = self.game.info_galaxy(scale=self.map_scale)
        text = urwid.Text('\n'.join(desc))
        b = urwid.Button('Hyperjump!', self.do_hyperjump)
        self._set_screen([b, text], head)
        self.screen.focus_position = 0

    def do_hyperjump(self, button=None):
        status, msg = self.game.hyperjump()
        if status:
            self.button_show_galaxy(button)
        self._set_head(msg)

    def button_show_locals(self, button=None):
        status, (head, desc) = self.game.info_local_systems()
        menu = self._create_button_list(desc, self.button_show_planet_info)
        self._set_screen(urwid.Pile(menu), head)
        self.screen.focus_position = 2

    def button_show_planet_info(self, button=None, name=None):
        if not name:
            name = self.selected_system
        status, message = self.game.info_selected_system(name)
        if status:
            head, info = message
            self._set_screen(urwid.Text('\n'.join(info)), head)
            self.selected_system = name
        else:
            self._set_head(message)
        self.screen.focus_position = 0

    def button_show_market(self, button=None):
        status, (head, desc) = self.game.info_trade()
        menu = urwid.Text('\n'.join(desc))
        self._set_screen(menu, head)
        self.screen.focus_position = 0

    def button_show_status(self, button=None):
        status, (head, desc) = self.game.info_commander()
        menu = urwid.Pile(self._create_button_list(desc, self.do_use))
        self._set_screen(menu, head)
        if not any((d[0] for d in desc)):
            self.screen.focus_position = 0
        else:
            self.screen.focus_position = 2

    def do_use(self, button=None, name=None):
        focus = self.info.widget_list[-1].focus_position
        status, msg = self.game.use_equipment(name)
        if status:
            self.button_show_status(button)
            if len(self.info.widget_list[-1].widget_list) > focus:
                self.info.widget_list[-1].focus_position = focus
        self._set_head(msg)

    def button_show_cargo(self, button=None):
        status, (head, desc) = self.game.info_cargo()
        menu = urwid.Pile(self._create_button_list(desc, self.do_dump))
        self._set_screen(menu, head)
        if not any((d[0] for d in desc)):
            self.screen.focus_position = 0
        else:
            self.screen.focus_position = 2

    def do_dump(self, button=None, name=None):
        focus = self.info.widget_list[-1].focus_position
        status, msg = self.game.dump(name, amt=1)
        if status:
            self.button_show_cargo(button)
            if len(self.info.widget_list[-1].widget_list) > focus:
                self.info.widget_list[-1].focus_position = focus
        self._set_head(msg)

    def _create_command_menu(self):
        """Construct the game menu buttons."""
        f1 = urwid.Button('Jump', on_press=self.button_show_jump)
        f2 = urwid.Button('Sell', on_press=self.button_show_sell)
        f3 = urwid.Button('Buy', on_press=self.button_show_buy)
        f4 = urwid.Button('Upgrade', on_press=self.button_show_equip)
        f5 = urwid.Button('Galaxy', on_press=self.button_show_galaxy)
        f6 = urwid.Button('Locals', on_press=self.button_show_locals)
        f7 = urwid.Button('System', on_press=self.button_show_planet_info)
        f8 = urwid.Button('Market', on_press=self.button_show_market)
        f9 = urwid.Button('Status', on_press=self.button_show_status)
        f0 = urwid.Button('Cargo', on_press=self.button_show_cargo)
        buttons = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f0]
        buttons = (urwid.AttrMap(b, 'button') for b in buttons)
        menu = urwid.Columns(buttons)
        menu.focus_position = 8
        return menu

    def _show_question_box(self, text):
        """Construct a question box with a text input."""
        question = urwid.Edit(text)
        self.info_head.widget_list.append(question)
        urwid.connect_signal(question, 'change', self.process_question)
        self.screen.focus_position = 1
        self.info_head.focus_position = 1

    def _create_button_list(self, data, function):
        """Construct a vertical list of buttons."""
        buttons = []
        for status, msg in data:
            if status:
                n, d = msg
                buttons.append(urwid.Button(d, on_press=function, user_data=n))
            else:
                buttons.append(urwid.Text(msg))
        return buttons

    def _set_head(self, new_head):
        self.info_head.widget_list = [urwid.Text(new_head.upper())]

    def _set_screen(self, new_menu, new_head):
        if isinstance(new_menu, list):
            self.info.widget_list = new_menu
        else:
            self.info.widget_list = [new_menu]
        self._set_head(new_head)

    def _parse_init_args(self):
        """Argparse function."""
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-s", help="specify a visual style: %s" % ', '.join(self.styles.keys()))
        argparser.add_argument("-m", help="specify the galaxy map scale, %d is default" % self.map_scale, type=int)
        args = argparser.parse_args()
        if args.s and args.s in self.styles:
            self.palette = self.styles[args.s]
        if args.m and 1 <= args.m <= 4:
            self.map_scale = args.m


if __name__ == "__main__":
    I = Interface()
    I.run()
