import ast
from pprint import pprint


def main():
    with open("target_code/myscript2.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"call": []}
        self.sources = source2

    def visit_Call(self, node):
        #for expr in node.func:
        try:
            self.stats["call"].append(node.func.id)
            #self.stats["call"].append("")
            #print(ast.get_source_segment(self.sources.read(),node))
        except:
            pass
        self.generic_visit(node)

    # def visit_Import(self, node):
    #     for alias in node.names:
    #         self.stats["import"].append(alias.name)
    #     self.generic_visit(node)
    #
    # def visit_ImportFrom(self, node):
    #     for alias in node.names:
    #         self.stats["from"].append(alias.name)
    #     self.generic_visit(node)

    def report(self):
        pprint(self.stats["call"])


if __name__ == "__main__":
    source2 = open("target_code/myscript2.py", "r")
    main()
