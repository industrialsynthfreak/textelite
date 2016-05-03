from collections import namedtuple, OrderedDict


class Randomizer:
    """
    Randomizer class combines both sas and lcc algorithms from the original code.
    The type of used algorithm should be specified in class .algorithm attribute.
    Should be used as class only.
    """
    next = 12345
    lr = 12345 - 1
    algorithm = 'sas'

    @classmethod
    def lcc(cls):
        cls.next = (214013 * cls.next + 2531011)
        return (cls.next >> 16) & 0x7fff

    @classmethod
    def sas(cls):
        r = (((((((((((cls.lr << 3) - cls.lr) << 3) + cls.lr) << 1) + cls.lr) << 4) - cls.lr) << 1) - cls.lr) + 0xe60)
        r &= 0x7fffffff
        cls.lr -= 1
        return r

    @classmethod
    def get_value(cls):
        """Returns a specific pseudo-random value"""
        if cls.algorithm == 'lcc':
            return cls.lcc()
        elif cls.algorithm == 'sas':
            return cls.sas()
        else:
            return 1


class NameGenerator:
    """
    Should be used as class only.
    """
    pairs0 = "ABOUSEITILETSTONLONUTHNO"
    pairs = "..LEXEGEZACEBISOUSESARMAINDIREA.ERATENBERALAVETIEDORQUANTEISRION"
    pairs1 = pairs0 + pairs

    @classmethod
    def get_name(cls, sample, special_set=False):
        """Returns a name string from a sample of random integers
        :param iterable sample: sample of random integers
        :param bool special_set: defines whether .pairs1 should be used (for non-planet names)
        """
        name = ''
        if special_set:
            pairs = cls.pairs1
        else:
            pairs = cls.pairs
        for s in sample:
            i = s & 0x3e
            name += pairs[i:i + 2]
        return name.replace('.', '')


