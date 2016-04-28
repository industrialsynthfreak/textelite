#!/usr/bin/python
from cmd import Cmd

from telite import TradingGame

__VERSION__ = '1.0'


class TradingGameCmd(Cmd):
    """Command interface to a TradingGame"""
    prompt = "> "

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
            amt = int(amt + 1)

        if not good:
            print('You must specify trade good')
            return False
        for commodity in self.game.localmarket.commodities:
            if commodity.name.lower().startswith(good):
                return commodity, amt
        else:
            print("Unknown trade good")
            return False

    def __init__(self, debug=False):
        self.debug = debug
        Cmd.__init__(self)
        self.game = TradingGame()
        self.set_prompt()

    def set_prompt(self):
        self.prompt = 'Cash : %0.2f>' % self.game.ship.cash

    def do_jump(self, planetname):
        ret = self.game.jump(planetname.strip())
        self.do_info('')
        return ret

    def do_j(self, planetname):
        return self.do_jump(planetname)

    def do_local(self, line):
        print("Galaxy number %d" % self.game.galaxy.galaxy_number)
        system_list = self.game.galaxy.systems_within(self.game.current_system, self.game.ship.maxfuel)
        system_list.sort(key=lambda x: x[0])  # Smallest first
        for distance, planet_sys in system_list:
            if distance <= self.game.ship.fuel:
                i = " * "
            else:
                i = "-"
            print("{i:2}{d:<8.1f} {desc}".format(i=i, d=distance / 10., desc=planet_sys.description(short=True)))

    def do_l(self, line):
        return self.do_local(line)

    def do_galhyp(self, line):
        ret = self.game.next_galaxy()
        print("You appear in galaxy %d" % self.game.galaxy.galaxy_number)
        return ret

    def do_mkt(self, line):
        self.game.display_market()
        print("Fuel : {f}   Holdspace : {s}".format(f=self.game.ship.fuel / 10.0, s=self.game.ship.hold_remaining))

    def do_m(self, line):
        return self.do_mkt(line)

    def do_sell(self, line):
        v = self._check_good(line)
        if not v:
            return
        res = self.game.sell(*v)
        self.set_prompt()
        return res

    def do_s(self, line):
        return self.do_sell(line)

    def do_buy(self, line):
        v = self._check_good(line)
        if not v:
            return
        self.game.buy(*v)
        self.set_prompt()
        return

    def do_b(self, line):
        return self.do_buy(line)

    def do_fuel(self, line):
        ly = self._check_value(line)
        if ly:
            print(self.game.buy_fuel(ly * 10))
            self.set_prompt()
        return

    def do_f(self, line):
        return self.do_fuel(line)

    def do_info(self, systemname):
        psystem = self.game.galaxy.closest_system_like(self.game.current_system, systemname)
        if psystem is None:
            print("System {name} could not be found.".format(name=systemname))
        else:
            print(psystem)
        return

    def do_i(self, name):
        return self.do_info(name)

    def do_com(self, line):
        print(self.game.ship)
        return

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

    @staticmethod
    def do_intro(line):
        print(
            '''
            Welcome to pyElite {version}
            Available commands:

            /// CONTROLS ///
            info  (or i) [planetname]          - planet information
            buy   (or b) [tradegood] [amount]  - buy from a local store
            sell  (or s) [tradegood] [amount]  - sell to a local store
            fuel  (or f) [amount]              - buy amount LY of fuel
            jump  (or j) [planetname]          - hyperjump
            local (or l) - list of planets within the ship hyperjump range
            mkt   (or m) - show local market
            com          - commander status
            galhyp       - jump to a next galaxy

            /// OTHER /////
            intro (or h)   - display this text
            quit  (or q)   - quit the game
            run [filepath] - run a script (one command per line)
            '''.format(version=__VERSION__)
        )

    @staticmethod
    def do_h(line):
        return TradingGameCmd.do_intro(line)


if __name__ == "__main__":
    tg = TradingGameCmd()
    tg.do_intro('')
    tg.cmdloop()
