import unittest

from ssg import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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

    def test_split_images(self):
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and nothing else", TextType.TEXT),
        ]
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and nothing else",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_images_two_images(self):
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_images_one_image(self):
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_images_only_image(self):
        expected_nodes = [
            TextNode(
                "This is a image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
            ),
        ]
        node = TextNode(
            "![This is a image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_image_just_text(self):
        expected_nodes = [
            TextNode("This is just text", TextType.TEXT),
        ]
        node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            expected_nodes,
        )

    def test_split_links(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and nothing else", TextType.TEXT),
        ]
        node = TextNode(
            "This is text with a [to boot dev](https://www.boot.dev) and nothing else",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            expected_nodes,
        )

    def test_split_links_two_links(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        node = TextNode(
            "This is text with a [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            expected_nodes,
        )

    def test_split_links_one_link(self):
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
        ]
        node = TextNode(
            "This is text with a [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_links_only_link(self):
        expected_nodes = [
            TextNode("This is a link", TextType.LINK, "https://www.boot.dev"),
        ]
        node = TextNode(
            "[This is a link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_links_just_text(self):
        expected_nodes = [
            TextNode("This is just text", TextType.TEXT),
        ]
        node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            expected_nodes,
        )

    def test_text_to_testnodes(self):
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            expected_nodes,
        )

    def test_text_to_testnodes_only_text(self):
        expected_nodes = [
            TextNode(
                "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev",
                TextType.TEXT,
            ),
        ]
        text = "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            expected_nodes,
        )

    def test_text_to_testnodes_nothing(self):
        expected_nodes = []
        text = ''
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            expected_nodes,
        )

    def test_text_to_testnodes_single_image(self):
        expected_nodes = [
            TextNode(
                "This is a image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
            ),
        ]
        text = "![This is a image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            expected_nodes,
        )

    def test_text_to_testnodes_single_link(self):
        expected_nodes = [
            TextNode("This is a link", TextType.LINK, "https://www.boot.dev"),
        ]
        text = "[This is a link](https://www.boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            expected_nodes,
        )

if __name__ == "__main__":
    unittest.main()
