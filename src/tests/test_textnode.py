import unittest
from src.textnode import TextNode, TextType


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
        self.assertEqual(None, node.url)

    def test_none_url(self):
        node = TextNode("This is a link", TextType.LINK, None)
        self.assertEqual(None, node.url)

    def test_set_url(self):
        expected = "www.google.com"
        url = "www.google.com"
        node = TextNode("This is a link to Google", TextType.LINK, url)
        self.assertEqual(expected, node.url)

if __name__ == "__main__":
    unittest.main()
