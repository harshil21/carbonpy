import pytest

from carbonpy import Element


element_dict = {}
values = (1, 2, 3)

elements = [Element('C1', 'CH3'), Element('C2', 'CH'), Element('C3', 'C')]

comp_n_value = (('C1', 'CH3', 3), ('C2', 'CH', 1), ('C3', 'C', 0))


@pytest.fixture(params=elements)
def element(request):
    return request.param


@pytest.mark.parametrize(argnames='element,attr', argvalues=zip(elements, comp_n_value))
def test_element_attributes(element, attr):
    assert element.value == attr[0] and element.comp == attr[1] and element.hydrogens() == attr[2]


@pytest.mark.parametrize(argnames='element,value', argvalues=zip(elements, values))
def test_dict_access(element, value):
    element_dict[element] = value
    assert element_dict[element] == element_dict[element.value] == value
