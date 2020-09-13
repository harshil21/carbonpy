from collections import deque
from typing import Union, List

from compound import CompoundObject
from element import Element
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
        self.processing = self.processing.translate({ord(i): None for i in 'CH23'})  # Removes everything except bonds

    def valency_checker(self) -> None:
        """Checks if valencies of carbon are satisfied and raises error if not satisfied."""

        hydros_bonds = {'H': 1, "H2": 1, "H3": 2, "H4": 3, '-': 1, '=': 2, '~': 3}
        splitted = []
        carbon_index = 0

        for element in self.graph:  # Final list example: ['CH3-', 'CH2--', 'CH3-']
            compound = ''
            for attr in ('comp', 'front_bond', 'back_bond', 'top_bond', 'bottom_bond'):
                value = getattr(element, attr)
                if value != '':
                    compound += value
            splitted.append(compound)

        for element in splitted:  # Counts the bonds and hydrogens to see if valency is satisfied
            valency = 0
            for hyd_bonds in hydros_bonds.keys():  # Iterating through dict
                if hyd_bonds in element:
                    valency += hydros_bonds[hyd_bonds] * element.count(hyd_bonds)
            carbon_index = self.structure.find('C', carbon_index) + 1
            if valency != 4:
                raise ValencyError(f"Check valencies of your compound!\n{self.structure}\n{' ' * (carbon_index - 1)}^")

    def lowest_position(self) -> Union[None, dict]:
        """First point of difference rule used"""
        lowest_front = {}
        lowest_back = {}
        # TODO: Maybe number from front and back simultaneously? (Also made me realize this may not work for isomers)
        self.bonds_only()
        # print(self.processing)
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
    def traverse_node(self, terminal_node: Element):
        # Using DFS approach-
        stack, visited = deque([terminal_node.value]), deque([terminal_node.value])
        path = terminal_node.value

        while stack:
            # noinspection PyTypeChecker
            next_nodes = self.graph[stack[-1]]
            if len(next_nodes) == 1 and path.count('C') > 1:  # When terminal node is reached
                yield path.split('-')

            for node in next_nodes:
                if node not in visited:
                    path += f"-{node}"
                    visited.append(node)
                    stack.append(node)
                    break
            else:
                stack.pop()
                path = "-".join(stack)

    def determine_longest(self):
        possible_paths: List[List[str]] = []
        longest_paths: List[List[str]] = []
        length: int = 1

        def calculate_longest(path_list):
            nonlocal length, longest_paths
            if len(path_list) > length:
                length = len(path_list)
                longest_paths = [path_list]
            elif len(path_list) == length:
                longest_paths.append(path_list)

        for terminal_node, value in self.graph.items():
            if len(value) == 1:
                for path in self.traverse_node(terminal_node=terminal_node):
                    possible_paths.append(path)

        list(map(calculate_longest, possible_paths))
        # print(possible_paths)
        # print(f"Number of possible paths: {len(possible_paths)}")
        # print(longest_paths)
        return longest_paths

    # def branch_splitter(self):  # split branches and pass each of them to longest()
    #
    #     print(self.processing)
    #     regex = re.compile('\((.*?)\)')
    #     chain = re.compile('C[H]*\((.*?)\).+')
    #     branches: list = regex.findall(self.processing)
    #     chained = chain.search(self.processing)
    #     print(chained)
    #     if branches:
    #         print(f"matched: {branches}")
    #         for match in branches:
    #             self.processing = re.sub(f'\({match}\)', '', self.processing)
    #         branches.append(self.processing)
    #         print(self.processing)
    #     print(branches)
    # self.longest(branches)
