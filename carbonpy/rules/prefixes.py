common = {5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non", 10: "dec",
          11: "undec", 20: "icos", 30: "tricont", 40: "tetracont", 50: "pentacont", 60: "hexacont",
          70: "heptacont", 80: "octacont", 90: "nonacont", 100: "hect", 101: "henhect", 200: "dict", 300: "trict",
          400: "tetract", 500: "pentact", 600: "hexact", 700: "heptact", 800: "octact", 900: "nonact", 1000: "kili",
          1001: "henkili", 2000: "dili", 3000: "trili", 4000: "tetrali", 5000: "pentali", 6000: "hexali",
          7000: "heptali", 8000: "octali", 9000: "nonali"}

# For parent carbon chain-
prefixes = {1: "meth", 2: "eth", 3: "prop", 4: "but", **common}
# For multiple branches, bonds-
multi_prefixes = {1: "mono", 2: "di", 3: "tri", 4: "tetra", **{k: f"{v}a" for k, v in common.items()}}


def to_place_values(num: int):
    if num > 99 and num % 100 == 11:
        yield 11
        num -= 11

    value = 1
    while num != 0:
        last = num % 10
        yield last * value
        num //= 10
        value *= 10


def get_prefix(count: int, parent: bool = False):
    try:
        return prefixes[count] if parent else multi_prefixes[count]
    except KeyError:
        pass

    prefix = ""
    for num in to_place_values(count):
        if num == 0:
            continue
        elif num == 1:
            prefix += "hen"
        elif num == 2:
            prefix += "do"
        elif num == 11:  # Special case for 11 where undeca will be used
            prefix += multi_prefixes[num]
        elif num == 20 and prefix[-1] in "aeiou":  # 'i' in 'icosa' is elided if it's after a vowel
            prefix += multi_prefixes[num][1:]
        else:
            prefix += multi_prefixes[num]
    return prefix[:-1] if parent else prefix
