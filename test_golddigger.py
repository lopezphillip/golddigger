import unittest

from golddigger import GoldDigger


# ---
# python -m unittest


# noinspection PyPep8Naming
def setUpModule():
    print("setUpModule (must be camel case)")


class TestGoldDigger(unittest.TestCase):
    gold_digger = None

    source_bag = None
    target_bag = None
    check_bag = None

    bags = ['2gp 6sp', '12sp', '2gp 8sp 10cp', '2gp 42sp 39cp']

    json = '{"Coin Bags": ["2gp 6sp", "12sp", "2gp 8sp 10cp", "2gp 42sp 39cp"], ' \
           '"Total coins": {"pp": 0, "gp": 6, "sp": 68, "cp": 49}, ' \
           '"Total value": {"pp": 1, "gp": 3, "sp": 2, "cp": 9}, ' \
           '"Party member share": {"pp": 0, "gp": 1, "sp": 13, "cp": 9}, ' \
           '"Left over coin": {"pp": 0, "gp": 1, "sp": 3, "cp": 4}, ' \
           '"Left over member share": {"pp": 0, "gp": 0, "sp": 2, "cp": 6}, ' \
           '"Left over remainder": {"pp": 0, "gp": 0, "sp": 0, "cp": 4}, ' \
           '"Conversion Fee": {"pp": 0, "gp": 0, "sp": 1, "cp": 4}, ' \
           '"Security Fee": {"pp": 0, "gp": 0, "sp": 1, "cp": 4}, ' \
           '"Tithe": {"pp": 0, "gp": 1, "sp": 3, "cp": 3}, ' \
           '"Party Size": 5, "Conversion Rate": 0.01, "Tax Rate": 0.01, "Tithe Percent": 0.1}'

    json_web = '{"1": {"pp": 0, "gp": 2, "sp": 6, "cp": 0}, ' \
               '"2": {"pp": 0, "gp": 0, "sp": 12, "cp": 0}, ' \
               '"3": {"pp": 0, "gp": 2, "sp": 8, "cp": 10}, ' \
               '"4": {"pp": 0, "gp": 2, "sp": 42, "cp": 39}, ' \
               '"Party Size": 5, "Conversion Rate": 0.01, "Tax Rate": 0.01, "Tithe Percent": 0.1}'

    json_web2 = '{"1": {"pp": 0, "gp": 2, "sp": 6, "cp": 0}, ' \
                '"2": {"pp": 0, "gp": 0, "sp": 12, "cp": 0}, ' \
                '"3": {"pp": 0, "gp": 2, "sp": 8, "cp": 10}, ' \
                '"4": {"pp": 0, "gp": 2, "sp": 42, "cp": 39}, ' \
                '"Party Size": 1, "Conversion Rate": 0, "Tax Rate": 0, "Tithe Percent": 0}'

    json_web3 = '{"1": {"pp": 1, "gp": 0, "sp": 0, "cp": 0}, ' \
                '"Party Size": 5, "Conversion Rate": 0, "Tax Rate": 0, "Tithe Percent": 0}'

    json_web3_results = '{"Party Size": 5, "Conversion Rate": 0.0, "Tax Rate": 0.0, "Tithe Percent": 0.0, ' \
                        '"Total coins": {"pp": 1, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Total value": {"pp": 1, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Party member share": {"pp": 0, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Left over coin": {"pp": 1, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Left over member share": {"pp": 0, "gp": 2, "sp": 0, "cp": 0}, ' \
                        '"Left over remainder": {"pp": 0, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Conversion Fee": {"pp": 0, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Security Fee": {"pp": 0, "gp": 0, "sp": 0, "cp": 0}, ' \
                        '"Tithe": {"pp": 0, "gp": 0, "sp": 0, "cp": 0}}'

    # --- INITIALIZATION --- #

    @classmethod
    def setUpClass(cls):
        cls.gold_digger = GoldDigger()
        cls.gold_digger.init()
        cls.source_bag = cls.initBag()
        cls.target_bag = cls.initBag()
        cls.check_bag = cls.initBag()

    @classmethod
    def initBag(cls):
        bag = dict()
        cls.gold_digger.init_bag(bag)
        return bag

    # --- UNIT --- #

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    # def test_tax(self):
    #     self.addGold(self.source_bag, pp=10)
    #     self.addGold(self.check_bag, gp=1)
    #
    #     self.gold_digger.tax(self.source_bag, self.target_bag)
    #     self.assertEqual(self.target_bag, self.check_bag)

    # --- SETUP --- #

    def test_set_coin_bags(self):
        self.gold_digger.set_coin_bags(self.bags)
        self.assertEqual(self.gold_digger.coin_bags, self.bags)

    # --- INTEGRATION --- #

    def test_process(self):
        self.gold_digger.init()
        self.gold_digger.set_coin_bags(self.bags)
        self.gold_digger.set_party_size(5)
        self.gold_digger.process()
        # --- TOTAL --- #
        self.addGold(self.check_bag, 0, 6, 68, 49)  # duplicate
        self.assertEqual(self.check_bag, self.gold_digger.total_coins)  # duplicate
        self.addGold(self.check_bag, 1, 3, 2, 9)
        self.assertEqual(self.check_bag, self.gold_digger.total_value)
        self.addGold(self.check_bag, 0, 1, 13, 9)
        self.assertEqual(self.check_bag, self.gold_digger.member_share)
        self.addGold(self.check_bag, 0, 1, 3, 4)
        # --- REMAINDER --- #
        self.assertEqual(self.check_bag, self.gold_digger.remainder)
        self.addGold(self.check_bag, 0, 0, 2, 6)
        self.assertEqual(self.check_bag, self.gold_digger.remainder_share)
        self.addGold(self.check_bag, 0, 0, 0, 4)
        self.assertEqual(self.check_bag, self.gold_digger.remainder_share_remainder)
        # --- MISCELLANEOUS --- #
        self.addGold(self.check_bag, 0, 0, 1, 4)
        self.assertEqual(self.check_bag, self.gold_digger.tax_man)
        self.addGold(self.check_bag, 0, 1, 3, 3)
        self.assertEqual(self.check_bag, self.gold_digger.tithe)

    def test_parse(self):
        self.gold_digger.init()
        self.gold_digger.set_coin_bags(self.bags)
        self.gold_digger.parse()
        self.addGold(self.check_bag, 0, 6, 68, 49)
        self.assertEqual(self.gold_digger.total_coins, self.check_bag)

    def test_get_json(self):
        self.gold_digger.init()
        self.gold_digger.set_coin_bags(self.bags)
        self.gold_digger.set_party_size(5)
        self.gold_digger.process()
        self.gold_digger.get_json()
        self.assertEqual(self.json, self.gold_digger.json)

    def test_set_json(self):
        total_data = dict()
        self.set_json_check(total_data)

        self.gold_digger.init()
        self.gold_digger.set_json(self.json)
        self.assertEqual(total_data, self.gold_digger.total_data)

    def test_set_json_web(self):
        total_data = dict()
        self.set_json_check(total_data, False)

        self.gold_digger.init()
        self.gold_digger.set_json_web(self.json_web)
        self.gold_digger.process()
        self.assertEqual(total_data, self.gold_digger.total_data)

    def test_set_json_web2(self):
        total_data = dict()
        self.set_json_check2(total_data, False)

        self.gold_digger.init()
        self.gold_digger.set_json_web(self.json_web2)
        self.gold_digger.process()
        self.assertEqual(total_data, self.gold_digger.total_data)

    def test_set_json_web3(self):
        # self.gold_digger.init()
        self.gold_digger.set_json_web(self.json_web3)
        json = self.gold_digger.get_json()

        self.assertEqual(self.json_web3_results, json)

    # --- UTILITY --- #

    @classmethod
    def addGold(cls, bag, pp=0, gp=0, sp=0, cp=0):
        bag[cls.gold_digger.PP] = pp
        bag[cls.gold_digger.GP] = gp
        bag[cls.gold_digger.SP] = sp
        bag[cls.gold_digger.CP] = cp
        return bag

    @classmethod
    def set_json_check(cls, total_data, coin_bags=True):
        # --- TOTAL --- #
        coins_total = dict()
        total_value = dict()
        member_share = dict()
        cls.addGold(coins_total, 0, 6, 68, 49)
        cls.addGold(total_value, 1, 3, 2, 9)
        cls.addGold(member_share, 0, 1, 13, 9)
        total_data[cls.gold_digger.TOTAL_COINS] = coins_total
        total_data[cls.gold_digger.TOTAL_VALUE] = total_value
        total_data[cls.gold_digger.PARTY_MEMBER_SHARE] = member_share

        # --- REMAINDER --- #
        remainder = dict()
        remainder_share = dict()
        remainder_share_remainder = dict()
        cls.addGold(remainder, 0, 1, 3, 4)
        cls.addGold(remainder_share, 0, 0, 2, 6)
        cls.addGold(remainder_share_remainder, 0, 0, 0, 4)
        total_data[cls.gold_digger.LEFT_OVER_COIN] = remainder
        total_data[cls.gold_digger.LEFT_OVER_MEMBER_SHARE] = remainder_share
        total_data[cls.gold_digger.LEFT_OVER_REMAINDER] = remainder_share_remainder

        # --- MISCELLANEOUS --- #
        conversion = dict()
        tax_man = dict()
        tithe = dict()
        cls.addGold(conversion, 0, 0, 1, 4)
        cls.addGold(tax_man, 0, 0, 1, 4)
        cls.addGold(tithe, 0, 1, 3, 3)
        total_data[cls.gold_digger.CONVERSION_FEE] = conversion
        total_data[cls.gold_digger.SECURITY_FEE] = tax_man
        total_data[cls.gold_digger.TITHE_LABEL] = tithe

        # --- PROPERTIES --- #
        if coin_bags:
            total_data[cls.gold_digger.COIN_BAGS] = ["2gp 6sp", "12sp", "2gp 8sp 10cp", "2gp 42sp 39cp"]
        total_data[cls.gold_digger.PARTY_SIZE] = 5
        total_data[cls.gold_digger.FEE_PERCENT_LABEL] = 0.01
        total_data[cls.gold_digger.TAX_PERCENT_LABEL] = 0.01
        total_data[cls.gold_digger.TITHE_PERCENT_LABEL] = 0.1

    @classmethod
    def set_json_check2(cls, total_data, coin_bags=True):
        # --- TOTAL --- #
        coins_total = dict()
        total_value = dict()
        member_share = dict()
        cls.addGold(coins_total, 0, 6, 68, 49)
        cls.addGold(total_value, 1, 3, 2, 9)
        cls.addGold(member_share, 0, 6, 68, 49)
        total_data[cls.gold_digger.TOTAL_COINS] = coins_total
        total_data[cls.gold_digger.TOTAL_VALUE] = total_value
        total_data[cls.gold_digger.PARTY_MEMBER_SHARE] = member_share

        # --- REMAINDER --- #
        remainder = dict()
        remainder_share = dict()
        remainder_share_remainder = dict()

        cls.addGold(remainder, 0, 0, 0, 0)
        cls.addGold(remainder_share, 0, 0, 0, 0)
        cls.addGold(remainder_share_remainder, 0, 0, 0, 0)

        total_data[cls.gold_digger.LEFT_OVER_COIN] = remainder
        total_data[cls.gold_digger.LEFT_OVER_MEMBER_SHARE] = remainder_share
        total_data[cls.gold_digger.LEFT_OVER_REMAINDER] = remainder_share_remainder

        # --- MISCELLANEOUS --- #
        conversion_fee = dict()
        tax_man = dict()
        tithe = dict()

        cls.addGold(conversion_fee, 0, 0, 0, 0)
        cls.addGold(tax_man, 0, 0, 0, 0)
        cls.addGold(tithe, 0, 0, 0, 0)

        total_data[cls.gold_digger.TITHE_LABEL] = tithe
        total_data[cls.gold_digger.CONVERSION_FEE] = conversion_fee
        total_data[cls.gold_digger.SECURITY_FEE] = tax_man

        # --- PROPERTIES --- #
        if coin_bags:
            total_data[cls.gold_digger.COIN_BAGS] = ["2gp 6sp", "12sp", "2gp 8sp 10cp", "2gp 42sp 39cp"]
        total_data[cls.gold_digger.PARTY_SIZE] = 1
        total_data[cls.gold_digger.FEE_PERCENT_LABEL] = 0.0
        total_data[cls.gold_digger.TAX_PERCENT_LABEL] = 0.0
        total_data[cls.gold_digger.TITHE_PERCENT_LABEL] = 0.0

    @classmethod
    def set_json_check3(cls, total_data):
        # --- TOTAL --- #
        coins_total = dict()
        total_value = dict()
        member_share = dict()
        cls.addGold(coins_total, 1, 0, 0, 0)
        cls.addGold(total_value, 1, 0, 0, 0)
        cls.addGold(member_share, 0, 0, 0, 0)
        total_data[cls.gold_digger.TOTAL_COINS] = coins_total
        total_data[cls.gold_digger.TOTAL_VALUE] = total_value
        total_data[cls.gold_digger.PARTY_MEMBER_SHARE] = member_share

        # --- REMAINDER --- #
        remainder = dict()
        remainder_share = dict()
        remainder_share_remainder = dict()

        cls.addGold(remainder, 1, 0, 0, 0)
        cls.addGold(remainder_share, 0, 2, 0, 0)
        cls.addGold(remainder_share_remainder, 0, 0, 0, 0)

        total_data[cls.gold_digger.LEFT_OVER_COIN] = remainder
        total_data[cls.gold_digger.LEFT_OVER_MEMBER_SHARE] = remainder_share
        total_data[cls.gold_digger.LEFT_OVER_REMAINDER] = remainder_share_remainder

        # --- MISCELLANEOUS --- #
        conversion_fee = dict()
        tax_man = dict()
        tithe = dict()

        cls.addGold(conversion_fee, 0, 0, 0, 0)
        cls.addGold(tax_man, 0, 0, 0, 0)
        cls.addGold(tithe, 0, 0, 0, 0)

        total_data[cls.gold_digger.TITHE_LABEL] = tithe
        total_data[cls.gold_digger.CONVERSION_FEE] = conversion_fee
        total_data[cls.gold_digger.SECURITY_FEE] = tax_man

        # --- PROPERTIES --- #
        total_data[cls.gold_digger.PARTY_SIZE] = 5
        total_data[cls.gold_digger.FEE_PERCENT_LABEL] = 0.0
        total_data[cls.gold_digger.TAX_PERCENT_LABEL] = 0.0
        total_data[cls.gold_digger.TITHE_PERCENT_LABEL] = 0.0


if __name__ == '__main__':
    unittest.main()
