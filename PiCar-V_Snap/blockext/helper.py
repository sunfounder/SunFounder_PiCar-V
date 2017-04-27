"""Code to interface with Scratch/Snap! as a "helper app".

Uses blockext.server as an HTTP nanoframework.
"""

#from __future__ import (absolute_import, division,
#                        print_function, unicode_literals)
#from future.builtins import *

import itertools
import re
import struct

from .blocks import Block
from .server import Server, Response, NotFound, Download, Redirect, quote
from .generate import Program



class HelperApp(object):
    def __init__(self, helper_cls, blocks_by_selector, descriptor, debug=False):
        self.blocks_by_selector = blocks_by_selector
        self.helper_cls = helper_cls

        self.debug = debug
        self.descriptor = descriptor

        self.requests = set()
        self.helper_cls = helper_cls
        self.helper = helper_cls()

    def get_response(self, selector=None, *args):
        if not self.ensure_connected():
            return Response("")

        if not selector:
            return self.index()

        func_name = "handle_" + selector
        func = getattr(self, func_name, None)
        if func:
            return func(*args)
        else:
            return self.handle(selector, *args)

    def ensure_connected(self):
        if hasattr(self.helper, "_is_connected"):
            return self.helper._is_connected()
        else:
            return True

    def handle(self, selector, *args):
        try:
            block = self.blocks_by_selector[selector]
        except KeyError:
            return NotFound()

        content = self.run_block(block, args)
        return Response(content.encode("utf-8"))

    def run_block(self, block, args):
        args = list(args)
        if block.is_blocking:
            request_id = args.pop(0)
            # Snap! doesn't use _busy, so it sends "-" as the request_id
            if request_id != "-":
                self.requests.add(request_id)

        assert len(args) == len(block.inputs)

        args = [decode_arg(a, t) for (a, t)
                in zip(args, block.inputs)]

        func = getattr(self.helper, block.selector)
        result = func(*args)
        content = encode_result(result, block.shape)

        if block.is_blocking:
            if request_id in self.requests:
                self.requests.remove(request_id)

        return content

    def handle_poll(self):
        reporter_values = {}
        for selector, block in self.blocks_by_selector.items():
            if block.is_blocking: continue
            if block.shape not in ("reporter", "predicate"):
                continue
            func = getattr(self.helper, selector)
            menu_names = [input_.menu for input_ in block.inputs]
            if all(menu_names): # they're all menu inputs
                insert_options = map(self.descriptor.menus.get, menu_names)
                for args in itertools.product(*insert_options):
                    path = "/".join([selector] + list(args))
                    reporter_values[path] = self.run_block(block, args)

        if self.requests:
            reporter_values["_busy"] = " ".join(map(str, self.requests))

        if hasattr(self.helper, "_problem"):
            problem = self.helper._problem()
            if problem:
                reporter_values["_problem"] = str(problem)

        lines = []
        for name, value in reporter_values.items():
            lines.append(name + " " + value)

        content = "\n".join(lines).encode("utf-8")
        return Response(content)

    def handle_reset_all(self):
        # TODO what if the helper isn't connected?
        if hasattr(self.helper, "_on_reset"):
            self.helper._on_reset()
            self.requests = set()
            # TODO clear self.requests, kill threads (?)
        return Response("")


    # For debugging extensions #

    def index(self):
        if not self.debug:
            return NotFound()
        """
        <!doctype html>
        <p><a href="/_generate_blocks/scratch">Download Scratch 2 extension file</a>
        <p><a href="/_generate_blocks/snap">Download Snap! blocks</a>
        """
        return Response("""\
        <!doctype html>
        <p><a href="/_generate_blocks/snap">Download Snap! blocks</a>
        <p><a href="http://snap.berkeley.edu/run">Run Snap!</a>
        """, content_type="text/html")

    def handle__generate_blocks(self, program_name, language_code="en", filename=None):
        if not self.debug:
            return NotFound()

        program = Program.by_short_name[program_name]
        language = self.descriptor.translations[language_code]

        if not filename:
            filename = program.get_filename(self.descriptor, language_code)
            new_path = "/".join((
                "/_generate_blocks",
                quote(program_name),
                quote(language_code),
                quote(filename))
            )
            return Redirect(new_path)

        return Download(program.generate_file(self.descriptor, language),
                        program.content_type)



#- Translate between block language strings and Pythonic values. -#

def decode_arg(arg, input_):
    if input_.shape == "number":
        try:
            arg = int(arg)
        except ValueError:
            try:
                arg = float(arg)
            except ValueError:
                arg = 0
    elif input_.shape == "boolean":
        arg = True if arg == "true" else False if arg == "false" else None
    elif input_.shape == "color":
        try:
            v = int(arg)
            a, r, g, b = struct.unpack('BBBB', struct.pack('>i', v))
            arg = r, g, b
        except (ValueError, struct.error):
            color_pat = re.compile(r'^rgba\(([0-9]+),([0-9]+),([0-9]+),1\)$')
            m = color_pat.match(arg)
            if m:
                arg = tuple(map(int, m.groups()))
            else:
                arg = (0, 0, 0)
    return arg


def encode_result(result, shape="reporter"):
    if shape == "command":
        result = None
    elif shape == "predicate":
        result = bool(result)
    elif shape == "reporter":
        pass

    result = ("true" if result is True else
              "false" if result is False else
              "" if result == None else str(result))
    return result



class Extension(object):
    def __init__(self, helper_cls, descriptor, deprecated_blocks=None):
        self.helper_cls = helper_cls
        """The class implementing the block methods.

        Block selectors must correspond to method names on this class.

        """

        self.descriptor = descriptor
        """Information about the extension."""

        deprecated_blocks = deprecated_blocks or []
        self._blocks_by_selector = {}
        for block in descriptor.blocks + deprecated_blocks:
            if not isinstance(block, Block):
                raise ValueError("not a block: " + repr(block))
            if block.selector in self._blocks_by_selector:
                raise ValueError("block selectors must be unique")
            if not hasattr(helper_cls, block.selector):
                raise ValueError(
                    "helper class needs method for block: " + repr(block.selector)
                )
            self._blocks_by_selector[block.selector] = block

    def run_forever(self, debug=False):
        app = HelperApp(self.helper_cls, self._blocks_by_selector,
                        self.descriptor, debug)
        server = Server(app, self.descriptor.host, self.descriptor.port)
        print("Listening on {self.descriptor.host}:{self.descriptor.port}".format(**vars()))
        server.serve_forever()

