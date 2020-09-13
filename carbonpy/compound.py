# An organic chemistry module for Grade 12(mostly)-
# Can name compounds based on their structure, convert the compound from one functional group to another and more...
# - single bond
# = double bond
# ~ triple bond
# TODO: Identify functional groups and somehow represent the compound in the same way you would draw it
# TODO: fix imports by adding '.' before merging

import re
from collections import deque
from typing import Dict, Deque

from constants import symbol
from element import Element


class CompoundObject:  # IUPAC Names for now only
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")  # Subscripts for molecular and structural formula

    def __init__(self, structure: str) -> None:
        self.processing = self.structure = structure.upper()  # Processing is a string only for processing
        self._carbons = self.atom_counter('C')

        if self._carbons > 20:
            raise ValueError(f"Got {self._carbons} carbon atoms, this version supports only up to 20 carbon atoms!")

        self._hydrogens = self.atom_counter('H')

        self._carbon_comps = self.processing.translate({ord(i): ' ' for i in '-=~()'}).split()
        self._bonds_only = list(self.processing.translate({ord(i): None for i in 'CH23()'}))
        # assert len(self._carbon_comps) - 1 == len(self._bonds_only)

        self._graph: Dict[Element, Deque[str]] = self.make_graph()

    def __str__(self):  # If user wants to see structural formula; called from print()
        return f"{self.structure.replace('~', symbol).translate(self.subscripts)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.structure!r})"

    def __len__(self) -> int:
        return self.carbons

    def __iter__(self) -> Element:
        for element_node in self._graph:
            yield element_node

    def __eq__(self, other):
        other = other.molar_mass if isinstance(other, self.__class__) else other
        return self.molar_mass == float(other) if isinstance(other, (int, float)) else NotImplemented

    def __lt__(self, other):
        other = other.molar_mass if isinstance(other, self.__class__) else other
        return self.molar_mass < float(other) if isinstance(other, (int, float)) else NotImplemented

    def __le__(self, other):
        other = other.molar_mass if isinstance(other, self.__class__) else other
        return self.molar_mass <= float(other) if isinstance(other, (int, float)) else NotImplemented

    def __gt__(self, other):
        other = other.molar_mass if isinstance(other, self.__class__) else other
        return self.molar_mass > float(other) if isinstance(other, (int, float)) else NotImplemented

    def __ge__(self, other):
        other = other.molar_mass if isinstance(other, self.__class__) else other
        return self.molar_mass >= float(other) if isinstance(other, (int, float)) else NotImplemented

    @property
    def graph(self) -> Dict[Element, Deque[str]]:
        return self._graph

    @property
    def molar_mass(self) -> float:
        molar_masses = {'C': 12.0107, 'H': 1.00784}
        return molar_masses['C'] * self.carbons + molar_masses['H'] * self.hydrogens

    @property
    def carbons(self) -> int:
        return self._carbons

    @property
    def hydrogens(self) -> int:
        return self._hydrogens

    def molecular_formula(self) -> str:  # If user wants to see molecular formula
        return str(f"C{self.carbons if self.carbons > 1 else ''}H{self.hydrogens}").translate(self.subscripts)

    def branch_checker(self) -> bool:
        return True if re.search('([()])', self.structure) else False

    @staticmethod
    def _remove_bonds(string: str) -> str:
        return string.translate({ord(i): ' ' for i in '-=~'})

    @staticmethod
    def add_edge(obj: dict, prev_element: str, this_element: str):
        obj.setdefault(prev_element, deque([]))
        obj.setdefault(this_element, deque([]))

        obj[prev_element].append(this_element)
        obj[this_element].append(prev_element)
        return obj

    def atom_counter(self, element):
        if element.upper() == "C":
            return self.structure.count('C')

        elif element.upper() == "H":
            count = 0
            hydros = {"H": 1, "H2": 1, "H3": 2, "H4": 3}  # Each value is less than 1 of parent since 'H' is in it too.
            for hydro, value in hydros.items():
                count += self.structure.count(hydro) * value  # Multiplied by its value to get actual value of H
            return count

    def to_element(self, graph: dict):
        _graph = {}
        for element_node, connected_nodes in graph.items():
            element = Element(value=element_node, comp=self._carbon_comps[int(element_node[1:]) - 1])

            position = max(0, int(element_node[1:]) - 2)
            element.back_bond = self._bonds_only[position]

            for node, at in zip(range(1, len(connected_nodes)), {'front_bond', 'top_bond', 'bottom_bond'}):
                position = int(connected_nodes[node][1:]) - 2
                setattr(element, at, self._bonds_only[position])

            _graph[element] = connected_nodes
        return _graph

    def make_graph(self):
        _graph: Dict[str, Deque[str]] = {}
        to_repl = {'-': ' ', '=': ' ', '~': ' ', 'C(': 'C (', 'H(': 'H (', 'H)': 'H )', 'H2)': 'H2 )', 'H3)': 'H3 )',
                   ')(': ') ('}
        splitted = self.structure
        for k, v in to_repl.items():
            splitted = splitted.replace(k, v)
        splitted = splitted.split()
        # print(f"{splitted=}")
        branch_elements = deque([])
        visited = deque(['C1'])
        carbon_indexes = []
        index = 0
        for ele in splitted:
            if 'C' in ele:
                index += 1
            carbon_indexes.append(index)

        previous = splitted[0]

        for index, element in zip(carbon_indexes[1:], splitted[1:]):
            if previous != ')' and element == '(':
                branch_elements.extend([visited[-1]] * 3)
                previous = element
                continue

            if previous == ")" and element != '(':
                popped1 = branch_elements.pop()
                _graph = self.add_edge(_graph, popped1, f"C{index}")
                if branch_elements and popped1 == branch_elements[-1]:
                    branch_elements.pop()

            elif previous == ")" and element == "(":
                _graph = self.add_edge(_graph, branch_elements.pop(), f"C{index + 1}")

            elif previous == "(" and f"C{index}" not in _graph:
                _graph = self.add_edge(_graph, branch_elements.pop(), f"C{index}")

            elif previous != "(" and element != ')':
                _graph = self.add_edge(_graph, visited[-1], f"C{index}")

            visited.append(f"C{index}")
            previous = element

        _graph: Dict[Element, Deque[str]] = self.to_element(_graph)  # Convert string nodes to Element nodes
        return _graph

# a = CompoundObject(structure="CH3-C(=CH-C~CH)(-CH=CH2)-C~CH")
# a = CompoundObject(structure="CH~C-CH(-C(-CH3)(-CH2-CH3)-CH3)-C(-CH=CH(-CH2-CH3)-CH3)(-CH3)-CH2-CH3")
#
# print(a.carbons)
# for element in a:
#     print(element)
