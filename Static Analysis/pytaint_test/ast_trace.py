import ast
import sys

class GlobalUseCollector(ast.NodeVisitor):
    def __init__(self, name):
        self.name = name
        # track context name and set of names marked as `global`
        self.context = [('global', ())]

    def visit_FunctionDef(self, node):
        self.context.append(('function', set()))
        self.generic_visit(node)
        self.context.pop()

    def visit_ClassDef(self, node):
        self.context.append(('class', ()))
        self.generic_visit(node)
        self.context.pop()

    def visit_Lambda(self, node):
        # lambdas are just functions, albeit with no statements
        self.context.append(('function', ()))
        self.generic_visit(node)
        self.context.pop()

    def visit_Global(self, node):
        assert self.context[-1][0] == 'function'
        self.context[-1][1].update(node.names)

    def visit_Name(self, node):
        ctx, g = self.context[-1]
        if node.id == self.name :
            print('{} used at line {}'.format(node.id, node.lineno))

indiv_file = sys.argv[1]
with open(indiv_file, 'r') as myfile:
    data = myfile.read()
myfile.close()

# print "Got here!"
readin = ast.parse(data)
# print data
for node in ast.walk(readin):
    if isinstance(node, ast.FunctionDef):
        print(node.name)

command_line = sys.argv[2]

a = GlobalUseCollector(command_line).visit(readin)