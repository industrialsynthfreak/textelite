from collections import namedtuple


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
            name += pairs[i:i+2]
        return name.replace('.', '')


class PlanSys:
    """A planetary system"""
    economy_types = ("Rich Ind", "Average Ind", "Poor Ind", "Mainly Ind",
                     "Mainly Agri", "Rich Agri", "Average Agri", "Poor Agri")
    gov_types = ("Anarchy", "Feudal", "Multi-gov", "Dictatorship", "Communist",
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

        name = _str_check(self.goatsoup_template)
        return name[0].capitalize() + name[1:]

    def __str__(self):
        self.gs = self.goatsoupseed[:]
        desc = '''
        System: {name}
        Position: {x}:{y}
        Economy: {eco_desc}
        Government: {gov_desc}
        Tech Level: {tech}
        Turnover: {prod} MCR
        Radius: {r} KM
        Population: {pop:.1f} BIL
        "{goat}" (c) The Hitchhiker's Guide
        '''.format(name=self.name, x=self.x, y=self.y, eco_desc=self.economy_description,
                   gov_desc=self.government_description, tech=self.techlev + 1, prod=self.productivity,
                   r=self.radius, pop=self.population / 10, goat=self.goatsoup)
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
        self.galaxy_number = None
        self.seed = None
        self.systems = None
        self.set_galaxy(1)

    def make_systems(self):
        self.systems = [self.make_system(i) for i in range(256)]
        print(self.galaxy_number)
        print(sorted([s.name for s in self.systems]))

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
        name = NameGenerator.get_name(sample[:3+long_name_flag])
        return PlanSys(system_number, x, y, name, economy, govtype,
                       techlev, population, productivity, radius, goatseed)

    @staticmethod
    def distance(a, b):
        return int(4.0 * ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 / 4.0) ** 0.5)

    def closest_system_like(self, current_sys, name):
        d = 9999
        ret_system = None
        for planet_sys in self.systems:
            if planet_sys.name_starts_with(name):
                dist = self.distance(current_sys, planet_sys)
                if dist < d:
                    d = dist
                    ret_system = planet_sys
        return ret_system

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

        def __init__(self, price=0, q=0):
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

    commodities = [
        Commodity(0x13, -0x02, 0x06, 0x01, Commodity.t, "Food        "),
        Commodity(0x14, -0x01, 0x0A, 0x03, Commodity.t, "Textiles    "),
        Commodity(0x41, -0x03, 0x02, 0x07, Commodity.t, "Radioactives"),
        Commodity(0x28, -0x05, 0xE2, 0x1F, Commodity.t, "Slaves      "),
        Commodity(0x53, -0x05, 0xFB, 0x0F, Commodity.t, "Liquor/Wines"),
        Commodity(0xC4, +0x08, 0x36, 0x03, Commodity.t, "Luxuries    "),
        Commodity(0xEB, +0x1D, 0x08, 0x78, Commodity.t, "Narcotics   "),
        Commodity(0x9A, +0x0E, 0x38, 0x03, Commodity.t, "Computers   "),
        Commodity(0x75, +0x06, 0x28, 0x07, Commodity.t, "Machinery   "),
        Commodity(0x4E, +0x01, 0x11, 0x1F, Commodity.t, "Alloys      "),
        Commodity(0x7C, +0x0d, 0x1D, 0x07, Commodity.t, "Firearms    "),
        Commodity(0xB0, -0x09, 0xDC, 0x3F, Commodity.t, "Furs        "),
        Commodity(0x20, -0x01, 0x35, 0x03, Commodity.t, "Minerals    "),
        Commodity(0x61, -0x01, 0x42, 0x07, Commodity.kg, "Gold        "),
        Commodity(0xAB, -0x02, 0x37, 0x1F, Commodity.kg, "Platinum    "),
        Commodity(0x2D, -0x01, 0xFA, 0x0F, Commodity.g, "Gem-Stones  "),
        Commodity(0x35, +0x0F, 0xC0, 0x07, Commodity.t, "Alien Items "),
    ]

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

        self.goods['Alien Items '].quantity = 0

    def __init__(self, system, fluct):
        self.goods = {c.name: self.MarketGood() for c in self.commodities}
        self.create_goods(system, fluct)


