"""LEXOR to HTML PARAGRAPH NodeConverter

Some paragraphs nodes may have been marked for deletion during the
parsing process. This converter removes them. Here we assume that the
pargraph has child nodes.

"""

from lexor.core.converter import NodeConverter


class ParagraphNC(NodeConverter):
    """Remove the paragraph nodes with the remove attribute. """

    def end(self, node):
        if 'remove' not in node:
            return node
        node.parent.extend_before(node.index, node)
        index = node.index
        parent = node.parent
        del node.parent[node.index]
        try:
            return parent[index]
        except IndexError:
            return parent[index-1]
