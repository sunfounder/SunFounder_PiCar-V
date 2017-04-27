#from __future__ import (absolute_import, division,
#                        print_function, unicode_literals)
#from future.builtins import *

import os
import re



class Block(object):
    _highest_id = 0

    def __init__(self, selector, shape, parts_or_spec, is_blocking=False,
            help_text="", defaults=[]):
        self.shape = str(shape)
        """A string determining the kind of values the block reports.

            * ``"command"`` -- Doesn't report a value. (puzzle-piece)
            * ``"reporter"`` -- Reports a number. (round ends)
            * ``"predicate"`` -- Reports a boolean. (pointy ends)

        """

        if selector.startswith("_"):
            raise ValueError("names starting with an underscore are reserved")
        self.selector = str(selector)
        """Used by the block language to identify the block."""

        if isinstance(parts_or_spec, list):
            self.parts = [p if isinstance(p, Input) else str(p) for p in parts]
        else:
            self.parts = parse_spec(parts_or_spec)

        for input_, value in zip(self.inputs, defaults):
            input_.default = value

        self.is_blocking = bool(is_blocking)
        """True if the block language should wait for the block to return."""

        self.help_text = str(help_text)
        """Text explaining the block to a Scratch user."""

        self.translations = {}

    @property
    def inputs(self):
        return [p for p in self.parts if isinstance(p, Input)]

    @property
    def defaults(self):
        return [x.default for x in self.inputs]

    @property
    def spec(self):
        return generate_spec(self.parts)

    def __repr__(self):
        return "<Block({spec})>".format(spec=repr(generate_spec(self.parts)))

    def __call__(self, func):
        func._block = self
        Block._highest_id += 1
        func._block_id = Block._highest_id
        return func


class Input(object):
    """The specification for an argument to a :class:`Block`."""

    DEFAULTS = {
        "number": 0,
        "number-menu": 0,
        "readonly-menu": None, # Set in _set_menu_defaults()
        "string": "",
        "boolean": False,
    }

    def __init__(self, shape, menu=None):
        self.shape = str(shape)
        """A string identifying the kind of values the input accepts.

            * ``'number'`` -- number input (round ends)
            * ``'string'`` -- string input (square ends)
            * ``'boolean'`` -- boolean input (pointy ends)
            * ``'readonly-menu'`` -- menu input
            * ``'number-menu'`` -- editable number input with menu
            * ``'color'`` -- color input with picker

        """

        if 'menu' in shape:
            assert menu, "Menu is required"
        else:
            assert not menu, "Menu not allowed"
        self.menu = str(menu) if menu else None
        """For menu inputs: the options the drop-down menu contains.

        The options come from an earlier :attr:`Extension.menu` call::

            ext.add_menu("menuName", ["one", "two", "three", ...])

        """

        self.default = Input.DEFAULTS.get(self.shape)

    def __repr__(self):
        r = "Input({}".format(repr(self.menu))
        if self.menu:
            r += ", menu={}".format(repr(self.menu))
        return r + ")"

    def __eq__(self, other):
        return (isinstance(other, Input) and self.shape == other.shape
                                         and self.menu == other.menu)

    def _set_menu_defaults(self, menus):
        if self.default is None:
            self.default = ""
            if self.shape == "readonly-menu":
                try:
                    options = menus[self.menu]
                except KeyError:
                    raise ValueError(
                        "menu not found: {}".format(repr(self.menu))
                    )
                self.default = options[0]


INPUT_SPECS = {
    "n": "number",
    "s": "string",
    "b": "boolean",
    "m": "readonly-menu",
    "d": "number-menu",
    "c": "color",
}


def parse_spec(spec):
    def generate_parts(spec):
        for part in re.split(r"(%[^ ](?:\.[A-z]+)?)", spec):
            match = re.match(r"^%([^ ])(?:\.([A-z]+))?$", part)
            if match:
                shape = INPUT_SPECS.get(match.group(1))
                if not shape:
                    raise ValueError("Unknown input shape %s" % part)
                part = Input(shape, match.group(2))
            else:
                part = str(part)
            yield part

    spec = str(spec)
    parts = list(generate_parts(spec))
    inputs = [p for p in parts if isinstance(p, Input)]

    return parts


def generate_spec(block_parts):
    """A string identifying the labels and inputs to the block.

    Words starting with "%" produce input slots. Supported input types are:

        * ``%n`` -- number input (round ends)
        * ``%s`` -- string input (square ends)
        * ``%b`` -- boolean input (pointy ends)
        * ``%m.menuName`` -- menu input
        * ``%d.menuName`` -- editable number input with menu

    The last two input slots produce a drop-down menu. The options come
    from an earlier :attr:`Extension.menu` call::

        ext.add_menu("menuName", ["one", "two", "three", ...])

    """

    def stringify_part(part):
        if isinstance(part, Input):
            for s, shape in INPUT_SPECS.items():
                if shape == part.shape:
                    break
            else:
                assert False
            r = "%" + s
            if part.menu:
                r += "." + part.menu
            return r
        return part

    spec = "".join(map(stringify_part, block_parts))
    return spec


def load_po_files(this_file, relative_folder=None, **language_file_paths):
    translations = {}
    base = ""
    if this_file is not None:
        base = os.path.abspath(os.path.dirname(this_file))
    if relative_folder:
        base = os.path.join(base, relative_folder)
    for lang, path in language_file_paths.items():
        path = os.path.join(base, path)
        with open(path) as f:
            translations[lang] = Language.from_po_file(f)
    return translations


class Language(object):
    def __init__(self, strings):
        self._strings = strings

    def __getitem__(self, key):
        """Return translation if possible, else untranslated string."""
        return self._strings.get(key, key)

    get = __getitem__

    @classmethod
    def from_po_file(cls, path):
        return
        raise NotImplementedError()

    def get_menus(self, menus):
        translated_menus = {}
        for key, options in menus.items():
            translated_menus[key] = list(map(self.get, options))
        return translated_menus


class Descriptor(object):
    def __init__(self, name, host, port, category, blocks, menus=None, translations=None):
        self.name = str(name)
        """Human-readable name of the hardware."""

        self.host = str(host)
        """Host the extension runs on."""

        self.port = int(port)
        """Port the extension runs on."""

        self.category = str(category)
        """Category the extension stays in."""

        self.blocks = list(blocks)
        """The list of blocks displayed in the interface."""

        menus = menus or {}
        menus = dict((str(k), list(map(str, v))) for k, v in menus.items())
        self.menus = menus
        """Options for custom drop-down menus."""

        translations = translations or {}
        if "en" in translations:
            raise ValueError("english must be default")
        translations["en"] = Language({})
        self.translations = translations
        """Translations for block specs and menu options."""

        # Set default menu options
        for block in self.blocks:
            for input_ in block.inputs:
                input_._set_menu_defaults(self.menus)

    def __repr__(self):
        return "<Descriptor(%r, %i)>" % (self.name, self.port)

