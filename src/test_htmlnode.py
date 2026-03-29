import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank",}
        expected_props = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(tag=None, value=None, children=None, props=props)
        self.assertEqual(node.props_to_html(), expected_props)

    def test_empty_props_to_html(self):
        props = {}
        expected_props = ''
        node = HTMLNode(tag=None, value=None, children=None, props=props)
        self.assertEqual(node.props_to_html(), expected_props)

    def test_empty_node_props_to_html(self):
        expected_props = ''
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), expected_props)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a(self):
        props = {"href": "https://www.google.com",}
        node = LeafNode("a", "Click me!", props=props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()
