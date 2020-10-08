from namer import Branched, BaseNamer

# Examples-

# comp1 = BaseNamer('CH2=C=C=C=CH2')
# comp2 = BaseNamer('CH~C-CH3')
# comp3 = BaseNamer('CH~C-C~C-CH=C=C=CH2')
# comp4 = BaseNamer('CH4')
# comp5 = BaseNamer('CH2=CH-CH=CH-CH=CH2')
# comp6 = BaseNamer('CH2=CH2')
# comp7 = BaseNamer('CH~C-CH=CH2')
# comp_tmp = Branched('CH4')
# comp_tmp2 = Branched('CH3-CH3')
comp8 = Branched('CH3-CH(-CH3)-CH3')
comp9 = Branched('CH3-C(-CH=C=CH2)(-CH3)-CH3')
comp10 = Branched('CH3-C(-CH2-CH2-CH3)(-CH2-CH2-CH3)-CH3')
comp11 = Branched('CH~C-CH(-C(-CH3)(-CH2-CH3)-CH3)-C(-CH=C(-CH2-CH3)-CH3)(-CH3)-CH2-CH3')
# comp12 = Branched('CH3-C(-CH2-CH(-CH3)-CH3)(-CH3)-CH2-CH3')

# comp10 = Branched('CH3-CH(-CH2-CH3)-CH3')  # 2-methylbutane. This shows user can input structure in any order!
# print(f"func :{comp8.branch_splitter()}")
# print()
# a = comp8.determine_longest()
# print()
# b = comp9.determine_longest()
# print()
# c = comp11.determine_longest()
# print()
comp11.valency_checker()

# comps = [comp1, comp2, comp3, comp4, comp5, comp6, comp7]

# for comp in comps:
#     print(f"{comp}\n{comp.molecular_formula()}\n{comp.analyser()}\n")
