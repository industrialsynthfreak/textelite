#!/usr/bin/python3
"""
This is a classic console interface for textelite.
You may enter game commands in the command line.
"""
from cmd import Cmd

from telite import TradingGame

__VERSION__ = '1.0'


class TradingGameCmd(Cmd):
    """Command interface to a TradingGame"""
    prompt = "> "

    def __init__(self, debug=False):
        self.debug = debug
        Cmd.__init__(self)
        self.game = TradingGame()
        self.set_prompt()

    def set_prompt(self):
        self.prompt = 'Cash : %0.2f>' % self.game.ship.cash

    @staticmethod
    def do_intro(line):
        print(
            '''
            Welcome to pyElite {version}
            Available commands:

            /// CONTROLS ///
            info  (or i) [planet name]         - planet information
            buy   (or b) [trade good] [amount] - buy from a local store
            sell  (or s) [trade good] [amount] - sell to a local store
            fuel  (or f) [amount]              - buy amount LY of fuel
            jump  (or j) [planet name]         - hyperjump
            use   (or u) [equipment name]      - use installed equipment
            dump [trade good] [amount]         - dump cargo into space
            upgrade [upgrade name]             - buy and install upgrade
            local (or l) - list of planets within the ship hyperjump range
            mkt   (or m) - show local market
            cargo (or c) - show cargo bay
            com          - commander status
            galhyp       - jump to the next galaxy

            /// OTHER /////
            intro (or h)   - display this text
            quit  (or q)   - quit the game
            run [filepath] - run a script (one command per line)
            '''.format(version=__VERSION__)
        )

    @staticmethod
    def do_quit(line):
        print("Goodbye, commander!")
        return True

    @staticmethod
    def do_q(line):
        return TradingGameCmd.do_quit(line)

    @staticmethod
    def do_EOF(line):
        return True

    def do_jump(self, planetname):
        status, msg = self.game.jump(planetname.strip())
        print(msg)
        self.do_info('')
        return

    def do_j(self, planetname):
        return self.do_jump(planetname)

    def do_local(self, line):
        print("Galaxy number %d" % self.game.galaxy.galaxy_number)
        status, (head, choices) = self.game.info_local_systems()
        print(head.upper())
        for __, (name, desc) in choices:
            print(''.join(desc))
        return

    def do_l(self, line):
        return self.do_local(line)

    def do_galhyp(self, line):
        status, ret = self.game.hyperjump()
        print(ret)
        return

    def do_mkt(self, line):
        status, (head, data) = self.game.info_trade()
        print(head.upper())
        for g in data:
            print(g)
        print("Fuel : {f}   Holdspace : {s}".format(
            f=self.game.ship.fuel / 10.0, s=self.game.ship.hold_remaining))
        return

    def do_m(self, line):
        return self.do_mkt(line)

    def do_sell(self, line):
        v = self._check_good(line)
        if not v:
            return
        name, amt = v
        status, msg = self.game.sell(name, amt)
        print(msg)
        self.set_prompt()
        return

    def do_s(self, line):
        return self.do_sell(line)

    def do_buy(self, line):
        v = self._check_good(line)
        if not v:
            return
        name, amt = v
        status, msg = self.game.buy(name, amt)
        print(msg)
        self.set_prompt()
        return

    def do_b(self, line):
        return self.do_buy(line)

    def do_fuel(self, line):
        status, msg = self.game.buy_fuel()
        print(msg)
        self.set_prompt()
        return

    def do_f(self, line):
        return self.do_fuel(line)

    def do_info(self, systemname):
        status, msg = self.game.info_selected_system(systemname)
        if status:
            (head, info) = msg
            print(head.upper())
            print('\n'.join(info))
        else:
            print(msg)
        return

    def do_i(self, name):
        return self.do_info(name)

    def do_com(self, line):
        status, msg = self.game.info_commander()
        if status:
            head, info = msg
            print(head.upper())
            for __, desc in info:
                if __:
                    name, desc = desc
                print(''.join(desc))
        return

    def do_cargo(self, line):
        status, msg = self.game.info_cargo()
        if status:
            head, info = msg
            print(head.upper())
            for __, desc in info:
                if __:
                    name, desc = desc
                print(''.join(desc))
        return

    def do_c(self, line):
        return self.do_cargo(line)

    def do_dump(self, line):
        v = self._check_good(line)
        if not v:
            return
        name, amt = v
        status, msg = self.game.dump(name, amt)
        print(msg)
        return

    def do_upgrade(self, line):
        status, msg = self.game.install_upgrade(line)
        print(msg)
        return

    def do_use(self, line):
        status, msg = self.game.use_equipment(line)
        print(msg)
        return

    def do_u(self, line):
        return self.do_use(line)

    def do_run(self, fname):
        import os
        if os.path.isfile(fname):
            lines = open(fname, 'r').read().split('\n')
            for line in lines:
                print(line)
                self.onecmd(line)
                print("Cash > ", self.game.ship.cash)
        else:
            print("Could not open file")
        return

    @staticmethod
    def do_h(line):
        return TradingGameCmd.do_intro(line)

    @staticmethod
    def _check_value(value):
        try:
            value = float(value)
        except ValueError:
            print("Value must be a number")
            return None
        if value <= 0:
            print("Nice try pilot.")
            return None
        else:
            return value

    def _check_good(self, line):
        """
        :param str line:
        :return iterable:
        """
        line = line.strip().lower()

        try:
            good, number = line.split(' ')
        except ValueError:
            good = line
            amt = 9999
        else:
            amt = self._check_value(number)
            if not amt:
                return False
            amt = int(amt)
        return good, amt


if __name__ == "__main__":
    tg = TradingGameCmd()
    tg.do_intro('')
    tg.cmdloop()