class Ship:
    """A ship (by default a Cobra MkIII)"""

    def __init__(self):
        self.holdsize = 20
        self.cargo = {c.name: 0 for c in Market.commodities}
        self.cash = 100.0
        self.maxfuel = 70
        self.fuel = self.maxfuel
        self.galaxynum = 1
        self.planetnum = 7  # Lave

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
        self.generate_market()      # Since we want seed=0 for Lave

    def generate_market(self, fluct=0):
        self.localmarket = Market(self.current_system, fluct)

    @staticmethod
    def char(value):
        value &= 255
        if value > 127:
            return value - 256
        return value

    @property
    def current_system(self):
        """Get the players current system"""
        return self.galaxy.systems[self.ship.planetnum]

    def move_to(self, planet_sys):
        self.ship.planetnum = planet_sys.num

    def jump(self, planetname):
        dest = self.galaxy.closest_system_like(self.current_system, planetname)

        if dest is None:
            print("Planet not found")
            return

        if dest.name == self.current_system.name:
            print("Bad jump!")
            return

        distance = self.galaxy.distance(self.current_system, dest)
        if distance > self.ship.fuel:
            print("Jump too far")
            return

        self.ship.fuel -= distance
        self.move_to(dest)

        r = Randomizer.get_value()
        fluct = self.char(r & 0xFF)
        self.generate_market(fluct)

    def sneak(self, planetname):
        fuelsafe = self.ship.fuel
        self.ship.fuel = 666
        self.jump(planetname)
        self.ship.fuel = fuelsafe

    def set_hold(self, newsize):
        sm = self.ship.cargosize()
        if sm > newsize:
            print("Hold too full to shrink!")
            return
        self.ship.holdsize = newsize

    def next_galaxy(self):
        """Galactic hyperspace to next galaxy"""
        self.galaxy.set_galaxy(self.galaxy.galaxy_number + 1)
        self.generate_market()

    def display_market(self):
        """Print out commodities, prices and quantities here"""
        for c in Market.commodities:
            lcl = self.localmarket.goods[c.name]
            current = self.ship.cargo[c.name]
            print('{name:15} {price:5.1f} {q:3d}{unit:<3} Hold: {current}'.format(name=c.name, price=lcl.price,
                                                                               q=lcl.quantity,unit=c.unit.name,
                                                                               current=current))

    def sell(self, commod, amt):
        #Do we have any to sell?
        cargo = self.ship.cargo[commod.name]
        if cargo <= 0:
            print("No {name} to sell.".format(commod.name))
            return

        if amt > cargo:
            print("Only have {q}{u} to sell. Selling {q}{u}".format(q=cargo, u=commod.unit.name))
            amt = cargo

        local_market = self.localmarket.goods[commod.name]
        price = amt * local_market.price
        print("Selling {q}{u} of {name} for {p}".format(q=amt, u=commod.unit.name, name=commod.name, p=price))
        self.ship.cash = self.ship.cash + price
        self.ship.cargo[commod.name] -= amt
        local_market.quantity += amt

    def buy(self, commod, amt):
        local_market = self.localmarket.goods[commod.name]
        lcl_amount = local_market.quantity
        if lcl_amount == 0:
            print("Could not buy any {name}".format(name=commod.name))
            return

        if amt > lcl_amount:
            print("Could not buy {q}{u} attempting to buy maximum {q2}{u} instead.".format(
                q=amt, u=commod.unit.name, q2=lcl_amount))
            amt = lcl_amount

        #How many can I afford?
        if local_market.price <= 0:
            can_have = amt
        else:
            can_have = int(self.ship.cash / local_market.price)
        if can_have <= 0:
            print("Cannot afford any {name}".format(name=commod.name))
            return

        if amt > can_have:
            amt = can_have

        #How much will fit in the hold?
        if self.ship.hold_remaining < amt * commod.unit.mod:
            can_have = self.ship.hold_remaining
            if can_have <= 0:
                print("No room in hold for any {name}".format(name=commod.name))
                return
            else:
                print("Could not fit {q}{u} into the hold. Reducing to {available}{u}".format(
                    q=amt, u=commod.unit.name, available=can_have))
                amt = can_have

        price = amt * local_market.price
        print("Buying {q}{u} of {name} for {p}".format(q=amt, u=commod.unit.name, name=commod.name, p=price))
        self.ship.cash -= price
        self.ship.cargo[commod.name] += amt
        local_market.quantity -= amt

    def buy_fuel(self, f):
        if f + self.ship.fuel > self.ship.maxfuel:
            f = self.ship.maxfuel - self.ship.fuel

        if f <= 0:
            print("Your fuel tank is full ({f} tonnes / {r} LY Range)".format(f=self.ship.fuel, r=self.ship.fuel / 10.0))
            return 0, 0

        # Find out what system we're at because fuelcost is there.
        this_sys = self.current_system

        cost = this_sys.fuelcost * f

        if self.ship.cash > 0:
            if cost > self.ship.cash:
                f = self.ship.cash / this_sys.fuelcost
                cost = this_sys.fuelcost * f
        else:
            print("You can't afford any fuel")
            return 0, 0

        self.ship.fuel += f
        self.ship.cash -= cost
        return f, cost
