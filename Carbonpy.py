# An organic chemistry module for Grade 12(mostly)-
# Can name compounds based on their structure, convert the compound from one functional group to another and more...
# - single bond
# = double bond
# ~ triple bond
# TODO: Should be able to identify multiple bonds in a compound, identify branched chains, and 
#  somehow represent thecompound in the same way you would draw it


class Namer(object):  # IUPAC Names for now only

    def __init__(self, structure):
        self.structure = structure
        self.carbons = 0  # No. of carbon atoms present
        self.hydrogens = 0
        self.bond = ""  # Name of bond
        # self.final = ""  # Name of final compound
        self.processing = []  # List for analysing given compound

    def analyser(self):
        compound_name = ""

        # Counts number of hydrogens and carbons in compound-
        self.carbons = self.atom_counter('C')
        self.hydrogens = self.atom_counter('H')

        # If compound valencies not satisfied-
        self.compound_check()

        # Processing and deciding name(s) of the compound-
        if '~' in self.structure:  # For alkynes
            self.bond = "yne"
            triple_bonds = self.structure.count('~')
            self.processing = self.structure.split('~')
            bond_type = self.alkynes_namer()
            compound_name += f"-{bond_type}"  # Suffix and position is decided

        if '=' in self.structure:  # For alkenes
            double_bonds = self.structure.count('=')
            self.processing = self.structure.split('=')
            bond_type = self.alkenes_namer()
            self.bond = "ene"
            compound_name += f"-{bond_type}"  # Suffix and position is decided

        if '~' not in self.structure and '=' not in self.structure:  # For alkanes
            self.bond = "ane"
            compound_name += self.bond

        return f"{prefixes[self.carbons].capitalize()}{compound_name}"  # returns final name

    def compound_check(self):
        """Checks if valencies of carbon are satisfied the same way you would do in real life, by counting no of
        hydrogens and bonds before and after the carbon."""

        values = {'H': 1, '-': 1, '=': 2, '~': 3}
        # 'CH3-CH=C=CH2'
        # 'CH~CH'
        for index, atom in enumerate(self.structure):
            if atom == 'C':
                valency = 0  # Valency of each carbon before calculating
                try:
                    if self.structure[index + 2].isdigit():  # If hydrogens after carbon
                        valency += int(self.structure[index + 2])  # Adds those hydrogens
                        valency += values[self.structure[index + 3]]  # And the bond (if it isn't terminal carbon)

                    elif self.structure[index + 2] in values.keys():  # If single H / bonds present
                        valency += values[self.structure[index + 2]]  # Add that bond value
                        valency += values[self.structure[index + 1]]  # Add that hydrogen
                    else:
                        valency += values[self.structure[index + 1]]  # Add either hydrogen or bond value

                except (IndexError, KeyError):
                    if self.structure[-1] == 'H':  # If last carbon has hydrogen
                        valency += 1  # Add that

                finally:
                    if valency != 4 and index != 0:  # If valency isn't 4 yet
                        previous_bond = self.structure[index - 1]
                        valency += values[previous_bond]  # Add previous bond value

                    if valency != 4:  # If it still isn't four!!!
                        raise ValencyError("Check valencies of your compound!")

        # This system wouldn't work if multiple different type of bonds are present-
        # if '-' in self.structure and 2 * self.carbons + 2 == self.hydrogens:  # If in the form CnH(2n+2): Alkanes
        #     return True
        # elif '=' in self.structure and 2 * self.carbons == self.hydrogens:  # If in the form CnH2n: Alkenes
        #     return True
        # elif '~' in self.structure and 2 * self.carbons - 2 == self.hydrogens:  # If in the form CnH(2n-2): Alkynes
        #     return True
        # else:
        #     return False

    def atom_counter(self, element):
        count = 0
        for index, atom in enumerate(self.structure):
            try:
                subscript = self.structure[index + 1]

            except IndexError:  # If last atom is reached
                if self.structure[-1] == element:  # Checks if element is present in the last position
                    count += 1
            else:
                if atom == element and subscript.isdigit():  # If subscript is present after the specified atom,
                    count += int(subscript)  # add that number

                elif atom == element:  # If only one atom is present,
                    count += 1  # add that one atom

        return count

    def alkenes_namer(self):
        lowest = 1
        # print(self.processing)
        for index, atom in enumerate(self.processing):
            self.processing[index] = atom.split('-')  # Splits the compound completely (only single bonds for now)
        self.processing = [j for i in self.processing for j in i]  # Unpacks the list inside list

        lowest = self.lowest_position('CH2')

        return f"{lowest}-ene"

    def alkynes_namer(self):  # Only works if single triple bond is present
        lowest = 1
        for index, atom in enumerate(self.processing):
            self.processing[index] = atom.split('-')  # Splits the compound completely (only single bonds for now)
        self.processing = [j for i in self.processing for j in i]  # Unpacks the list inside list
        # print(self.processing)

        lowest = self.lowest_position('C')  # If triple bond in between compound
        lowest = self.lowest_position('CH')  # If triple bond at ends or ethyne

        return f"{lowest}-yne"

    def lowest_position(self, element):
        lowest = 1
        try:
            front_search = self.processing.index(element) + 1  # Searches for element from the front
            back_search = list(reversed(self.processing)).index(element) + 1  # Searches for element from the back
        except ValueError:
            pass
        else:
            if back_search < front_search:
                lowest = back_search
            else:
                lowest = front_search

        return lowest

    def show_structure(self):  # If user wants to see structure
        symbol = '\u2261'  # The triple bond symbol ≡
        return f"The compound you entered is: {self.structure.replace('~', symbol)}"


class ValencyError(Exception):
    pass


prefixes = {1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept", 8: "oct", 9: "non", 10: "dec",
            11: "undec", 12: "dodec", 13: "tridec", 14: "tetradec", 15: "pentadec", 16: "hexadec", 17: "heptadec",
            18: "octadec", 19: "nonadec", 20: "icos"}


# compound1 = Namer('CH3-CH=C=CH2')
# compound2 = Namer('CH~CH')
compound3 = Namer('CH3-C~C-CH=CH2')

# print(compound1.analyser())
# print(compound2.analyser())
print(compound3.analyser())