class PlanSys:
    """A planetary system"""
    economy_types = ("Rich Industrial", "Industrial Ind",
                     "Poor Industrial", "Industrial Ind",
                     "Mainly Agricultural", "Rich Agricultural",
                     "Average Agricultural", "Poor Agricultural")
    gov_types = ("Anarchy", "Feudal", "Multi-government", "Dictatorship", "Communist",
                 "Confederacy", "Democracy", "Corporate State")
    goatsoup_template = "\x8F is \x97."
    desc_list = {
        "\x81": ["fabled", "notable", "well known", "famous", "noted"],
        "\x82": ["very", "mildly", "most", "reasonably", ""],
        "\x83": ["ancient", "\x95", "great", "vast", "pink"],
        "\x84": ["\x9E \x9D plantations", "mountains", "\x9C", "\x94 forests", "oceans"],
        "\x85": ["shyness", "silliness", "mating traditions", "loathing of \x86", "love for \x86"],
        "\x86": ["food blenders", "tourists", "poetry", "discos", "\x8E"],
        "\x87": ["talking tree", "crab", "bat", "lobst", "\xB2"],
        "\x88": ["beset", "plagued", "ravaged", "cursed", "scourged"],
        "\x89": ["\x96 civil war", "\x9B \x98 \x99s", "a \x9B disease", "\x96 earthquakes", "\x96 solar activity"],
        "\x8A": ["its \x83 \x84", "the \xB1 \x98 \x99", "its inhabitants' \x9A \x85", "\xA1", "its \x8D \x8E"],
        "\x8B": ["juice", "brandy", "water", "brew", "gargle blasters"],
        "\x8C": ["\xB2", "\xB1 \x99", "\xB1 \xB2", "\xB1 \x9B", "\x9B \xB2"],
        "\x8D": ["fabulous", "exotic", "hoopy", "unusual", "exciting"],
        "\x8E": ["cuisine", "night life", "casinos", "sit coms", " \xA1 "],
        "\x8F": ["\xB0", "The planet \xB0", "The world \xB0", "This planet", "This world"],
        "\x90": ["n unremarkable", " boring", " dull", " tedious", " revolting"],
        "\x91": ["planet", "world", "place", "little planet", "dump"],
        "\x92": ["wasp", "moth", "grub", "ant", "\xB2"],
        "\x93": ["poet", "arts graduate", "yak", "snail", "slug"],
        "\x94": ["tropical", "dense", "rain", "impenetrable", "exuberant"],
        "\x95": ["funny", "wierd", "unusual", "strange", "peculiar"],
        "\x96": ["frequent", "occasional", "unpredictable", "dreadful", "deadly"],
        "\x97": ["\x82 \x81 for \x8A", "\x82 \x81 for \x8A and \x8A", "\x88 by \x89",
                 "\x82 \x81 for \x8A but \x88 by \x89", "a\x90 \x91"],
        "\x98": ["\x9B", "mountain", "edible", "tree", "spotted"],
        "\x99": ["\x9F", "\xA0", "\x87oid", "\x93", "\x92"],
        "\x9A": ["ancient", "exceptional", "eccentric", "ingrained", "\x95"],
        "\x9B": ["killer", "deadly", "evil", "lethal", "vicious"],
        "\x9C": ["parking meters", "dust clouds", "ice bergs", "rock formations", "volcanoes"],
        "\x9D": ["plant", "tulip", "banana", "corn", "\xB2weed"],
        "\x9E": ["\xB2", "\xB1 \xB2", "\xB1 \x9B", "inhabitant", "\xB1 \xB2"],
        "\x9F": ["shrew", "beast", "bison", "snake", "wolf"],
        "\xA0": ["leopard", "cat", "monkey", "goat", "fish"],
        "\xA1": ["\x8C \x8B", "\xB1 \x9F \xA2", "its \x8D \xA0 \xA2", "\xA3 \xA4", "\x8C \x8B"],
        "\xA2": ["meat", "cutlet", "steak", "burgers", "soup"],
        "\xA3": ["ice", "mud", "Zero-G", "vacuum", "\xB1 ultra"],
        "\xA4": ["hockey", "cricket", "karate", "polo", "tennis"]
    }

    def __init__(self, num, x, y, name, economy, govtype,
                 techlev, population, productivity, radius, goatseed):
        self.num = num
        self.x = x
        self.y = y
        self.economy = economy
        self.govtype = govtype
        self.techlev = techlev
        self.population = population
        self.productivity = productivity
        self.radius = radius
        self.name = name
        self.goatsoupseed = goatseed
        self.gs = None
        self.fuelcost = 0.2

    def name_starts_with(self, name):
        return self.name.lower().startswith(name.strip().lower())

    @property
    def economy_description(self):
        return self.economy_types[self.economy]

    @property
    def government_description(self):
        return self.gov_types[self.govtype]

    def gen_rnd_number(self):
        """Generate a random number for goat-soup.
           Uses own algorithm so results are consistent and
           platform independant.
        """
        x = (self.gs[0] * 2) & 0xFF
        a = x + self.gs[2]
        if self.gs[0] > 127:
            a += 1
        self.gs[0] = a & 0xFF
        self.gs[2] = x
        a //= 256
        x = self.gs[1]
        a = (a + x + self.gs[3]) & 0xFF
        self.gs[1] = a
        self.gs[3] = x
        return a

    @property
    def goatsoup(self):
        """
        Planet description property.
        :return: str description
        """

        def _char_check(s):
            if s == '\xB0':
                return self.name.capitalize()
            elif s == '\xB1':
                if self.name[-1] in 'EUIOA':
                    ns = self.name[:-1]
                else:
                    ns = self.name
                return ns.capitalize() + 'ian'
            elif s == '\xB2':
                l = self.gen_rnd_number() & 3
                sample = (self.gen_rnd_number() for _ in range(l))
                return NameGenerator.get_name(sample, special_set=True).capitalize()
            elif s in self.desc_list:
                return self.desc_list[s][self.gen_rnd_number() % 5]
            else:
                return False

        def _str_check(s):
            new_s = ''
            for c in s:
                data = _char_check(c)
                if data:
                    data = _str_check(data)
                else:
                    data = c
                new_s += data
            return new_s

        self.gs = self.goatsoupseed[:]
        name = _str_check(self.goatsoup_template)
        return name[0].capitalize() + name[1:]

    def __str__(self):
        desc = '''
        System: {name}
        Position: {x}:{y}
        Economy: {eco_desc}
        Government: {gov_desc}
        Tech Level: {tech}
        Turnover: {prod} MCR
        Diameter: {r}km
        Population: {pop:.1f} Billion
        "{goat}" (c) The Hitchhiker's Guide
        '''.format(name=self.name, x=self.x, y=self.y, eco_desc=self.economy_description,
                   gov_desc=self.government_description, tech=self.techlev + 1, prod=self.productivity,
                   r=2 * round(self.radius, -2), pop=self.population / 10, goat=self.goatsoup)
        return desc

    def description(self, short=True):
        if not short:
            return self.__str__()
        return '{name} {tech} {eco_desc} {gov_desc}'.format(name=self.name, tech=self.techlev + 1,
                                                            eco_desc=self.economy_description,
                                                            gov_desc=self.government_description)


