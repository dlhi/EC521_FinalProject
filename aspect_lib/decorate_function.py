import types

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

def decorate(globals=None):
    for name, obj in list(globals.items()):
        if isinstance(obj, types.FunctionType):
            globals[name] = decorator(obj)


