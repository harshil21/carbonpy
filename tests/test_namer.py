import pytest
from carbonpy import Namer, ValencyError

comps = ['CH4', 'CH~CH', 'CH~C-C~C-CH=C=C=CH2', 'CH3-C~C-CH3', 'CH2=CH2', 'CH2=CH-CH=CH-CH=CH2', 'CH~C-CH=CH2']

names = ['Methane', 'Eth-1-yne', 'Octa-1,2,3-trien-5,7-diyne', 'But-2-yne', 'Eth-1-ene', 'Hexa-1,3,5-triene',
         'But-1-en-3-yne']

formulas = ['CH₄', 'C₂H₂', 'C₈H₄', 'C₄H₆', 'C₂H₄', 'C₆H₈', 'C₄H₄']

carbs_hyds = (1, 4), (2, 2), (8, 4), (4, 6), (2, 4), (6, 8), (4, 4)


@pytest.fixture(params=comps)
def compound(request):
    return request.param


@pytest.fixture(params=names)
def name(request):
    return request.param


@pytest.fixture(params=formulas)
def molecular_form(request):
    return request.param


@pytest.fixture(params=carbs_hyds)
def carb_hyd(request):
    return request.param


class TestNamer:

    @pytest.mark.parametrize(argnames='compound,atom', argvalues=zip(comps, carbs_hyds))
    def test_attributes(self, compound, atom):
        comp = Namer(compound)
        assert comp.carbons == atom[0]
        assert comp.hydrogens == atom[1]

    @pytest.mark.parametrize(argnames='compound,molecular_form', argvalues=zip(comps, formulas), indirect=True)
    def test_molecular_formula(self, compound, molecular_form):
        assert Namer(compound).molecular_formula() == molecular_form

    @pytest.mark.parametrize(argnames='compound,name', argvalues=zip(comps, names), indirect=True)
    def test_analyser(self, compound, name):
        assert Namer(compound).analyser() == name

    def test_valency_checker(self):
        with pytest.raises(ValencyError):
            Namer('CH3-C=CH2').valency_checker()

    def test_excess_carbons(self):
        with pytest.raises(ValueError):
            Namer(f"CH3{'-CH2' * 19}-CH3")

    def test_atom_counter(self):
        with pytest.raises(ValueError):
            Namer('CH4').atom_counter('N')