class Galaxy:
    class Seed:
        """A pseudo-random number holder based on 16 bit numbers."""

        @staticmethod
        def bit_mask(value):
            mask = (1 << 16) - 1
            return value & mask

        @staticmethod
        def twist(x):
            def rotate(v):
                temp = v & 128
                return (2 * (v & 127)) + (temp >> 7)

            return (256 * rotate(x >> 8)) + rotate(x & 255)

        def __init__(self, w0=0x5A4A, w1=0x0248, w2=0xB753):
            self.w0 = w0
            self.w1 = w1
            self.w2 = w2

        def __str__(self):
            return '{}/{}/{}'.format(self.w0, self.w1, self.w2)

        def twist_all(self):
            self.w0 = self.twist(self.w0)
            self.w1 = self.twist(self.w1)
            self.w2 = self.twist(self.w2)

        def shuffle(self):
            """Pseudo Randomize a seed"""
            temp = self.bit_mask(self.w0 + self.w1 + self.w2)
            self.w0 = self.w1
            self.w1 = self.w2
            self.w2 = temp

    def __init__(self):
        """A galaxy.

           In the original game all system data was generated from the initial
           seed value for galaxy one. If you want a later galaxy you have to
           advance through to get it.
        """
        self.galaxy_number = 1
        self.seed = None
        self.systems = None
        self.set_galaxy(1)

    def make_systems(self):
        self.systems = [self.make_system(i) for i in range(256)]

    def set_galaxy(self, num: int):
        """Set base seed for galaxy
        :param int num: galaxy number
        """
        self.seed = self.Seed()
        for __ in range(2, num + 1):
            self.seed.twist_all()
        self.galaxy_number = num % 8
        self.make_systems()

    def make_system(self, system_number):
        """
        Creates a system with a specific number.
        System data seems ok for a classic Elite, but doesn't match Elite+
        (for example: Orerve/Orrere, different tech levels, pop and productivity).
        I also tweaked a goatsoup string generation a bit, so planet descriptions
        probably won't match original ones (but the game don't use them anyway).
        :param int system_number:
        :return: PlanSys instance
        """
        s = self.seed
        x, y = s.w1 >> 8, s.w0 >> 8
        long_name_flag = bool(s.w0 & 64)
        govtype = ((s.w1 >> 3) & 7)  # bits 3,4 &5 of w1
        economy = ((s.w0 >> 8) & 7)  # bits 8,9 &A of w0
        if govtype <= 1:
            economy |= 2
        techlev = ((s.w1 >> 8) & 3) + (economy ^ 7) + (govtype >> 1)
        techlev += govtype & 1
        population = 4 * techlev + economy + govtype + 1
        productivity = (((economy & 7) + 3) * (govtype + 4)) * population * 8
        radius = 256 * (((s.w2 >> 8) & 15) + 11) + x
        goatseed = [s.w1 & 0xFF, s.w1 >> 8, s.w2 & 0xFF, s.w2 >> 8]
        sample = []
        for __ in range(4):
            sample.append(2 * ((s.w2 >> 8) & 31))
            s.shuffle()
        name = NameGenerator.get_name(sample[:3 + long_name_flag])
        return PlanSys(system_number, x, y, name, economy, govtype,
                       techlev, population, productivity, radius, goatseed)

    @staticmethod
    def distance(a, b):
        return int(4.0 * ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 / 4.0) ** 0.5)

    def closest_system_like(self, current_sys, name):
        if not name:
            return 0., current_sys
        d = 9999
        ret_system = None
        for planet_sys in self.systems:
            if planet_sys.name_starts_with(name):
                dist = self.distance(current_sys, planet_sys)
                if dist < d:
                    d = dist
                    ret_system = planet_sys
        return d, ret_system

    def systems_within(self, current, max_ly_distance):
        found = []
        for planet_sys in self.systems:
            dist = self.distance(current, planet_sys)
            if dist <= max_ly_distance:
                found.append((dist, planet_sys))
        return found


