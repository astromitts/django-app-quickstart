import json
from django import template

register = template.Library()


@register.filter(name='pdb')
def pdb(item, item2=None):
    import pdb  # noqa
    pdb.set_trace()  # noqa


@register.filter(name='get')
def get(sourcedict, key):
    return sourcedict.get(key)


@register.filter(name='get_as_str')
def get_as_str(sourcedict, key):
    return sourcedict.get(str(key))


@register.filter(name='jsondump')
def jsondump(source_object):
    return json.dumps(source_object)
