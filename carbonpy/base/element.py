class Element(object):  # Node
    __slots__ = ('value', 'comp', 'front_bond', 'back_bond', 'top_bond', 'bottom_bond')

    def __init__(self, value: int or str, comp: str) -> None:
        # Required-
        self.value: int or str = value
        self.comp: str = comp

        # Optional-
        self.front_bond: str = ''
        self.back_bond: str = ''
        self.top_bond: str = ''
        self.bottom_bond: str = ''

    def __str__(self) -> str:
        return self.comp

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r}, {self.comp!r})"

    def __hash__(self) -> hash:
        return hash(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value == other
        return self.value == other.value if isinstance(other, Element) else NotImplemented

    def hydrogens(self) -> int:
        last = self.comp[-1]
        if last.isdigit():
            return int(last)
        return 1 if last == 'H' else 0
