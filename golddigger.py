import math

import JSON


class GoldDigger:
    TOTAL_COINS = "Total coins"
    TOTAL_VALUE = "Total value"
    PARTY_MEMBER_SHARE = "Party member share"
    LEFT_OVER_COIN = "Left over coin"
    LEFT_OVER_MEMBER_SHARE = "Left over member share"
    LEFT_OVER_REMAINDER = "Left over remainder"
    CONVERSION_FEE = "Conversion Fee"
    SECURITY_FEE = "Security Fee"
    TITHE_LABEL = "Tithe"

    COIN_BAGS = "Coin Bags"
    PARTY_SIZE = "Party Size"
    FEE_PERCENT_LABEL = "Conversion Rate"
    TAX_PERCENT_LABEL = "Tax Rate"
    TITHE_PERCENT_LABEL = "Tithe Percent"

    PP = 'pp'
    GP = 'gp'
    SP = 'sp'
    CP = 'cp'
    FEE = 0.01
    TAX = 0.01
    TITHE = 0.1
    PARTY = 1

    json_parser = JSON.JSON()
    json = ""

    total_data = dict()
    total_coins = dict()
    total_value = dict()
    member_share = dict()
    remainder = dict()
    remainder_share = dict()
    remainder_share_remainder = dict()
    conversion_fee = dict()
    tax_man = dict()
    tithe = dict()

    coin_bags = []
    party_size = 1
    conversion_percent = FEE
    tax_percent = TAX
    tithe_percent = TITHE

    debug = False
    debug_bags = ['2gp 6sp', '12sp', '2gp 8sp 10cp', '2gp 42sp 39cp']

# -------------------------------------------------------------
# --- INITIALIZATION
# -------------------------------------------------------------
    @classmethod
    def init(cls):
        cls.init_bags()
        cls.init_total_data()
        cls.init_properties()
        return cls

    @classmethod
    def init_bags(cls):
        cls.init_bag(cls.total_coins)
        cls.init_bag(cls.total_value)
        cls.init_bag(cls.member_share)
        cls.init_bag(cls.remainder)
        cls.init_bag(cls.remainder_share)
        cls.init_bag(cls.remainder_share_remainder)

        cls.init_bag(cls.conversion_fee)
        cls.init_bag(cls.tax_man)
        cls.init_bag(cls.tithe)

        cls.set_coin_bags([])

    @classmethod
    def init_total_data(cls):
        cls.total_data[cls.TOTAL_COINS] = cls.total_coins
        cls.total_data[cls.TOTAL_VALUE] = cls.total_value
        cls.total_data[cls.PARTY_MEMBER_SHARE] = cls.member_share
        cls.total_data[cls.LEFT_OVER_COIN] = cls.remainder
        cls.total_data[cls.LEFT_OVER_MEMBER_SHARE] = cls.remainder_share
        cls.total_data[cls.LEFT_OVER_REMAINDER] = cls.remainder_share_remainder
        cls.total_data[cls.CONVERSION_FEE] = cls.conversion_fee
        cls.total_data[cls.SECURITY_FEE] = cls.tax_man
        cls.total_data[cls.TITHE_LABEL] = cls.tithe

    @classmethod
    def init_properties(cls):
        cls.set_party_size(cls.PARTY)
        cls.set_conversion_fee(cls.FEE)
        cls.set_tax(cls.TAX)
        cls.set_tithe(cls.TITHE)

    @classmethod
    def init_bag(cls, bag):
        bag[cls.PP] = 0
        bag[cls.GP] = 0
        bag[cls.SP] = 0
        bag[cls.CP] = 0

    @classmethod
    def init_json(cls):
        if cls.FEE_PERCENT_LABEL in cls.total_data:
            cls.set_conversion_fee(cls.total_data[cls.FEE_PERCENT_LABEL])
        if cls.TAX_PERCENT_LABEL in cls.total_data:
            cls.set_tax(cls.total_data[cls.TAX_PERCENT_LABEL])
        if cls.TITHE_PERCENT_LABEL in cls.total_data:
            cls.set_tithe(cls.total_data[cls.TITHE_PERCENT_LABEL])
        if cls.PARTY_SIZE in cls.total_data:
            cls.set_party_size(cls.total_data[cls.PARTY_SIZE])

    @classmethod
    def set_coin_bags(cls, coins):
        cls.coin_bags = coins[:]
        cls.total_data[cls.COIN_BAGS] = cls.coin_bags

    @classmethod
    def set_party_size(cls, size):
        cls.party_size = int(size)
        cls.total_data[cls.PARTY_SIZE] = cls.party_size

    @classmethod
    def set_conversion_fee(cls, fee):
        cls.conversion_percent = float(fee)
        cls.total_data[cls.FEE_PERCENT_LABEL] = cls.conversion_percent

    @classmethod
    def set_tax(cls, tax):
        cls.tax_percent = float(tax)
        cls.total_data[cls.TAX_PERCENT_LABEL] = cls.tax_percent

    @classmethod
    def set_tithe(cls, tithe):
        cls.tithe_percent = float(tithe)
        cls.total_data[cls.TITHE_PERCENT_LABEL] = cls.tithe_percent

    @classmethod
    def set_json(cls, json):
        cls.total_data = cls.json_parser.loads(json)

    @classmethod
    def set_json_web(cls, json):
        cls.init_bags()
        cls.set_json(json)
        cls.init_total_data()
        cls.init_json()
        # cls.init_total_data()
        cls.process_coin_bags_web(cls.total_data)
        cls.process()

    @classmethod
    def get_json(cls):
        return cls.json

    @classmethod
    def gold_dig(cls):
        cls.get_input()
        cls.process()
        cls.get_json()
        cls.output()

