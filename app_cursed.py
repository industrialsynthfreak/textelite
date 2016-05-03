#!/usr/bin/python3
import urwid

from telite import TradingGame


class Interface:
    styles = {
        'dark': [('info', 'dark green', 'black'),
                 ('button', 'light cyan', 'dark blue')],
        'light': [('info', 'black', 'light gray'),
                  ('button', 'light red', 'light gray')]
    }
    palette = None

    def _create_command_menu(self):
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

    def _set_palette(self, palette: str):
        self.palette = self.styles.get(palette)

    def _show_question_box(self, text):
        question = urwid.Edit(text)
        self.info_head.widget_list.append(question)
        urwid.connect_signal(question, 'change', self.process_question)
        self.screen.focus_position = 1
        self.info_head.focus_position = 1

    def _create_button_list(self, data, function):
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
        self.info.widget_list = [new_menu]
        self._set_head(new_head)

    def process_events(self, key):
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
        if text.endswith(' '):
            self.info_head.widget_list.pop(-1)
            self.screen.focus_position = 0
            if self.question == 'NAME':
                self.game.change_name(text[:-1])
                self.button_show_status()
            self.question = None

    @staticmethod
    def do_terminate():
        raise urwid.ExitMainLoop()

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
            self.info.widget_list[-1].focus_position = focus
        self._set_head(msg)

    def button_show_equip(self, button=None):
        status, (head, desc) = self.game.info_equip()
        menu = urwid.Pile(self._create_button_list(desc, self.do_upgrade))
        self._set_screen(menu, head)
        self.screen.focus_position = 2

    def do_upgrade(self, button=None, name=None):
        status, msg = False, None
        if name.lower() == 'fuel':
            status, msg = self.game.buy_fuel()
        if status:
            self.button_show_equip(button)
        self._set_head(msg)

    def button_show_galaxy(self, button=None):
        status, (head, desc) = self.game.info_galaxy()
        text = urwid.Text('\n'.join(desc))
        self._set_screen(text, head)
        self.screen.focus_position = 0

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

    def button_show_status(self, button=None):
        status, (head, desc) = self.game.info_commander()
        menu = urwid.Text('\n'.join(desc))
        self._set_screen(menu, head)
        self.screen.focus_position = 0

    def button_show_market(self, button=None):
        status, (head, desc) = self.game.info_trade()
        text = urwid.Text('\n'.join(desc))
        self._set_screen(text, head)
        self.screen.focus_position = 0

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

    def do_question_change_name(self):
        self.question = 'NAME'
        self._show_question_box('Enter your name, commander: ')

    def __init__(self):
        self.question = 'NAME'
        self.game = TradingGame()
        self.selected_system = None
        self.menu = self._create_command_menu()
        self.info_head = urwid.Pile([urwid.Text(u'')])
        self.info = urwid.Pile([urwid.Text(u'')])
        self.screen = urwid.Pile([self.menu, self.info_head, self.info])
        self.button_show_status()
        self.do_question_change_name()
        self._set_palette('dark')
        self.fill = urwid.Filler(self.screen, 'top')
        self.fill = urwid.AttrMap(self.fill, 'info')
        self.loop = urwid.MainLoop(self.fill, palette=self.palette, unhandled_input=self.process_events)
        self.loop.screen.set_terminal_properties(colors=16)

    def run(self):
        self.loop.run()


if __name__ == "__main__":
    I = Interface()
    I.run()
