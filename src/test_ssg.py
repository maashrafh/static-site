import unittest

from ssg import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSSG(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_two_blocks(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        node = TextNode(
            "This is text with a `code block` and another `code block`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple_old_nodes(self):
        expected_nodes = [
            TextNode("This is a bold text node", TextType.BOLD),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        nodes = [
            TextNode("This is a bold text node", TextType.BOLD),
            TextNode("This is text with a `code block` word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_start_delim(self):
        expected_nodes = [
            TextNode("A code block", TextType.CODE),
            TextNode(" starts this node", TextType.TEXT),
        ]
        node = TextNode("`A code block` starts this node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_not_closed(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with a unclosed `code block", TextType.TEXT)
            split_nodes_delimiter([node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