# -------------------------------------------------------------
# --- UTILITY
# -------------------------------------------------------------

    @classmethod  # process indexed bags from web {"1" : {"pp": 1 "gp": 2}} : directly add to total_value
    def process_coin_bags_web(cls, data):
        i = 1
        ii = str(i)
        while ii in data:
            mapp = data[ii]
            for key, value in mapp.items():
                cls.add_coin(cls.total_coins, key, value)
            i += 1
            ii = str(i)
        for x in range(1, i, 1):
            data.pop(str(x))

    @classmethod
    def add_coin(cls, bag, key, value):
        bag[key] += value

# -------------------------------------------------------------
# --- INPUT
# -------------------------------------------------------------

    @classmethod
    def get_input(cls):
        if cls.debug:
            cls.set_coin_bags(cls.debug_bags)
            cls.set_party_size(5)
        else:
            cls.input_gold_bags()
            cls.set_party_size(cls.input_party_size())
            cls.set_conversion_fee(cls.input_conversion_fee())

    @classmethod
    def input_gold_bags(cls):
        prompt = f"Input format : 1pp 2gp 3sp 4cp : empty when finished. "
        coin_bag = input(prompt)
        while coin_bag:
            if cls.validate_input(coin_bag):
                cls.coin_bags.append(coin_bag)
            else:
                print(f"Invalid input[{coin_bag}].  Skipping.")
            coin_bag = input(prompt)

    @classmethod
    def input_party_size(cls):
        size = 0
        while size == 0:
            user_input = input("Enter party size: ")

            # Attempt to convert the input to an integer
            try:
                size = int(user_input)
            except ValueError:
                print("Invalid input.")
        return size

    @classmethod
    def input_conversion_fee(cls):
        fee = 0.00
        valid = False
        while not valid:
            valid = True
            user_input = input("What is the conversion fee?  Enter for default (0.01)")

            # Attempt to convert the input to an integer
            if user_input:
                try:
                    fee = float(user_input)
                except ValueError:
                    print(f"{user_input} is invalid.")
                    valid = False
            else:
                fee = cls.FEE
        return fee

    @classmethod
    def validate_input(cls, coin_bag):
        good_bag = True
        for coin_type in coin_bag.lower().split():
            coins = "no_coin"
            if len(coin_type) > 2:
                if coin_type.endswith(cls.PP):
                    coins = coin_type.split(cls.PP)[0]
                if coin_type.endswith(cls.GP):
                    coins = coin_type.split(cls.GP)[0]
                if coin_type.endswith(cls.SP):
                    coins = coin_type.split(cls.SP)[0]
                if coin_type.endswith(cls.CP):
                    coins = coin_type.split(cls.CP)[0]
            try:
                int(coins)
            except ValueError:
                good_bag = False
                print(f"Bad input value: {coin_type}")
        return good_bag

