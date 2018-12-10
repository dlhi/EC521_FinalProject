import types
import inspect
import find_functions

d = find_functions.find()
funcs = []
for k, v in d.items():
    for f in v:
        funcs.append(f)
# print(funcs)
def decorator(f):
    """Accept arbitrary arguments, and use them to decorate functions.
    """
    def called(*args, **kwargs):
        print('>>> ', f)
        print('args: %s\nkwargs: %s' %(args, kwargs))
        print('----------------')
        result = f(*args, **kwargs)
        print('----------------')
        print('returned: %s of type %s' %(result, type(result)))
        print('<<< ', f)
        print('\n')
        return result
    # print("calling")
    return called

def decorate(globals=None, decor=None):
    if decor is None:
        decor = []
    for name, obj in list(globals.items()):
        # print(name, obj)
        if (isinstance(obj, types.FunctionType)
            or isinstance(obj, types.BuiltinFunctionType)
            or isinstance(obj, types.MethodType)
            or isinstance(obj, types.BuiltinMethodType)) and name in funcs:
                print(globals['__name__'], name, obj)
                globals[name] = decorator(obj)
        # elif inspect.ismethoddescriptor(obj) and name in funcs:
        #     globals[name].__init__ = decorator(globals[name].__init__)
        elif (isinstance(obj, types.ModuleType) or inspect.isclass(obj)) and name not in decor:
            # print('\n\n>>>>>>>', name)
            decor.append(name)
            decorate(obj.__dict__, decor)