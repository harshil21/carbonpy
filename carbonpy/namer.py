#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright © 2020 Harshil Mehta

# namer.py - File containing the Namer class to assign names to chemical compounds.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module names a chemical compound based on IUPAC conventions.
Bonds are represented as follows:
    -   :   Single bond
    =   :   Double bond
    ~   :   Triple bond

Examples:
    CH~CH
    CH~C-C~C-CH=C=C=CH2
"""

import re
from typing import Union

from .error import ValencyError


class Namer(object):  # IUPAC Names for now only

    """
    This class contains methods which helps naming a compound.

    Args:
        structure (:obj:`str`): The condensed chemical structure of the compound.

    Attributes:
        carbons (:obj:`int`): The number of carbon atoms present in the compound.
        hydrogens (:obj:`int`): The number of hydrogen atoms present in the compound.
    """

    prefixes = {1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non", 10: "dec",
                11: "undec", 12: "dodec", 13: "tridec", 14: "tetradec", 15: "pentadec", 16: "hexadec", 17: "heptadec",
                18: "octadec", 19: "nonadec", 20: "icos"}

    multipl_suffixes = {2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "hexa", 7: "hepta", 8: "octa", 9: "nona"}

    symbol = '\u2261'  # The triple bond symbol ≡
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")  # Subscripts for molecular and structural formula

    def __init__(self, structure: str) -> None:
        self.processing = self.structure = structure  # Processing is a string only for processing

        # Counts number of hydrogens and carbons in compound-
        self.carbons = self.atom_counter('C')
        self.hydrogens = self.atom_counter('H')

        self.bond = ""  # Name of bond

    def __str__(self):  # If user wants to see structural formula
        return f"{self.structure.replace('~', self.symbol).translate(self.subscripts)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.structure!r})"

    def molecular_formula(self):  # If user wants to see molecular formula
        """Returns the molecular formula of the compound."""
        return str(f"C{self.carbons if self.carbons > 1 else ''}H{self.hydrogens}").translate(self.subscripts)

    def analyser(self) -> str:
        """
        This method processes the outputs from various functions and finally returns the name of the compound.

        Raises:
            :class:`carbonpy.ValencyError`: If valencies of any one carbon atom is not satisfied.
        """
        compound_name = ""
        many_bonds = ""  # Is empty for saturated compounds

        # Checks valencies of atoms in compound-
        self.valency_checker()
        # Processing and deciding name(s) of the compound-
        bond_type = self.suffix_namer()

        if any(suffix in bond_type for suffix in list(self.multipl_suffixes.values())):
            many_bonds += "a-"  # This is the 'a' in a compound like butadiene
        elif not bond_type == "ane":  # If compound has only one unsaturated bond
            many_bonds += "-"
        compound_name += f"{many_bonds}{bond_type}"  # Suffix and position is decided

        return f"{self.prefixes[self.carbons].capitalize()}{compound_name}"  # returns final name

    def valency_checker(self) -> None:
        """Checks if the valencies of each carbon atom in the compound are satisfied."""
        valency = 0
        hydros_bonds = {'H': 1, "H2": 1, "H3": 2, "H4": 3, '-': 1, '=': 2, '~': 3}
        splitted = re.split('([-=~])', self.structure)  # Splits the bonds and elements

        for index, element in enumerate(splitted):  # Adds the bonds to the string of atoms
            if element == "-" or element == "=" or element == "~":
                splitted[index - 1] += element
                splitted[index + 1] += element
                splitted.pop(index)  # Removes those bonds from the list. Final list example: ['CH3-', 'CH2-', 'CH3-']

        for element in splitted:  # Counts the bonds and hydrogens to see if valency is satisfied
            for hyd_bonds in hydros_bonds.keys():  # Iterating through dict
                if hyd_bonds in element:
                    valency += hydros_bonds[hyd_bonds] * element.count(hyd_bonds)
            if valency != 4:
                raise ValencyError("Check valencies of your compound!")
            valency = 0

    def atom_counter(self, element: str) -> int:
        """
        This method counts the number of occurrences of that element in the compound.
        Currently only supports carbon(C) and hydrogen(H).
        """
        if element == "C":
            return self.structure.count('C')

        elif element == "H":
            count = 0
            hydros = {"H": 1, "H2": 1, "H3": 2, "H4": 3}  # Each value is less than 1 of parent since 'H' is in it too.
            for hydro, value in hydros.items():
                count += self.structure.count(hydro) * value  # Multiplied by its value to get actual value of H
            return count
        else:
            raise ValueError("Only Carbon ('C') and Hydrogen ('H') is supported in this version!")

    def suffix_namer(self) -> str:
        """Assigns one or more suffix(es) based on number of bonds present in the compound."""
        lowest_db = lowest_tb = db_suffix = tb_suffix = ""  # db,tb- double, triple bond
        self.processing = self.processing.translate({ord(i): None for i in 'CH23'})  # Removes everything except bonds

        lows_pos = self.lowest_position()
        if not isinstance(lows_pos, dict):  # If compound is saturated
            return f"ane"  # Alkane

        for key, value in lows_pos.items():
            if value == '=':
                lowest_db += f"{key},"  # Adds position of double bond with ',' for more bonds
            elif value == '~':
                lowest_tb += f"{key},"  # Same as above, except this time for triple bond

        lowest_tb = lowest_tb.strip(',')  # Removes ','
        lowest_db = lowest_db.strip(',')

        # If many double/triple bonds present, get their suffix(di, tri, tetra, etc.)
        if len(lowest_db) >= 3:
            db_suffix = f"-{self.multipl_suffixes[len(lowest_db.replace(',', ''))]}"  # Add that '-' too
        else:
            db_suffix += "-"  # else only '-'

        if len(lowest_tb) >= 3:
            tb_suffix = f"-{self.multipl_suffixes[len(lowest_tb.replace(',', ''))]}"
        else:
            tb_suffix += "-"

        if '=' in self.processing and '~' in self.processing:  # If double and triple bond present
            return f"{lowest_db}{db_suffix}en-{lowest_tb}{tb_suffix}yne"

        elif '~' in self.processing:  # Only triple bond present
            return f"{lowest_tb}{tb_suffix}yne"

        elif '=' in self.processing:  # Only double bond present
            return f"{lowest_db}{db_suffix}ene"  # Return with di,tri,etc

    def lowest_position(self) -> Union[None, dict]:
        """
        This finds the position at which a double or triple bond occurs. The arrangement where the bonds occur at the
        lowest position is selected. The first point of difference rule is followed throughout.
        """
        lowest_front = {}  # Dictionaries containing db and tb as values and its position(int) as keys
        lowest_back = {}
        # TODO: Maybe number from front and back simultaneously? (Also made me realize this may not work for isomers)
        # Adds all occurrences from front
        for index, string in enumerate(self.processing):
            if string in ('=', '~'):
                lowest_front[index + 1] = string

        # Adds all occurrences from back
        for index, string in enumerate(''.join(reversed(self.processing))):
            if string in ('=', '~'):
                lowest_back[index + 1] = string

        assert (len(lowest_front) == len(lowest_back))  # Make sure they have the same length
        for (index, value), (index2, value2) in zip(lowest_front.items(), lowest_back.items()):
            # First point of difference-
            if index < index2:
                return lowest_front
            elif index2 < index:
                return lowest_back
            elif index == index2:  # Same index, check for precedence (only = and ~ for now)
                # Double bond has more precedence than triple
                if value == '=':  # Will change into a dict access for func groups priority
                    return lowest_front
                elif value2 == '=':
                    return lowest_back

        if len(lowest_front) == 0:
            return None
        else:
            return lowest_back  # Can also return lowest_front(if compound is symmetrical)