class Market:
    """Local market model"""

    class MarketGood:
        """A commodity for sale : price / quantity"""

        def __init__(self, commodity, price=0, q=0):
            self.commodity = commodity
            self.price = price
            self.quantity = q

    class Commodity:
        """Trade commodity"""
        Unit = namedtuple('Unit', ['name', 'mod'])
        t = Unit('t', 1.)
        kg = Unit('kg', 0.)
        g = Unit('g', 0.)

        def __init__(self, base_price, gradient, base_quantity, mask, unit, name):
            self.base_price = base_price
            self.gradient = gradient
            self.base_quantity = base_quantity
            self.mask = mask
            self.unit = unit
            self.name = name

    commodities = (
        Commodity(0x13, -0x02, 0x06, 0x01, Commodity.t, "Food"),
        Commodity(0x14, -0x01, 0x0A, 0x03, Commodity.t, "Textiles"),
        Commodity(0x41, -0x03, 0x02, 0x07, Commodity.t, "Radioactives"),
        Commodity(0x28, -0x05, 0xE2, 0x1F, Commodity.t, "Slaves"),
        Commodity(0x53, -0x05, 0xFB, 0x0F, Commodity.t, "Liquor/Wines"),
        Commodity(0xC4, +0x08, 0x36, 0x03, Commodity.t, "Luxuries"),
        Commodity(0xEB, +0x1D, 0x08, 0x78, Commodity.t, "Narcotics"),
        Commodity(0x9A, +0x0E, 0x38, 0x03, Commodity.t, "Computers"),
        Commodity(0x75, +0x06, 0x28, 0x07, Commodity.t, "Machinery"),
        Commodity(0x4E, +0x01, 0x11, 0x1F, Commodity.t, "Alloys"),
        Commodity(0x7C, +0x0d, 0x1D, 0x07, Commodity.t, "Firearms"),
        Commodity(0xB0, -0x09, 0xDC, 0x3F, Commodity.t, "Furs"),
        Commodity(0x20, -0x01, 0x35, 0x03, Commodity.t, "Minerals"),
        Commodity(0x61, -0x01, 0x42, 0x07, Commodity.kg, "Gold"),
        Commodity(0xAB, -0x02, 0x37, 0x1F, Commodity.kg, "Platinum"),
        Commodity(0x2D, -0x01, 0xFA, 0x0F, Commodity.g, "Gem-Stones"),
        Commodity(0x35, +0x0F, 0xC0, 0x07, Commodity.t, "Alien Items"),
    )

    @classmethod
    def find_by_name(cls, commod_name: str):
        for c in cls.commodities:
            if c.name.lower().startswith(commod_name.lower().strip()):
                return c
        else:
            return None

    def create_goods(self, system, fluct):
        for c in self.commodities:
            good = self.goods[c.name]
            product = system.economy * c.gradient
            changing = fluct & c.mask
            q = c.base_quantity + changing - product
            q &= 0xFF

            if q & 0x80:
                q = 0
            good.quantity = q & 0x3F

            q = c.base_price + changing + product
            q &= 0xFF
            good.price = (q * 4) / 10.0

        self.goods['Alien Items'].quantity = 0

    def __init__(self, system, fluct):
        self.goods = OrderedDict([(c.name, self.MarketGood(c)) for c in self.commodities])
        self.create_goods(system, fluct)
        self.selling_fee = 0.035


