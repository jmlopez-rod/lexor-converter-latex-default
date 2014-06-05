"""LEXOR to HTML DOCUMENT NodeConverter

"""

import os
import re
from lexor.core.converter import NodeConverter
from lexor.core.converter import get_converter_namespace


class DocumentClassNC(NodeConverter):
    """Verify that the node has a class. """

    def start(self, node):
        if 'class' not in node:
            self.msg('E001', node)
        return node


class DocumentBodyNC(NodeConverter):
    """Transform the body node. """

    def start(self, node):
        node.name = 'document'
        return node


class BibliographyNC(NodeConverter):
    """Read the bibliography and add a list of references. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        namespace = get_converter_namespace()
        self.re_ref = re.compile(r'@.*\{(.*),')
        if 'latex_bib' not in namespace:
            namespace['latex_bib'] = list()

    def start(self, node):
        latex_bib = get_converter_namespace()['latex_bib']
        if 'src' not in node:
            self.msg('E100', node)
            return node
        src = node['src']
        if src != '/':
            base = os.path.dirname(node.owner.uri_)
            if base != '':
                base += '/'
            src = '%s%s' % (base, src)
        try:
            text = open(src, 'r').read()
        except IOError:
            self.msg('E101', node, [src])
            return self.converter.remove_node(node)
        match = self.re_ref.findall(text)
        latex_bib.extend(match)
        return node

MSG = {
    'E001': 'documentclass does not define a class',
    'E100': 'missing src attribute in bibliography node',
    'E101': 'file `{0}` not found',
}
MSG_EXPLANATION = [
    """
    - A documentclass needs to define a class. See:

        http://en.wikibooks.org/wiki/LaTeX/Document_Structure#Document_classes

    Reports error E001.

""",
    """
    - Python was not able to open the file specified.

    Reports error E101.

""",
]
