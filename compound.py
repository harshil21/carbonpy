# An organic chemistry module for Grade 12(mostly)-
# Can name compounds based on their structure, convert the compound from one functional group to another and more...
# - single bond
# = double bond
# ~ triple bond
# TODO: Identify branched chains, functional groups and somehow represent the compound in the same way you would draw it

import re

from constants import symbol

# Base class for all compounds-


class CompoundObject:  # IUPAC Names for now only
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")  # Subscripts for molecular and structural formula

    def __init__(self, structure: str) -> None:
        self.processing = self.structure = structure.upper()  # Processing is a string only for processing
        self.carbons = 0  # No. of carbon atoms present
        self.hydrogens = 0
        self.final = ""  # Name of final compound

        # Counts number of hydrogens and carbons in compound-
        self.carbons = self.atom_counter('C')
        self.hydrogens = self.atom_counter('H')

        self.comp_dict = {}

    def __str__(self):  # If user wants to see structural formula; called from print()
        return f"{self.structure.replace('~', symbol).translate(self.subscripts)}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.structure!r})"

    def __len__(self):
        return self.carbons

    def __iter__(self):
        self.loop = self.remove_bonds(self.structure).replace('(', ' (').replace(')', ') ').split()
        self.index = 0
        return self

    def __next__(self):
        if self.index <= self.loop.__len__() - 1:
            self.index += 1
            if self.loop[self.index - 1] == "(":
                self.loop[self.index] = '(' + self.loop[self.index]
                self.loop.pop(self.index - 1)

            return self.loop[self.index - 1]

        else:
            raise StopIteration

    def molecular_formula(self) -> str:  # If user wants to see molecular formula
        return str(f"C{self.carbons if self.carbons > 1 else ''}H{self.hydrogens}").translate(self.subscripts)

    def branch_checker(self) -> bool:
        return True if re.search('([()])', self.structure) else False

    @staticmethod
    def remove_bonds(string: str) -> str:
        return string.translate({ord(i): ' ' for i in '-=~'})

    def to_dict(self, start_index: int = 0):
        in_branch = False
        branch_elements = 0
        branches = 0
        print(f"Total number of carbons: {self.carbons}")

        for index, element in enumerate(self):
            print(f"{element}")

            self.comp_dict.setdefault(f'C{index + 1}', {})
            self.comp_dict[f'C{index + 1}'].setdefault('adjacent_carbons', [])
            self.comp_dict[f'C{index + 1}'].setdefault('actual_rep', element)
            self.comp_dict[f'C{index + 1}'].setdefault('is_terminal', False)

        for index, element in zip(range(start_index, len(self)), self):
            if index + 1 == 1:
                self.comp_dict[f'C{index + 1}']['is_terminal'] = True
                continue

            if index + 1 == self.carbons:
                self.comp_dict[f'C{index + 1}']['is_terminal'] = True

                print(f"{branches=}, {branch_elements=}")
                self.comp_dict[f'C{index + 1}']['adjacent_carbons'] = [f'C{self.carbons - branch_elements - 1}']
                self.comp_dict[f'C{self.carbons - branch_elements - 1}']['adjacent_carbons'].append(f'C{index + 1}')
                continue

            if element.startswith('(') and element.endswith(')'):
                branch_elements += 1
                branches += 1
                print(f"Final: {branch_elements=}")
                # if in_branch:

                self.comp_dict[f'C{index + 1}']['is_terminal'] = True

                self.comp_dict[f'C{index + 1}']['adjacent_carbons'] = [f'C{index + 1 - branch_elements}']
                self.comp_dict[f'C{index + 1 - branch_elements}']['adjacent_carbons'].append(f'C{index + 1}')
                continue

            if element.endswith(')'):
                branch_elements += 1

                self.comp_dict[f'C{index + 1}']['is_terminal'] = True

                self.comp_dict[f'C{index + 1}']['adjacent_carbons'] = [f'C{index}']  # Terminal C should've only one adj
                self.comp_dict[f'C{index}']['adjacent_carbons'].append(f'C{index + 1}')
                if in_branch:
                    in_branch = False
                continue

            if element.startswith('C'):
                if not self.comp_dict[f'C{index}']['is_terminal']:
                    self.comp_dict[f'C{index}']['adjacent_carbons'].append(f'C{index + 1}')
                    self.comp_dict[f'C{index + 1}']['adjacent_carbons'].append(f'C{index}')
                else:
                    self.comp_dict[f'C{index + 1}']['adjacent_carbons'].append(f'C{index - branch_elements}')
                    self.comp_dict[f'C{index - branch_elements}']['adjacent_carbons'].append(f'C{index + 1}')

                if in_branch:
                    branch_elements += 1
                    print(f"{branch_elements=}")
                else:
                    branch_elements = 0

            if element.startswith('('):
                # if in_branch:
                #     print('HEREEEE')
                #     return self.to_dict(start_index=index)
                in_branch = True
                branch_elements += 1
                branches += 1
                if not self.comp_dict[f'C{index}']['is_terminal']:
                    self.comp_dict[f'C{index}']['adjacent_carbons'].append(f'C{index + 1}')
                    self.comp_dict[f'C{index + 1}']['adjacent_carbons'].append(f'C{index}')
                else:
                    self.comp_dict[f'C{index + 1}']['adjacent_carbons'].append(f'C{index + 1 - branch_elements}')
                    self.comp_dict[f'C{index + 1 - branch_elements}']['adjacent_carbons'].append(f'C{index + 1}')

        for k, v in self.comp_dict.items():
            print(k, v)

        return self.comp_dict

    def atom_counter(self, element):
        if element.upper() == "C":
            return self.structure.count('C')

        elif element.upper() == "H":
            count = 0
            hydros = {"H": 1, "H2": 1, "H3": 2, "H4": 3}  # Each value is less than 1 of parent since 'H' is in it too.
            for hydro, value in hydros.items():
                count += self.structure.count(hydro) * value  # Multiplied by its value to get actual value of H
            return count