class Ship:
    """A ship (by default a Cobra MkIII)"""
    ship_descriptions = (
        '''
        This ship is most commonly used by traders, although a few have been captured
        by pirates,so a wise commander will be wary of even the quietest looking ships.
        The standard Cobra hull is equipped with four missile pods, separate front and
        rear shields, and provision for a cargo bay extension which increases the
        capacity of the hold.
        ''',
    )
    Ship = namedtuple('Ship', ['name', 'holdsize', 'maxfuel', 'velocity', 'maneur', 'crew', 'hull', 'desc'])
    ship_types = (
        Ship('Cobra MkIII', 20, 70, 0.3, 8, 1, 18, ship_descriptions[0]),
    )

    def __init__(self, ship_type='Cobra MkIII'):
        self.name = 'Jameson'
        self.ship = next((s for s in self.ship_types if s.name == ship_type), self.ship_types[0])
        self.holdsize = self.ship.holdsize
        self.maxfuel = self.ship.maxfuel
        self.fuel = self.maxfuel
        self.cargo = OrderedDict([(c.name, 0) for c in Market.commodities])
        self.cash = 100.0
        self.galaxynum = 1
        self.planetnum = 7  # Lave

    def __str__(self):
        return '''
        {name}
        Fuel : {fuel}/{maxfuel}
        Cash : {cash}
        Ship : {ship.name}
        Hull : T{ship.hull} | Maneurability : CF{ship.maneur} | Velocity : {ship.velocity} | Crew : {ship.crew}
        {ship.desc}
        '''.format(name=self.ship.name,
                   fuel=int(self.fuel), maxfuel=self.maxfuel,
                   cash=int(self.cash), ship=self.ship)

    @property
    def cargosize(self):
        """Return current size of cargo in tonnes"""
        return sum([self.cargo[c.name] * c.unit.mod for c in Market.commodities])

    @property
    def hold_remaining(self):
        """Return how much space remains in the hold"""
        return self.holdsize - self.cargosize


