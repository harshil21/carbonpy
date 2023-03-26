# Class to handle addition of carbons, bonds, etc in carboncanvas.
from gi.repository import Gtk

from interface import Interface
from builder import builder
from carbonpy.carbonpy.base.GraphElement import GraphElement


class Playground:
    graph = {}
    total_carbons = 1

    fixed_canvas = builder.get_object("fixedcanvas")

    carbon_buttons: list = fixed_canvas.get_children()
    this_node, next_node = None, None

    def on_carbon_clicked(self, button):
        # bonds: ‒, =, ≡
        self.this_node = int(button.get_name())

        x, y = self.fixed_canvas.child_get(button, "x", "y")
        print(f"{x=},{y=}")

        molecule = GraphElement(value=self.this_node, comp=button.get_label(), x=x, y=y)

        if not self.graph:
            self.graph[molecule] = []

        self.do_physics()

        # space_available, to_place_x, to_place_y = self.get_adjacent_atoms(button, (x, y), self.fixed_canvas)
        # print(space_available, to_place_x, to_place_y)
        #
        # if not space_available:
        #     return

        self.total_carbons += 1

        self.next_node = self.total_carbons
        connections = self.graph[self.this_node]

        if not connections:
            carbon_label = "CH3"
            button.set_label("CH3")
        elif len(connections) == 1:
            carbon_label = "CH2"
            button.set_label(carbon_label)
        elif len(connections) == 2:
            carbon_label = "CH"
            button.set_label(carbon_label)
        elif len(connections) == 3:
            carbon_label = "C"
            button.set_label(carbon_label)
        else:
            return

        bond_button = self.make_bond_button(None, '‒')
        carbon_button = self.make_carbon_button(carbon_label)

        self.set_properties(bond_button, carbon_button)

        # print(self.graph)
        self.fixed_canvas.put(bond_button, x + 30, y)
        self.fixed_canvas.put(carbon_button, to_place_x, to_place_y)

        # assert len(self.carbon_buttons) == self.total_carbons

        self.carbon_buttons[-1].set_label('CH3')  # Terminal carbon should always be CH3
        print()

    def make_bond_button(self, widget, bond_type: str):
        bond_button = Gtk.Button(label=bond_type, name="single", relief=Gtk.ReliefStyle.NONE)

        bond_button.connect("enter-notify-event", Interface.on_enter_notify_event)
        bond_button.connect("leave-notify-event", Interface.on_leave_notify_event)

        Gtk.StyleContext.add_class(bond_button.get_style_context(), "bond")

        return bond_button

    def make_carbon_button(self, actual_rep: str):
        carbon_button = Gtk.Button(label=actual_rep, name=self.next_node, relief=Gtk.ReliefStyle.NONE)
        carbon_button.connect("clicked", self.on_carbon_clicked)
        carbon_button.connect("enter-notify-event", Interface.on_enter_notify_event)
        carbon_button.connect("leave-notify-event", Interface.on_leave_notify_event)

        self.carbon_buttons.append(carbon_button)

        self.add_edge()
        return carbon_button

    def add_edge(self):
        self.graph.setdefault(self.this_node, [])
        self.graph.setdefault(self.next_node, [])

        self.graph[self.this_node].append(self.next_node)
        self.graph[self.next_node].append(self.this_node)

    @staticmethod
    def set_properties(*widgets):
        for widget in widgets:
            widget.set_can_focus(False)
            widget.show()

    # def get_adjacent_atoms(self, button: Gtk.Button, initial_pos: tuple, canvas: Gtk.Container):
    #     if button.get_label() == "C":  # Can't place any more atoms when octet is satisfied
    #         return False, None, None
    #
    #     # assert len(initial_pos) == 2
    #
    #     current_x, current_y = initial_pos
    #
    #     adj_positions = tuple(tuple(canvas.child_get(self.carbon_buttons[adj - 1], "x", "y"))
    #                           for adj in self.graph[self.this_node])  # Obtain coords of each adj atom
    #
    #     print(adj_positions)
    #
    #     if all(adj_x != current_x + 45 for adj_x, adj_y in adj_positions):
    #         return True, current_x + 45, current_y
    #     elif all(adj_x != current_x - 45 for adj_x, adj_y in adj_positions):
    #         return True, current_x - 45, current_y
    #     elif all(adj_y != current_y + 23 for adj_x, adj_y in adj_positions):
    #         return True, current_x, current_y + 23
    #     elif all(adj_y != current_y - 23 for adj_x, adj_y in adj_positions):
    #         return True, current_x, current_y - 23
    #
    #     return True, 323, 142

    # def do_physics(self):
    #     force_on_node =