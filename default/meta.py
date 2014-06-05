"""LEXOR to HTML META NodeConverter

Attach the meta info to the main document.

"""

from lexor.core.converter import NodeConverter


class MetaNC(NodeConverter):
    """Attach the entries to the document meta attribute. """

    def end(self, node):
        for entry in node.child:
            node.owner.meta[entry['name']] = entry.data
        return self.converter.remove_node(node)
