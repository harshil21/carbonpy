from typing import Union
import re

from compound import CompoundObject
from error import ValencyError
from constants import multipl_suffixes, prefixes


class BaseNamer(CompoundObject):
    def analyser(self) -> str:
        compound_name = ""
        many_bonds = ""  # Is empty for saturated compounds

        if self.branch_checker():
            pass

        # Checks valencies of atoms in compound-
        self.valency_checker()
        # Processing and deciding name(s) of the compound-
        bond_type = self.suffix_namer()

        if any(suffix in bond_type for suffix in list(multipl_suffixes.values())):
            many_bonds += "a-"  # This is the 'a' in a compound like butadiene
        elif not bond_type == "ane":  # If compound has only one unsaturated bond
            many_bonds += "-"
        compound_name += f"{many_bonds}{bond_type}"  # Suffix and position is decided

        return f"{prefixes[self.carbons].capitalize()}{compound_name}"  # returns final name

    def suffix_namer(self) -> str:
        lowest_db = lowest_tb = db_suffix = tb_suffix = ""  # db,tb- double, triple bond

        lows_pos = self.lowest_position()
        if not isinstance(lows_pos, dict):  # If compound is saturated
            return "ane"  # Alkane

        for key, value in lows_pos.items():
            if value == '=':
                lowest_db += f"{key},"  # Adds position of double bond with ',' for more bonds
            elif value == '~':
                lowest_tb += f"{key},"  # Same as above, except this time for triple bond

        lowest_tb = lowest_tb.strip(',')  # Removes ','
        lowest_db = lowest_db.strip(',')

        # If many double/triple bonds present, get their suffix(di, tri, tetra, etc.)
        if len(lowest_db) >= 3:
            db_suffix = f"-{multipl_suffixes[len(lowest_db.replace(',', ''))]}"  # Add that '-' too
        else:
            db_suffix += "-"  # else only '-'

        if len(lowest_tb) >= 3:
            tb_suffix = f"-{multipl_suffixes[len(lowest_tb.replace(',', ''))]}"
        else:
            tb_suffix += "-"

        if '=' in self.processing and '~' in self.processing:  # If double and triple bond present
            return f"{lowest_db}{db_suffix}en-{lowest_tb}{tb_suffix}yne"

        elif '~' in self.processing:  # Only triple bond present
            return f"{lowest_tb}{tb_suffix}yne"

        elif '=' in self.processing:  # Only double bond present
            return f"{lowest_db}{db_suffix}ene"  # Return with di,tri,etc

    def bonds_only(self):
        print('im here')
        self.processing = self.processing.translate({ord(i): None for i in 'CH23'})  # Removes everything except bonds

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

    def lowest_position(self) -> Union[None, dict]:
        """First point of difference rule used"""
        lowest_front = {}
        lowest_back = {}
        # TODO: Maybe number from front and back simultaneously? (Also made me realize this may not work for isomers)
        self.bonds_only()
        print(self.processing)
        # Adds all occurrences from front
        for index, string in enumerate(self.processing):
            if string in ('=', '~'):
                lowest_front[index + 1] = string  # Adds position no. of bond

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
            return lowest_back  # Can also return front(if compound is symmetrical)

    def priority_order(self):
        pass


class Branched(BaseNamer):
    # TODO: Adding chains
    # def longest(self, chains: list):
    #     chains = [CompoundObject(structure) for structure in chains]
    #     longest_chain = max(compound.atom_counter('C') for compound in chains)
    #     print(longest_chain)
    #     print(self.processing)

    def branch_splitter(self):  # split branches and pass each of them to longest()

        print(self.processing)
        regex = re.compile('\((.*?)\)')
        chain = re.compile('C[H]*\((.*?)\).+')
        branches: list = regex.findall(self.processing)
        chained = chain.search(self.processing)
        print(chained)
        if branches:
            print(f"matched: {branches}")
            for match in branches:
                self.processing = re.sub(f'\({match}\)', '', self.processing)
            branches.append(self.processing)
            print(self.processing)
        print(branches)
        # self.longest(branches)
