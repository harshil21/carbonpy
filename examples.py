from namer import BaseNamer, Branched

# Examples-

comp1 = BaseNamer('CH3-C~C-CH3')
comp2 = BaseNamer('CH~CH')
comp3 = BaseNamer('CH~C-C~C-CH=C=C=CH2')
comp4 = BaseNamer('CH4')
comp5 = BaseNamer('CH2=CH-CH=CH-CH=CH2')
comp6 = BaseNamer('CH2=CH2')
comp7 = BaseNamer('CH~C-CH=CH2')
comp8 = Branched('CH3-CH(CH3)-CH3')  # C-C(C)-C
comp9 = Branched('')
print(f"{comp8.longest()}")
comps = [comp1, comp2, comp3, comp4, comp5, comp6, comp7]

for comp in comps:
    print(f"{comp}\n{comp.molecular_formula()}\n{comp.analyser()}\n")
