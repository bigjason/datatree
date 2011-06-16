
try:
    from importlib import import_module
except ImportError:
    import_module = None
    
if import_module:
    def get_class(kls):
        """Return a class by its full name."""
        parts = kls.split('.')
        module = '.'.join(parts[:-1])
        m = import_module(module)
        return getattr(m, parts[-1])
else:    
    def get_class(kls):
        """
         Return a class by its full name.
         """
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m