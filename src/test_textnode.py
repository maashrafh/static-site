import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a link", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_none_url(self):
        node = TextNode("This is a link", TextType.LINK, None)
        self.assertEqual(node.url, None)

    def test_set_url(self):
        expected = "www.google.com"
        url = "www.google.com"
        node = TextNode("This is a link to Google", TextType.LINK, url)
        self.assertEqual(node.url, expected)

    def test_text(self):
        expected_tag = None
        expected_value = "This is a text node"
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)

    def test_text_bold(self):
        expected_tag = "b"
        expected_value = "This is a bold text node"
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)

    def test_text_italic(self):
        expected_tag = "i"
        expected_value = "This is a italic text node"
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)

    def test_text_code(self):
        expected_tag = "code"
        expected_value = "This is a code text node"
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)

    def test_text_link(self):
        expected_tag = "a"
        expected_value = "This is a link node"
        expected_props = {"href": "www.google.com"}
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)
        self.assertEqual(html_node.props, expected_props)

    def test_text_image(self):
        expected_tag = "img"
        expected_value = None
        expected_props = {
            "src": "www.example.com/image.png",
            "alt": "This is image.png",
        }
        node = TextNode(
            "This is image.png", TextType.IMAGE, "www.example.com/image.png"
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, expected_tag)
        self.assertEqual(html_node.value, expected_value)
        self.assertEqual(html_node.props, expected_props)


if __name__ == "__main__":
    unittest.main()
