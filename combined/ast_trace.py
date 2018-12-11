import astpretty
import ast
import sys
import dis
import importlib

from optparse import OptionParser
import inspect

class Context(object):
    def __init__(self):
        self.function = None
        self.arguments = None

    def __str__(self):
        return "{} ( {} )".format(self.function, self.arguments)

    def __repr__(self):
        return "{} ( {} )".format(self.function, self.arguments)


class GlobalUseCollector(ast.NodeVisitor):
    def __init__(self, names):
        self.names = names
        # track context name and set of names marked as `global`
        self.context = []
        self.functions = {}

        for n in names:
            self.functions[n] = []

        self.assign = False
        self.name = None

    # def visit_Expr(self, node):
    #     self.context.append(('expr', node.value, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    def get_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return None

    def visit_Assign(self, node):
        for n in node.targets:
            if n.id in self.names:
                # self.context.append(self.get_name(n))
                self.assign = True
                self.name = n.id
                self.generic_visit(node)
                self.assign = False
                # self.context.pop()
            else:
                self.generic_visit(node)


    def visit_Call(self, node):
        self.context.append(self.get_name(node.func))
        self.generic_visit(node)
        if self.assign:
            # print(self.context)
            self.functions[self.name].append(self.context[-1])
        self.context.pop()

        # self.context.function = None

    def visit_FunctionDef(self, node):
        self.context.append(node.name)
        self.generic_visit(node)
        self.context.pop()

    # def visit_ClassDef(self, node):
    #     self.context.append(('class', node.id, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_Lambda(self, node):
    #     self.context.append(('function', node.id, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    def visit_Attribute(self, node):
        self.context.append(node.attr)
        self.generic_visit(node)
        self.context.pop()

    # def visit_Try(self, node):
    #     self.context.append(('try', 'try', list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_TryExcept(self, node):
    #     self.context.append(('try_except', 'try_except', list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_TryFinally(self, node):
    #     self.context.append(('try_finally', 'try_finally', list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_ExceptHandler(self, node):
    #     self.context.append(('except', 'except', list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_UnaryOp(self, node):
    #     self.context.append(('unary_op', node.op, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_BinOp(self, node):
    #     self.context.append(('bin_op', node.op, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_For(self, node):
    #     self.context.append(('for', node.target.id, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_While(self, node):
    #     self.context.append(('while', 'comp', list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_Str(self, node):
    #     self.context[-1][2].append(node.s)

    # def visit_Num(self, node):
    #     self.context[-1][2].append(node.n)

    # def visit_Bytes(self, node):
    #     self.context[-1][2].append(node.s)

    # def visit_List(self, node):
    #     self.context[-1][2].append(node.elts)

    # def visit_Tuple(self, node):
    #     self.context[-1][2].append(node.elts)

    # def visit_Set(self, node):
    #     self.context[-1][2].append(node.elts)

    # def visit_Dict(self, node):
    #     self.context[-1][2].append((node.keys, node.values))

    # def visit_NameConstant(self, node):
    #     self.context[-1][2].append(node.value)

    # def visit_Global(self, node):
    #     assert self.context[-1][0] == 'function_def'
    #     self.context[-1][2].append(node.names)

    # def visit_Nonlocal(self, node):
    #     print(self.names)

    def visit_Name(self, node):
        # self.context[-1][2].append(node.id)
        if node.id in self.names and not self.assign:
            # print(self.context)
            self.functions[node.id].append(self.context[-1])

def read_file(filename):
    # Read in file to data
    with open(filename, 'r') as myfile:
        data = myfile.read()
    myfile.close()
    # Parse data into AST format
    readin = ast.parse(data)
    return readin

def parseAST(filename, variable_key):
    locals()[filename[:-3]] = importlib.import_module(filename[:-3])
    object_ast = GlobalUseCollector([variable_key])

    parsed_ast = read_file(filename)
    # astpretty.pprint(parsed_ast)
    object_ast.visit(parsed_ast)
    # print(object_ast.functions)

    # stack = []
    # for node in ast.walk(parsed_ast):
    #     if isinstance(node, ast.Assign):
    functions = []
    for k, v in object_ast.functions.items():
        for f in v:
            functions.append(f)
    print(functions)
    return functions
def main():
    parseAST(sys.argv[1], sys.argv[2])
    # print(d)
    # print(v)
    # print(f)
    
if __name__ == '__main__':
    main()
