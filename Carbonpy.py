# An organic chemistry module for Grade 12(mostly)-
# Can name compounds based on their structure, convert the compound from one functional group to another and more...
# - single bond
# = double bond
# ~ triple bond


class Namer(object):  # IUPAC Names for now only

    def __init__(self, structure):
        self.structure = structure
        self.carbon_atoms = 0  # No. of carbon atoms present
        self.bond = ""  # Name of bond
        self.final = ""  # Name of final compound
        self.processing = []  # List for analysing given compound

    def analyser(self):
        compound_name = ""

        if '~' in self.structure:
            self.bond = "yne"
            self.processing = self.structure.split('~')
            bond_type = self.alkynes_namer()
            compound_name += f"-{bond_type}"  # Suffix and position is decided

        if '=' in self.structure:
            self.processing = self.structure.split('=')
            bond_type = self.alkenes_namer()
            self.bond = "ene"
            compound_name += f"-{bond_type}"  # Suffix and position is decided
        else:
            self.bond = "ane"
            # compound_name += self.bond

        symbol = '\u2261'  # The triple bond symbol
        print(f"The compound you entered is: {self.structure.replace('~', symbol)}")
        return f"{prefixes[self.carbon_counter()]}{compound_name}"

    def carbon_counter(self):
        for atom in self.structure:
            if atom in 'Cc':
                self.carbon_atoms += 1
        return self.carbon_atoms

    def alkenes_namer(self):
        lowest = 1
        for index, atom in enumerate(self.processing):
            self.processing[index] = atom.split('-')  # Splits the compound completely (only single bonds for now)
        self.processing = [j for i in self.processing for j in i]  # Unpacks the list inside list
        print(self.processing)

        try:
            lowest = self.lowest_position('CH2')
        except ValueError:
            pass
        return f"{lowest}-ene"

    def alkynes_namer(self):  # Only works if single triple bond is present
        lowest = 1
        for index, atom in enumerate(self.processing):
            self.processing[index] = atom.split('-')  # Splits the compound completely (only single bonds for now)
        self.processing = [j for i in self.processing for j in i]  # Unpacks the list inside list
        print(self.processing)

        try:
            lowest = self.lowest_position('C')  # If triple bond in between compound
            lowest = self.lowest_position('CH')  # If triple bond in ends or ethyne
        except ValueError:
            pass

        return f"{lowest}-yne"

    def lowest_position(self, element):
        lowest = 1
        front_search = self.processing.index(element) + 1  # Searches for element from the front

        self.processing = list(reversed(self.processing))
        back_search = self.processing.index(element) + 1  # Searches for element from the back
        self.processing = list(reversed(self.processing))

        if back_search < front_search:
            lowest = back_search
        else:
            lowest = front_search

        return lowest


prefixes = {1: "meth", 2: "eth", 3: "prop", 4: "but", 5: "pent", 6: "hex", 7: "hept", 8: "oct"}


compound = Namer('CH2=CH-CH=CH2')

print(compound.analyser())
