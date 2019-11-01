# An organic chemistry module for Grade 12(mostly)-
# Can name compounds based on their structure, convert the compound from one functional group to another and more...
# - single bond
# = double bond
# ~ triple bond
# TODO: Identify branched chains, functional groups and somehow represent the compound in the same way you would draw it


class Namer(object):  # IUPAC Names for now only
    symbol = '\u2261'  # The triple bond symbol ≡
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")  # Subscripts for molecular and structural formula

    def __init__(self, structure):
        self.processing = self.structure = structure  # Processing is a string only for processing
        self.carbons = 0  # No. of carbon atoms present
        self.hydrogens = 0
        self.bond = ""  # Name of bond
        # self.final = ""  # Name of final compound

        # Counts number of hydrogens and carbons in compound-
        self.carbons = self.atom_counter('C')
        self.hydrogens = self.atom_counter('H')

    def analyser(self):
        compound_name = ""
        many_bonds = ""  # Is empty for saturated compounds

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

    def valency_checker(self):
        """Checks if valencies of carbon are satisfied the same way you would do in real life, by counting no. of
        atoms and bonds before and after the carbon."""

        values = {'H': 1, '-': 1, '=': 2, '~': 3}
        # use these as examples to understand code below 'CH3-CH=C=CH2', 'CH~CH':
        for index, atom in enumerate(self.structure):
            if atom == 'C':
                valency = 0  # Valency of each carbon before calculating
                try:
                    if self.structure[index + 2].isdigit():  # If atoms after carbon
                        valency += int(self.structure[index + 2])  # Adds those atoms
                        valency += values[self.structure[index + 3]]  # And the bond (if it isn't terminal carbon)

                    elif self.structure[index + 2] in values.keys():  # If single H / bonds present
                        valency += values[self.structure[index + 2]]  # Add that bond value
                        valency += values[self.structure[index + 1]]  # Add that atom
                    else:
                        valency += values[self.structure[index + 1]]  # Add either atom or bond value

                except (IndexError, KeyError):
                    if self.structure[-1] == 'H':  # If last carbon has atom
                        valency += 1  # Add that

                if valency != 4 and index != 0:  # If valency isn't 4 yet
                    previous_bond = self.structure[index - 1]
                    valency += values[previous_bond]  # Add previous bond value

                if valency != 4:  # If it still isn't four!!!
                    raise ValencyError("Check valencies of your compound!")

    def atom_counter(self, element):
        if element == "C":
            return self.structure.count('C')

        elif element == "H":
            count = 0
            hydros = {"H": 1, "H2": 1, "H3": 2, "H4": 3}  # Each value is less than 1 of parent since 'H' is in it too.
            for hydro, value in hydros.items():
                count += self.structure.count(hydro) * value  # Multiplied by its value to get actual value of H
            return count

    def suffix_namer(self):
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

    def lowest_position(self):
        """First point of difference rule used"""
        lowest_front = {}
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
            return lowest_back  # Can also return front(if compound is symmetrical)

    def priority_order(self):
        pass

    def struct_formula(self):  # If user wants to see structural formula
        return f"{self.structure.replace('~', self.symbol).translate(self.subscripts)}"

    def molecular_formula(self):  # If user wants to see molecular formula
        return str(f"C{self.carbons if self.carbons > 1 else ''}H{self.hydrogens}").translate(self.subscripts)


class ValencyError(Exception):
    pass


prefixes = {1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non", 10: "dec",
            11: "undec", 12: "dodec", 13: "tridec", 14: "tetradec", 15: "pentadec", 16: "hexadec", 17: "heptadec",
            18: "octadec", 19: "nonadec", 20: "icos"}

# precedence = {"=": 1, "~": 1}

multipl_suffixes = {2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "hexa", 7: "hepta", 8: "octa", 9: "nona"}

compound1 = Namer('CH3-C~C-CH3')
compound2 = Namer('CH~CH')
compound3 = Namer('CH~C-C~C-CH=C=C=CH2')
compound4 = Namer('CH4')
compound5 = Namer('CH2=CH-CH=CH-CH=CH2')
compound6 = Namer('CH2=CH2')
compound7 = Namer('CH~C-CH=CH2')

print(f"{compound1.struct_formula()}\n{compound1.molecular_formula()}\n{compound1.analyser()}\n")
print(f"{compound2.struct_formula()}\n{compound2.molecular_formula()}\n{compound2.analyser()}\n")
print(f"{compound3.struct_formula()}\n{compound3.molecular_formula()}\n{compound3.analyser()}\n")
print(f"{compound4.struct_formula()}\n{compound4.molecular_formula()}\n{compound4.analyser()}\n")
print(f"{compound5.struct_formula()}\n{compound5.molecular_formula()}\n{compound5.analyser()}\n")
print(f"{compound6.struct_formula()}\n{compound6.molecular_formula()}\n{compound6.analyser()}\n")
print(f"{compound7.struct_formula()}\n{compound7.molecular_formula()}\n{compound7.analyser()}\n")
