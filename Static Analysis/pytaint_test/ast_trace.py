import ast
import sys
import dis
import importlib

from optparse import OptionParser
import inspect

class GlobalUseCollector(ast.NodeVisitor):
    def __init__(self, name):
        self.name = name
        # track context name and set of names marked as `global`
        self.context = [('global', ())]
        self.variables = []

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
            # print('{} used at line {}'.format(node.id, node.lineno))
            # print node.lineno
            self.variables.append(node.lineno)

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
            # print(node.name)
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
    object_ast = GlobalUseCollector(variable_key)

    parsed_ast = read_file(filename)
    object_ast.visit(parsed_ast)

    variable_occurances = object_ast.variables
    dictionar, func_list = functionFinder(parsed_ast)

    for internalFunc in func_list:
        directory = filename[:-2] + str(internalFunc)
        try:
            array_to_parse = list_func_calls(eval(directory))
            for intFunc in array_to_parse:
                if intFunc not in func_list:
                    func_list.append(intFunc)
        except:
            pass
            # print(internalFunc, " does not have an internal function!")

    return dictionar, variable_occurances, func_list

def main():
    d, v, f = parseAST("system_vuln.py", 'f')
    print(d)
    print(v)
    print(f)
    
if __name__ == '__main__':
    main()