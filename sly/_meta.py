from collections import OrderedDict

class NoDupeDict(OrderedDict):
    def __setitem__(self, key, value):
        if key in self and not isinstance(value, property):
            raise AttributeError('Name %s redefined' % (key))
        super().__setitem__(key, value)

class RuleMeta(type):
    @staticmethod
    def __prepare__(meta, *args, **kwargs):
        d = NoDupeDict()
        def _(rule):
            def decorate(func):
                func.rule = rule
                return func
            return decorate
        d['_'] = _
        return d

    def __new__(meta, clsname, bases, attributes):
        del attributes['_']
        cls = super().__new__(meta, clsname, bases, attributes)
        cls._build(list(attributes.items()))
        return cls