class TradingGame:
    """Encodes rules of the game"""

    def __init__(self):
        self.ship = Ship()
        self.galaxy = Galaxy()
        self.localmarket = None
        self.generate_market()  # Since we want seed=0 for Lave

    @property
    def current_system(self):
        """Get the players current system"""
        return self.galaxy.systems[self.ship.planetnum]

    def generate_market(self, fluct=0):
        self.localmarket = Market(self.current_system, fluct)

    def next_galaxy(self):
        """Galactic hyperspace to next galaxy"""
        self.galaxy.set_galaxy(self.galaxy.galaxy_number + 1)
        self.generate_market()

    def move_to(self, planet_sys):
        self.ship.planetnum = planet_sys.num

    def jump(self, planetname):

        def _char(value):
            value &= 255
            if value > 127:
                return value - 256
            return value

        distance, dest = self.galaxy.closest_system_like(self.current_system, planetname)
        if dest is None:
            return False, "NAV ERROR: Planet not found!"
        if dest.name == self.current_system.name:
            return False, "NAV ERROR: Jump not possible!"
        if distance > self.ship.fuel:
            return False, "NAV ERROR: Not enough fuel for the jump!"
        self.ship.fuel -= distance
        self.move_to(dest)
        r = Randomizer.get_value()
        self.generate_market(_char(r & 0xFF))
        return True, "REPORT: Welcome to %s" % dest.name

    def dump(self, commod, amt):
        commod = self.localmarket.find_by_name(commod)
        cargo = self.ship.cargo.get(commod.name)
        if not cargo:
            msg = "ENG ERROR: No %s available to dump into space" % commod.name
            return False, msg
        if amt > cargo:
            amt = cargo
        self.ship.cargo[commod.name] -= amt
        msg = "REPORT: %.0f %s of %s successfully removed from the ship" % (
            amt, commod.unit.name, commod.name)
        return True, msg

    def sell(self, commod, amt):
        commod = self.localmarket.find_by_name(commod)
        cargo = self.ship.cargo[commod.name]
        if cargo <= 0:
            msg = "FIN ERROR: No %s to sell." % commod.name
            return False, msg
        if amt > cargo:
            # msg = "Only have {q}{u} to sell. Selling {q}{u}".format(q=cargo, u=commod.unit.name)
            amt = cargo
        local_market = self.localmarket.goods[commod.name]
        price = amt * local_market.price * (1. - self.localmarket.selling_fee)
        msg = "REPORT: Selling {q}{u} of {name} for {p:.1f}".format(
            q=amt, u=commod.unit.name, name=commod.name, p=price)
        self.ship.cash += price
        self.ship.cargo[commod.name] -= int(amt)
        local_market.quantity += int(amt)
        return True, msg

    def buy(self, commod, amt):
        commod = self.localmarket.find_by_name(commod)
        local_market = self.localmarket.goods[commod.name]
        lcl_amount = local_market.quantity
        if lcl_amount == 0:
            msg = "FIN ERROR: no %s on the market" % commod.name
            return False, msg
        if amt > lcl_amount:
            # msg = "FIN ERROR: Could not buy {q}{u} attempting to buy maximum {q2}{u} instead.".format(
            # q=amt, u=commod.unit.name, q2=lcl_amount)
            amt = lcl_amount
        if local_market.price <= 0:
            can_have = amt
        else:
            can_have = int(self.ship.cash / local_market.price)
        if can_have <= 0:
            msg = "FIN ERROR: Cannot afford any %s" % commod.name
            return False, msg
        if amt > can_have:
            amt = can_have
        if self.ship.hold_remaining < amt * commod.unit.mod:
            can_have = self.ship.hold_remaining
            if can_have <= 0:
                msg = "ENG ERROR: No room in hold for any %s" % commod.name
                return False, msg
            else:
                # msg = "ENG ERROR: Could not fit {q}{u} into the hold. Reducing to {available}{u}".format(
                # q=amt, u=commod.unit.name, available=can_have)
                amt = can_have
        price = amt * local_market.price
        msg = "REPORT: Buying {q}{u} of {name} for {p:.1f}".format(
            q=amt, u=commod.unit.name, name=commod.name, p=price)
        self.ship.cash -= price
        self.ship.cargo[commod.name] += int(amt)
        local_market.quantity -= int(amt)
        return True, msg

    def buy_fuel(self):
        fuel_to_buy = self.ship.maxfuel - self.ship.fuel
        if fuel_to_buy <= 0:
            msg = "ENG ERROR: Fuel tank is full ( %.0f tonnes / %.1f LY Range)" % (self.ship.fuel, self.ship.fuel * 0.1)
            return False, msg
        cost = self.current_system.fuelcost * fuel_to_buy
        if self.ship.cash <= 0:
            self.ship.cash = 0.
            return False, "FIN ERROR: You can't afford any fuel"
        if cost > self.ship.cash:
            fuel_to_buy = self.ship.cash / self.current_system.fuelcost
            cost = self.current_system.fuelcost * fuel_to_buy
        self.ship.fuel += fuel_to_buy
        self.ship.cash -= cost
        msg = "REPORT: Refuelling %.1f LY (%.0f tonnes) cost %.1f credits" % (
            fuel_to_buy * 0.1, fuel_to_buy, cost)
        return True, msg

    def info_local_systems(self):
        head = 'short range chart'
        system_list = self.galaxy.systems_within(self.current_system, self.ship.maxfuel)
        choices = []
        for d, s in system_list:
            if d <= self.ship.fuel:
                i = " * "
            else:
                i = "-"
            desc = (s.name, '{i:2}{d:<8.1f} {desc}'.format(i=i, d=d / 10., desc=s.description(short=True)))
            choices.append((True, desc))
        return True, (head, choices)

    def info_commander(self):
        head = 'Commander %s' % self.ship.name
        desc = ('System:       %s' % self.current_system.name,
                'Fuel:         %.1f Light Years' % (self.ship.fuel * 0.1),
                'Cash:         %.1f Credits' % self.ship.cash,
                'Legal Status: Clean',
                'Rating:       Harmless',
                'Ship:         %s' % self.ship.ship.name,
                'EQUIPMENT:',)
        return True, (head, desc)

    def info_equip(self):
        head = 'Equip ship %.1f Credits' % self.ship.cash
        desc = [
            (False, self.ship.ship.desc),
            (False, 'EQUIPMENT            BUY / SELL')
        ]
        data = ('Fuel', 'Fuel (/Light Year) %s' % (self.ship.fuel * 0.1))
        desc.append((True, data))
        return True, (head, desc)

    def info_selected_system(self, name=None):
        d, system = self.galaxy.closest_system_like(self.current_system, name)
        if not system:
            return False, 'NAV ERROR', ('System not found!!!',)
        head = 'Data on %s' % system.name
        desc = ('Distance:      %.1f Light Years' % (d * 0.1),
                'Economy:       %s' % system.economy_description,
                'Government:    %s' % system.government_description,
                'Tech. Level:   %d' % system.techlev,
                'Population:    %.1f Billion' % (system.population * 0.1),
                'Productivity:  %d M CR' % system.productivity,
                'Radius (Av):   %d km' % system.radius,
                '%s' % system.goatsoup,)
        return True, (head, desc)

    def info_galaxy(self):
        head = 'galactic chart %d' % self.galaxy.galaxy_number
        galaxy = [[' '] * 137 for _ in range(32)]
        player_pos, star, reachable = '>', '.', '*'
        list_of_nearest = [s for d, s in self.galaxy.systems_within(self.current_system, self.ship.maxfuel)]
        for s in self.galaxy.systems:
            if s in list_of_nearest:
                x0, y0 = s.x // 2, s.y // 8
                dx = len(s.name)
                galaxy[y0][x0 + 1:x0 + dx] = list(s.name)
                galaxy[y0][x0] = reachable
            else:
                galaxy[s.y // 8][s.x // 2] = star
        x0, y0 = self.current_system.x // 2, self.current_system.y // 8
        galaxy[y0][x0] = player_pos
        galaxy = [''.join(row) for row in galaxy]
        return True, (head, galaxy)

    def info_cargo(self):
        head = 'items %d / %d tonnes' % (self.ship.holdsize - self.ship.hold_remaining, self.ship.holdsize)
        choices = [
            (False, 'Fuel: %.1f Light Years' % (self.ship.fuel * 0.1)),
            (False, 'Cash: %.1f Credits' % self.ship.cash),
        ]
        if self.ship.hold_remaining < self.ship.holdsize:
            choices.append((False, 'CARGO      DUMP'))
        for c, am in self.ship.cargo.items():
            if am:
                choices.append(
                    (True, (c, "%s %d" % (c, am)))
                )
        return True, (head, choices)

    def info_buy(self):
        head = 'buy cargo%5.1f Credits' % self.ship.cash
        data = [(False, 'PRODUCT         UNIT  PRICE / QTY')]
        for name, g in self.localmarket.goods.items():
            item = (name, '{n:16s} {u:3s} {b:5.1f} {q:5d}'.format(
                n=name, u=g.commodity.unit.name, b=g.price, q=g.quantity))
            data.append((True, item))
        return True, (head, data)

    def info_sell(self):
        head = 'sell cargo%5.1f Credits' % self.ship.cash
        data = [(False, 'PRODUCT         UNIT  PRICE / QTY')]
        for name, g in self.localmarket.goods.items():
            item = (name, '{n:16s} {u:3s} {b:5.1f} {q:5d}'.format(
                n=name, u=g.commodity.unit.name, b=g.price * (1 - self.localmarket.selling_fee),
                q=self.ship.cargo[name]))
            data.append((True, item))
        return True, (head, data)

    def info_trade(self):
        head = '%s market prices' % self.current_system.name
        data = ['PRODUCT         UNIT  BUY / SELL']
        for name, g in self.localmarket.goods.items():
            data.append(
                '{n:16s} {u:3s} {b:5.1f} {s:5.1f}'.format(
                    n=name, u=g.commodity.unit.name, b=g.price, s=g.price * (1 - self.localmarket.selling_fee))
            )
        return True, (head, data)
