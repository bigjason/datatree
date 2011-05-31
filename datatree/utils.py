from importlib import import_module

def get_class(kls):
    """Return a class by its full name."""
    parts = kls.split('.')
    module = '.'.join(parts[:-1])
    m = import_module(module)
    return getattr(m, parts[-1])

def get_module(module_path):
    """Return a module by its full name."""
    return import_module(module_path)
