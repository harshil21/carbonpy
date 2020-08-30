from namer import BaseNamer, Branched

# Examples-

# comp1 = BaseNamer('CH3-C~C-CH3')
# comp2 = BaseNamer('CH~CH')
# comp3 = BaseNamer('CH~C-C~C-CH=C=C=CH2')
# comp4 = BaseNamer('CH4')
# comp5 = BaseNamer('CH2=CH-CH=CH-CH=CH2')
# comp6 = BaseNamer('CH2=CH2')
# comp7 = BaseNamer('CH~C-CH=CH2')
comp_tmp = Branched('CH4')
comp_tmp2 = Branched('CH3-CH3')
comp8 = Branched('CH3-CH(-CH3)-CH3')  # C-C(C)-C
comp9 = Branched('CH3-C(-CH2-CH2-CH3)(-CH3)-CH3')
comp10 = Branched('CH3-C(-CH2-CH2-CH3)(-CH2-CH2-CH3)-CH3')
comp11 = Branched('CH3-C(-CH2-CH2-CH3)(-CH3)-CH-(-CH3)-CH3')
comp12 = Branched('CH3-C(-CH2-CH(-CH3)-CH3)(-CH3)-CH2-CH3')

# comp10 = Branched('CH3-CH(-CH2-CH3)-CH3')  # 2-methylbutane. This shows user can input structure in any order!
# print(f"func :{comp8.branch_splitter()}")
print()
a = comp8.to_dict()
print()
b = comp9.to_dict()
print()
c = comp10.to_dict()
print()
d = comp11.to_dict()
print()
e = comp12.to_dict()


def test_case():
    assert a['C1']['adjacent_carbons'] == ['C2']
    assert a['C2']['adjacent_carbons'] == ['C1', 'C3', 'C4']
    assert a['C3']['adjacent_carbons'] == ['C2']
    assert a['C4']['adjacent_carbons'] == ['C2']

    assert b['C1']['adjacent_carbons'] == ['C2']
    assert b['C2']['adjacent_carbons'] == ['C1', 'C3', 'C6', 'C7']
    assert b['C3']['adjacent_carbons'] == ['C2', 'C4']
    assert b['C4']['adjacent_carbons'] == ['C3', 'C5']
    assert b['C5']['adjacent_carbons'] == ['C4']
    assert b['C6']['adjacent_carbons'] == ['C2']
    assert b['C7']['adjacent_carbons'] == ['C2']

    assert c['C1']['adjacent_carbons'] == ['C2']
    assert c['C2']['adjacent_carbons'] == ['C1', 'C3', 'C6', 'C9']
    assert c['C3']['adjacent_carbons'] == ['C2', 'C4']
    assert c['C4']['adjacent_carbons'] == ['C3', 'C5']
    assert c['C5']['adjacent_carbons'] == ['C4']
    assert c['C6']['adjacent_carbons'] == ['C2', 'C7']
    assert c['C7']['adjacent_carbons'] == ['C6', 'C8']
    assert c['C8']['adjacent_carbons'] == ['C7']
    assert c['C9']['adjacent_carbons'] == ['C2']

    assert d['C1']['adjacent_carbons'] == ['C2']
    assert d['C2']['adjacent_carbons'] == ['C1', 'C3', 'C6', 'C7']
    assert d['C3']['adjacent_carbons'] == ['C2', 'C4']
    assert d['C4']['adjacent_carbons'] == ['C3', 'C5']
    assert d['C5']['adjacent_carbons'] == ['C4']
    assert d['C6']['adjacent_carbons'] == ['C2']
    assert d['C7']['adjacent_carbons'] == ['C2', 'C8', 'C9']
    assert d['C8']['adjacent_carbons'] == ['C7']
    assert d['C9']['adjacent_carbons'] == ['C7']


test_case()

# print(f'func: {comp9.branch_splitter()}')
# print(f'func: {comp10.branch_splitter()}')

# comps = [comp1, comp2, comp3, comp4, comp5, comp6, comp7]

# for comp in comps:
#     print(f"{comp}\n{comp.molecular_formula()}\n{comp.analyser()}\n")
