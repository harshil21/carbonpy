# An organic chemistry module for Grade 12(mostly)-
# Can name compounds based on their structure, convert the compound from one functional group to another and more...
# - single bond
# = double bond
# ~ triple bond
# TODO: Identify branched chains, functional groups and somehow represent the compound in the same way you would draw it

import re

from constants import symbol
from error import ValencyError


class CompoundObject(object):  # IUPAC Names for now only
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")  # Subscripts for molecular and structural formula

    def __init__(self, structure: str, **kwargs) -> None:
        self.processing = self.structure = structure  # Processing is a string only for processing
        self.carbons = 0  # No. of carbon atoms present
        self.hydrogens = 0
        self.final = ""  # Name of final compound
        super().__init__(**kwargs)

        # Counts number of hydrogens and carbons in compound-
        self.carbons = self.atom_counter('C')
        self.hydrogens = self.atom_counter('H')

    def __str__(self):  # If user wants to see structural formula
        return f"{self.structure.replace('~', symbol).translate(self.subscripts)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.structure!r})"

    def molecular_formula(self):  # If user wants to see molecular formula
        return str(f"C{self.carbons if self.carbons > 1 else ''}H{self.hydrogens}").translate(self.subscripts)

    def branch_checker(self):
        return True if re.search('([()])', self.structure) else False

    def atom_counter(self, element):
        if element == "C":
            return self.structure.count('C')

        elif element == "H":
            count = 0
            hydros = {"H": 1, "H2": 1, "H3": 2, "H4": 3}  # Each value is less than 1 of parent since 'H' is in it too.
            for hydro, value in hydros.items():
                count += self.structure.count(hydro) * value  # Multiplied by its value to get actual value of H
            return count

    def valency_checker(self) -> None:
        """Checks if valencies of carbon are satisfied and raises error if not satisfied."""

        hydros_bonds = {'H': 1, "H2": 1, "H3": 2, "H4": 3, '-': 1, '=': 2, '~': 3}
        splitted = re.split('([-=~])', self.structure)  # Splits the bonds and elements

        for index, element in enumerate(splitted):  # Adds the bonds to the string of atoms
            if element == "-" or element == "=" or element == "~":
                splitted[index - 1] += element
                splitted[index + 1] += element
                splitted.pop(index)  # Removes those bonds from the list. Final list example: ['CH3-', 'CH2--', 'CH3-']

        for element in splitted:  # Counts the bonds and hydrogens to see if valency is satisfied
            valency = 0
            for hyd_bonds in hydros_bonds.keys():  # Iterating through dict
                if hyd_bonds in element:
                    valency += hydros_bonds[hyd_bonds] * element.count(hyd_bonds)
            if valency != 4:
                raise ValencyError("Check valencies of your compound!")
