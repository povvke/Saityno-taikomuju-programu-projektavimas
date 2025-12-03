from pylint.checkers import BaseChecker
import astroid


class NoPrintChecker(BaseChecker):
    name = "no-print-checker"
    priority = -1
    msgs = {
        "W9001": (
            "Naudojama print() funkcija. Naudokite logger.",  # Message
            "no-print-statement",  # Symbol
            "Print funkcijos neturi likti production kode.",  # Description
        ),
    }

    def visit_call(self, node):
        """
        Tikrina kiekvieną funkcijos kvietimą.
        """
        if isinstance(node.func, astroid.Name) and node.func.name == "print":
            self.add_message("no-print-statement", node=node)


def register(linter):
    linter.register_checker(NoPrintChecker(linter))
