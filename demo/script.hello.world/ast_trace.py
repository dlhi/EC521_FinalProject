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
        self.context = Context()
        self.functions = {}

        for n in names:
            self.functions[n] = []
        print(self.functions)

    # def visit_Expr(self, node):
    #     self.context.append(('expr', node.value, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_Assign(self, node):
    #     self.generic_visit(node)


    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.context.function = node.func.id
        elif isinstance(node.func, ast.Attribute):
            self.context.function = node.func.attr
        self.generic_visit(node)
        self.context.function = None

    # def visit_FunctionDef(self, node):
    #     self.context.append(('function_def', node.name, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_ClassDef(self, node):
    #     self.context.append(('class', node.id, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_Lambda(self, node):
    #     self.context.append(('function', node.id, list()))
    #     self.generic_visit(node)
    #     self.context.pop()

    # def visit_Attribute(self, node):
    #     self.generic_visit(node)

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
        if node.id in self.names:
            self.context.arguments = node.id
            self.functions[node.id].append(self.context.function)

def read_file(filename):
    # Read in file to data
    with open(filename, 'r') as myfile:
        data = myfile.read()
    myfile.close()
    # Parse data into AST format
    readin = ast.parse(data)
    return readin

def functionFinder(parsed_ast):
    dictionary = {}
    function_list = []

    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.ClassDef):
            for entries in node.body:
                if isinstance(entries, ast.FunctionDef):
                    # print(entries.name)
                    if node.name not in dictionary:
                        dictionary[node.name] = []
                    dictionary[node.name].append((entries.name, entries.lineno))

        if isinstance(node, ast.FunctionDef):
            print(node.name)
            function_list.append(node.name)

    return dictionary, function_list

def list_func_calls(fn):
    funcs = []
    bytecode = dis.Bytecode(fn)
    instrs = list(reversed([instr for instr in bytecode]))
    for (ix, instr) in enumerate(instrs):
        if instr.opname=="CALL_FUNCTION":
            load_func_instr = instrs[ix + instr.arg + 1]
            funcs.append(load_func_instr.argval)

    return ["%s" % (funcname) for (ix, funcname) in enumerate(reversed(funcs), 1)]

def parseAST(filename, variable_key):
    locals()[filename[:-3]] = importlib.import_module(filename[:-3])
    object_ast = GlobalUseCollector([variable_key])

    parsed_ast = read_file(filename)
    # astpretty.pprint(parsed_ast)
    object_ast.visit(parsed_ast)
    print(object_ast.functions)
    return object_ast.functions

    # variable_occurances = object_ast.variables
    # dictionar, func_list = functionFinder(parsed_ast)

    # for internalFunc in func_list:
    #     directory = filename[:-2] + str(internalFunc)
    #     try:
    #         array_to_parse = list_func_calls(eval(directory))
    #         for intFunc in array_to_parse:
    #             if intFunc not in func_list:
    #                 func_list.append(intFunc)
    #     except:
    #         pass
    #         # print(internalFunc, " does not have an internal function!")

    # return dictionar, variable_occurances, func_list

def main():
    parseAST(sys.argv[1], 'name')
    # print(d)
    # print(v)
    # print(f)
    
if __name__ == '__main__':
    main()
