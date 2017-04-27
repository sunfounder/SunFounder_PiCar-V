#from __future__ import (absolute_import, division,
#                        print_function, unicode_literals)
#from future.builtins import *

"""Library for writing Scratch 2.0 and Snap! extensions.

Blockext provides two things:

- automatic generation of extension files for both Scratch and Snap! from
  blocks defined in Python code.
- an method for extensions to communicate with Scratch and Snap!.

"""

__version__ = '0.2.0a'

from collections import OrderedDict
from functools import wraps
import re

from .blocks import Block, Input, Descriptor, load_po_files
from .generate import generate_file
from .helper import Extension


_doc_pat = re.compile(r'[ \t]*\n[ \t]*')

def _shape(shape):
    def make_block(spec, defaults=[], help_text="", **kwargs):
        def wrapper(func, help_text=help_text):
            # Magic: name -> selector
            selector = func.__name__

            # Magic: docstring -> help text
            help_text = help_text or func.__doc__ or ""
            help_text = _doc_pat.sub("\n", help_text)

            block = Block(selector, shape, spec, defaults=defaults,
                          help_text=help_text, **kwargs)
            block(func) # attaches itself to func._block
            return func
        return wrapper
    return make_block

command = _shape("command")
reporter = _shape("reporter")
predicate = _shape("predicate")

del _shape


def get_decorated_blocks_from_class(cls, selectors=None):
    if selectors:
        cls_vars = vars(cls)
        values = map(cls_vars.get, selectors)
    else:
        values = vars(cls).values()

    functions = []
    for value in values:
        if callable(value) and hasattr(value, '_block'):
            functions.append(value)
    functions.sort(key=lambda func: func._block_id)
    return [f._block for f in functions]

