import pytest

from carbonpy import BaseNamer


names = ['methane', 'acetylene', 'octa-1,2,3-trien-5,7-diyne', 'but-2-yne', 'eth-1-ene', 'hexa-1,3,5-triene',
         'but-1-en-3-yne']

comps = ['CH4', 'CH~CH', 'CH~C-C~C-CH=C=C=CH2', 'CH3-C~C-CH3', 'CH2=CH2', 'CH2=CH-CH=CH-CH=CH2', 'CH~C-CH=CH2']


@pytest.mark.parametrize(argnames='compound,name', argvalues=zip(comps, names))
def test_analyser(compound, name):
    assert BaseNamer(compound).analyser() == name
