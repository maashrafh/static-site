import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        expected = ' href="https://www.google.com" target="_blank"'
        props = {"href": "https://www.google.com", "target": "_blank", }
        node = HTMLNode(tag=None, value=None, children=None, props=props)
        self.assertEqual(node.props_to_html(), expected)

    def test_empty_props_to_html(self):
        expected = ''
        props = {}
        node = HTMLNode(tag=None, value=None, children=None, props=props)
        self.assertEqual(node.props_to_html(), expected)

    def test_empty_node_props_to_html(self):
        expected = ''
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_to_html_p(self):
        expected = '<p>Hello, world!</p>'
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_raw(self):
        expected = 'Hello, world!'
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_a(self):
        expected = '<a href="https://www.google.com">Click me!</a>'
        props = {"href": "https://www.google.com", }
        node = LeafNode("a", "Click me!", props=props)
        self.assertEqual(node.to_html(), expected)

    def test_leaf_none_to_html(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError)

    def test_parent_to_html_with_children(self):
        expected = '<div><span>child</span></div>'
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_to_html_with_grandchildren(self):
        expected = '<div><span><b>grandchild</b></span></div>'
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_to_html_with_raw_children(self):
        expected = '<div>child</div>'
        child_node = LeafNode(None, "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_raw_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError)

    def test_parent_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError)

    def test_parent_none_to_html(self):
        node = ParentNode(None, None)
        self.assertRaises(ValueError)

if __name__ == "__main__":
    unittest.main()
