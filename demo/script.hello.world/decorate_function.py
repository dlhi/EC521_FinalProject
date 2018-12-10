import types
import inspect
import find_functions
import os

d = find_functions.find()
funcs = []
for k, v in d.items():
    for f in v:
        funcs.append(f)
with open('/Users/chaseclarke/Desktop/decorate.txt', 'w+') as file:
    file.write(str(funcs))
funcs = ['system', 'exec', 'create_table', 'insert_into_table', 'callExec', 'SQLVuln', 'read_db', 'Sockets']

file = open('/Users/chaseclarke/Desktop/temp.txt', 'w+')
file.close()
# file.write(funcs)
def decorator(f):
    """Accept arbitrary arguments, and use them to decorate functions.
    """
    def called(*args, **kwargs):
        with open('/Users/chaseclarke/Desktop/temp.txt', 'a') as file:
            file.write('>>> ' + str(f) + '\n')
            file.write('args: %s\nkwargs: %s\n' %(args, kwargs))
            file.write('----------------\n')
            result = f(*args, **kwargs)
            file.write('----------------\n')
            file.write('returned: %s of type %s\n' %(result, type(result)))
            file.write('<<< ' + str(f) + '\n')
            file.write('\n')
        return result
    # file.write("calling")
    return called

def decorate(globals=None, decor=None):
    if decor is None:
        decor = []
    for name, obj in list(globals.items()):
        # file.write(name, obj)
        if (isinstance(obj, types.FunctionType)
            or isinstance(obj, types.BuiltinFunctionType)
            or isinstance(obj, types.MethodType)
            or isinstance(obj, types.BuiltinMethodType)) and name in funcs:
#                file.write(globals['__name__'], name, obj)
                globals[name] = decorator(obj)
        # elif inspect.ismethoddescriptor(obj) and name in funcs:
        #     globals[name].__init__ = decorator(globals[name].__init__)
        elif (isinstance(obj, types.ModuleType) or inspect.isclass(obj)) and name not in decor:
            # file.write('\n\n>>>>>>>', name)
            decor.append(name)
            decorate(obj.__dict__, decor)