# -------------------------------------------------------------
# --- PROCESS
# -------------------------------------------------------------

    @classmethod
    def process(cls):
        cls.parse()
        cls.allocate(cls.total_coins, cls.member_share, cls.remainder)
        cls.allocate_remainder(cls.remainder, cls.remainder_share, cls.remainder_share_remainder)
        cls.consolidate(cls.total_coins, cls.total_value)

        cls.process_deductions()
        cls.json = cls.json_parser.dumps(cls.total_data)

    @classmethod  # combines multiple coin bags from the command line into one bag cls.coins_total
    def parse(cls):
        for bag in cls.coin_bags:
            for coin in bag.split():
                if coin.endswith(cls.PP):
                    cls.total_coins[cls.PP] += int(coin.split(cls.PP)[0])
                if coin.endswith(cls.GP):
                    cls.total_coins[cls.GP] += int(coin.split(cls.GP)[0])
                if coin.endswith(cls.SP):
                    cls.total_coins[cls.SP] += int(coin.split(cls.SP)[0])
                if coin.endswith(cls.CP):
                    cls.total_coins[cls.CP] += int(coin.split(cls.CP)[0])

    @classmethod  # split for each party member and save remainder
    def allocate(cls, source, member, remainder):
        
        for key, value in source.items():
            member[key] = value // cls.party_size
            remainder[key] = value % cls.party_size

    @classmethod  # converts to copper, applying conversion fee, and divides by party size
    def allocate_remainder(cls, remainder, remainder_share, remainder_share_remainder):
        temp_remainder = dict()
        cls.init_bag(temp_remainder)

        copper_bag = cls.convert_to_copper(remainder)
        cls.allocate(copper_bag, temp_remainder, remainder_share_remainder)
        cls.consolidate(temp_remainder, remainder_share)

    @classmethod
    def process_deductions(cls):
        copper_bag = cls.convert_to_copper(cls.total_coins)
        cls.process_fee(copper_bag, cls.conversion_fee, cls.conversion_percent)
        cls.process_fee(copper_bag, cls.tax_man, cls.tax_percent)
        cls.process_fee(copper_bag, cls.tithe, cls.tithe_percent)

    @classmethod
    def process_fee(cls, copper_bag, target_bag, fee_percent):
        fee_bag = dict()
        cls.init_bag(fee_bag)

        cls.add_coin(fee_bag, cls.CP, math.ceil(copper_bag[cls.CP] * fee_percent))
        cls.consolidate(fee_bag, target_bag)

    @classmethod  # converts to total cp and optionally subtract fee
    def convert_to_copper(cls, source_bag):
        copper_bag = dict()
        cls.init_bag(copper_bag)

        gp = source_bag[cls.PP] * 10
        sp = (source_bag[cls.GP] + gp) * 10
        cp = (source_bag[cls.SP] + sp) * 10 + source_bag[cls.CP]
        copper_bag[cls.CP] = cp

        return copper_bag

    @classmethod
    def populate_fee_bag(cls, target_bag, fee):
        source_bag = dict()
        cls.init_bag(source_bag)
        source_bag[cls.CP] = fee
        cls.consolidate(source_bag, target_bag)

    # converts the coins in the bag to the largest denomination
    @classmethod
    def consolidate(cls, source_bag, target_bag):
        pp = source_bag[cls.PP]
        gp = source_bag[cls.GP]
        sp = source_bag[cls.SP]
        cp = source_bag[cls.CP]

        target_bag[cls.CP] = cp % 10
        sp += cp // 10
        target_bag[cls.SP] = sp % 10
        gp += sp // 10
        target_bag[cls.GP] = gp % 10
        target_bag[cls.PP] = pp + gp // 10

    @classmethod
    def gp(cls, bag):
        temp = dict()
        cls.init_bag(temp)
        cls.consolidate(bag, temp)
        gp = f'{temp[cls.PP] * 10 + temp[cls.GP]}.{temp[cls.SP]}{temp[cls.CP]}'
        return gp

    @classmethod
    def pretty_output(cls, dictionary):
        string = ''
        for key, value in dictionary.items():
            string += f'{key.upper()}:{value} ' if value > 0 else ''
        return string.rstrip()

# -------------------------------------------------------------
# --- OUTPUT
# -------------------------------------------------------------
    @classmethod
    def output(cls):
        if cls.debug:
            print(f'--- JSON ---\n{cls.json}')
        print("--- TOTAL ---")
        print(f'{cls.TOTAL_COINS}: {cls.pretty_output(cls.total_coins)}')
        print(f'{cls.TOTAL_VALUE}: ({cls.gp(cls.total_value)}gp) {cls.pretty_output(cls.total_value)}')
        print(f'{cls.PARTY_MEMBER_SHARE}: ({cls.gp(cls.member_share)}gp) {cls.pretty_output(cls.member_share)}')

        print("--- REMAINDER ---")
        print(f'{cls.LEFT_OVER_COIN}: ({cls.gp(cls.remainder)}gp) {cls.pretty_output(cls.remainder)}')
        print(f'{cls.LEFT_OVER_MEMBER_SHARE}: ({cls.gp(cls.remainder_share)}gp) '
              f'{cls.pretty_output(cls.remainder_share)}')
        print(f'{cls.LEFT_OVER_REMAINDER}: ({cls.gp(cls.remainder_share_remainder)}gp) '
              f'{cls.pretty_output(cls.remainder_share_remainder)}')

        print("--- MISCELLANEOUS ---")
        print(f"{cls.PARTY_SIZE}: {cls.party_size}")
        print(f"{cls.CONVERSION_FEE}: ({cls.conversion_percent}): {cls.pretty_output(cls.conversion_fee)}")
        print(f"{cls.SECURITY_FEE}: ({cls.TAX}): {cls.pretty_output(cls.tax_man)}")
        print(f"{cls.TITHE_LABEL}: {cls.TITHE_PERCENT_LABEL} ({cls.TITHE}): {cls.pretty_output(cls.tithe)}")

    # -------------------------------------------------------------
    # --- RUN
    # -------------------------------------------------------------
    @classmethod
    def run(cls):
        cls.init().gold_dig()


if __name__ == "__main__":
    GoldDigger().run()
