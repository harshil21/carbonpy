import pytest
from collections import deque
from carbonpy import ValencyError, CompoundObject, Element

comps = ['CH4', 'CH~CH', 'CH~C-C~C-CH=C=C=CH2', 'CH3-C~C-CH3', 'CH2=CH2', 'CH2=CH-CH=CH-CH=CH2', 'CH~C-CH=CH2']

formulas = ['CH₄', 'C₂H₂', 'C₈H₄', 'C₄H₆', 'C₂H₄', 'C₆H₈', 'C₄H₄']

carbs_hyds = (1, 4), (2, 2), (8, 4), (4, 6), (2, 4), (6, 8), (4, 4)


class TestCompoundObject:

    @pytest.mark.parametrize(argnames='compound,atom', argvalues=zip(comps, carbs_hyds))
    def test_attributes(self, compound, atom):
        comp = CompoundObject(compound)
        assert comp.carbons == atom[0]
        assert comp.hydrogens == atom[1]
        assert len(comp._carbon_comps) - 1 == len(comp._bonds_only)

    @pytest.mark.parametrize(argnames='compound,molecular_form', argvalues=zip(comps, formulas))
    def test_molecular_formula(self, compound, molecular_form):
        assert CompoundObject(compound).molecular_formula() == molecular_form

    def test_molar_mass(self):
        assert round(CompoundObject('CH~CH').molar_mass, 2) == 26.04

    def test_comparisons(self):
        assert CompoundObject('CH~CH') > CompoundObject('CH4') == CompoundObject('CH4') != CompoundObject('CH3-CH3')

    def test_valency_checker(self):
        assert CompoundObject('CH3-CH=CH2').valency_checker()
        assert CompoundObject('CH3-C(-CH=CH-CH3)(-CH2-C~CH)-CH3').valency_checker()

        with pytest.raises(ValencyError):
            CompoundObject('CH3-C=CH2').valency_checker()
            CompoundObject('CH~C-CH(-C(-CH3)(-CH2-CH3)-CH3)-C(-CH=CH(-CH2-CH3)-CH3)(-CH3)-CH2-CH3').valency_checker()

    def test_excess_carbons(self):
        with pytest.raises(ValueError):
            CompoundObject(f"CH3{'-CH2' * 19}-CH3")

    def test_atom_counter(self):
        with pytest.raises(ValueError):
            CompoundObject('CH4').atom_counter('N')

    def test_graph(self):
        a = CompoundObject('CH~C-CH(-C(-CH3)(-CH=CH2)-CH3)-C(-CH=C(-CH3)-CH3)(-CH3)-CH3')
        graph = {'C1': ['C2'],
                 'C2': ['C1', 'C3'],
                 'C3': ['C2', 'C4', 'C9'],
                 'C4': ['C3', 'C5', 'C6', 'C8'],
                 'C5': ['C4'],
                 'C6': ['C4', 'C7'],
                 'C7': ['C6'],
                 'C8': ['C4'],
                 'C9': ['C3', 'C10', 'C14', 'C15'],
                 'C10': ['C9', 'C11'],
                 'C11': ['C10', 'C12', 'C13'],
                 'C12': ['C11'],
                 'C13': ['C11'],
                 'C14': ['C9'],
                 'C15': ['C9']}

        for element, nodes in graph.items():
            assert a.graph[element] == deque(nodes)

    def test_iteration(self):
        for element in CompoundObject('CH3-C(-CH=CH-CH3)(-CH2-C~CH)-CH3'):
            assert isinstance(element, Element)
