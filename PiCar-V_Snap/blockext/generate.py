#from __future__ import (absolute_import, division,
#                        print_function, unicode_literals)
#from future.builtins import *

from .blocks import Block, Input
from .languages import language_codes


class Program(object):
    """For exporting blocks to a specfic block language."""

    name = "Program" # "Scratch 2", "Snap"
    """Name of the hardware or extension. Must be filename-friendly."""

    by_short_name = {} # "scratch2": ScratchProgram, "snap": SnapProgram

    file_extension = "xml"

    content_type = "application/octet-stream"

    @classmethod
    def get_filename(cls, descriptor, lang):
        language = language_codes.get(lang) or lang
        fmt = "{cls.name} {descriptor.name} {language}.{cls.file_extension}"
        return fmt.format(**locals())

    @classmethod
    def generate_file(cls, descriptor, language):
        raise NotImplementedError(self)



#-- Scratch 2.0 --#

import json

BLOCK_SHAPES = {
    "command": " ",
    "reporter": "r",
    "predicate": "b",
}

class ScratchProgram(Program):
    name = "Scratch"
    file_extension = "s2e"

    @classmethod
    def generate_file(cls, descriptor, language):
        s2e = {
            "extensionName": descriptor.name,
            "extensionPort": descriptor.port,
            "blockSpecs": [],
            "menus": language.get_menus(descriptor.menus),
        }
        for block in descriptor.blocks:
            shape = BLOCK_SHAPES[block.shape]
            if block.shape == "command" and block.is_blocking:
                shape = "w"
            spec = language.get(block.spec)
            blockspec = [shape, spec, block.selector] + block.defaults
            s2e["blockSpecs"].append(blockspec)
        return json.dumps(s2e, ensure_ascii=False).encode("utf-8")
        # TODO check Scratch will accept utf-8 json

Program.by_short_name["scratch"] = ScratchProgram



#-- Snap! --#

import re
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import commands

INPUT_SELECTORS = {
    "number": "n",
    "string": "s",
    "boolean": "b",
    "readonly-menu": "txt",
    "number-menu": "n",
    "color": "clr",
}

class SnapProgram(Program):
    name = "Snap"
    file_extension = "xml"
    content_type = "application/xml"

    @classmethod
    def generate_file(cls, descriptor, language):
        return generate_snap(descriptor, language)

def get_ip():
    ip = commands.getoutput("hostname -I")
    return ip.strip()

def generate_snap(descriptor, language):
    root = Element("blocks", {
        "app": "Snap! 4.0, http://snap.berkeley.edu",
        "version": "1",
    })

    menus = language.get_menus(descriptor.menus)

    for block in descriptor.blocks:
        defn = SubElement(root, "block-definition", {
            "type": "%s" % block.shape, # Can't use a future.builtins.str
            "category": "%s" % descriptor.category,
        })

        if block.help_text:
            comment = SubElement(defn, "comment", w="360", collapsed="false")
            comment.text = block.help_text

        SubElement(defn, "header")
        SubElement(defn, "code")
        inputs = SubElement(defn, "inputs")

        snap_spec = ""
        for part in block.parts:
            if isinstance(part, Input):
                input_el = SubElement(inputs, "input", {
                    "type": "%{shape}".format(shape=INPUT_SELECTORS[part.shape]),
                    "readonly": "true" if part.shape == "m" else "",
                })
                input_el.text = str(part.default)
                if "menu" in part.shape:
                    options = SubElement(input_el, "options")
                    options.text = "\n".join(menus[part.menu])
                    # TODO menus
                    # XXX ^ why is there a todo comment here?

                index = block.inputs.index(part)
                part = "%'arg-{}'".format(index)
            else:
                assert isinstance(part, str)
                # Snap! doesn't allow %-signs in block text yet.
                part = re.compile(r" *% *").sub(" ", part)
            snap_spec += part

        defn.attrib["s"] = snap_spec

        http_block = Element("block", s="reportURL")
        join_block = SubElement(http_block, "block", s="reportJoinWords")
        list_ = SubElement(join_block, "list")
        host = get_ip()
        url = "{host}:{descriptor.port}/{block.selector}".format(**vars())
        if block.is_blocking:
            url += "/-" # Blank request id
        SubElement(list_, "l").text = url

        for index, input_ in enumerate(block.inputs):
            SubElement(list_, "l").text = "/"
            encode = SubElement(list_, "block", s="reportTextFunction")
            l = SubElement(encode, "l")
            SubElement(l, "option").text = "encode URI component"
            join = SubElement(encode, "block", s="reportJoinWords")
            SubElement(join, "block", var="arg-{}".format(index))

        if block.shape == "command":
            script_xml = """
            <script>
                <block s="{cmd}">
                    <block s="reifyReporter">
                        <autolambda>
                            {http_block_xml}
                        </autolambda>
                    </block>
                </block>
            </script>
            """.format(
                cmd="doRun" if block.is_blocking else "fork",
                http_block_xml="{http_block_xml}",
            )
        elif block.shape == "predicate":
            script_xml = """
            <script>
                <block s="doDeclareVariables">
                    <list>
                        <l>result</l>
                    </list>
                </block>
                <block s="doSetVar">
                    <l>result</l>
                    {http_block_xml}
                </block>
                <block s="doIf">
                    <block s="reportEquals">
                        <block var="result"/>
                        <l>true</l>
                    </block>
                    <script>
                        <block s="doSetVar">
                            <l>result</l>
                            <block s="reportTrue"/>
                        </block>
                    </script>
                </block>
                <block s="doIf">
                    <block s="reportEquals">
                        <block var="result"/>
                        <l>false</l>
                    </block>
                    <script>
                        <block s="doSetVar">
                            <l>result</l>
                            <block s="reportFalse"/>
                        </block>
                    </script>
                </block>
                <block s="doReport">
                    <block var="result"/>
                </block>
            </script>
            """
        elif block.shape == "reporter":
            script_xml = """
            <script>
                <block s="doReport">
                    {http_block_xml}
                </block>
            </script>
            """

        script = ElementTree.fromstring(script_xml.format(
            http_block_xml=str(ElementTree.tostring(http_block).decode("utf-8"))
        ))
        defn.append(script)

    return ElementTree.tostring(root)

Program.by_short_name["snap"] = SnapProgram


def generate_file(descriptor, program_short_name, language_code="en"):
    program = Program.by_short_name[program_short_name]
    filename = Program.get_filename(descriptor, language_code)
    language = descriptor.translations[language_code]
    contents = program.generate_file(descriptor, language)
    return filename, contents

