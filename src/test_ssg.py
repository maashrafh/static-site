import unittest

from ssg import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_markdown_link(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_images_two_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links_two_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_markdown_links_markdown_image(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )
        self.assertListEqual(matches, [])

if __name__ == "__main__":
    unittest.main()
