import unittest
from src.mdblocks import BlockType, markdown_to_blocks, block_to_blocktype, text_from_block, markdown_to_htmlnode


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(expected, blocks)

    def test_markdown_to_blocks_empty_newline(self):
        expected = [
            "There's only one block",
        ]
        md = """
There's only one block


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(expected, blocks)

    def test_markdown_to_blocks_leading_whitespace(self):
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        md = """
This is **bolded** paragraph  

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line  

- This is a list
- with items  
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(expected, blocks)

    def test_block_to_blocktype_paragraph(self):
        expected = BlockType.PARAGRAPH
        block = "This is a paragraph block"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_block_to_blocktype_heading(self):
        expected = BlockType.HEADING
        block = "###### This is a heading block"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_block_to_blocktype_code(self):
        expected = BlockType.CODE
        block = "```\nThere's some code here\n```"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_block_to_blocktype_code_multiline(self):
        expected = BlockType.CODE
        block = "```\nThere's some code here\nand here too\n```"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_block_to_blocktype_quote(self):
        expected = BlockType.QUOTE
        block = "> This is a quote block\n>this should still be a quote"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_block_to_blocktype_list(self):
        expected = BlockType.LIST
        block = "- This is a list item\n- This should still be a list item"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_block_to_blocktype_ordered_list(self):
        expected = BlockType.NUM_LIST
        block = "1. This is a list item\n2. This should still be a list item"
        blocktype = block_to_blocktype(block)
        self.assertEqual(expected, blocktype)

    def test_text_from_block_heading(self):
        expected = "This is a heading"
        block = "### This is a heading"
        text = text_from_block(block)
        self.assertEqual(expected, text)

    def test_text_from_block_code(self):
        expected = "This is a\ncode block\n"
        block = "```\nThis is a\ncode block\n```"
        text = text_from_block(block)
        self.assertEqual(expected, text)

    def test_text_from_block_quote(self):
        expected = "This is a quote"
        block = "> This is a quote"
        text = text_from_block(block)
        self.assertEqual(expected, text)

    def test_text_from_block_list(self):
        expected = [
            "This is a list item",
            "This is another list item"
        ]
        block = "- This is a list item\n- This is another list item"
        text = text_from_block(block)
        self.assertEqual(expected, text)

    def test_text_from_block_ordered_list(self):
        expected = [
            "This is an ordered list item",
            "This is another ordered list item"
        ]
        block = "1. This is an ordered list item\n2. This is another ordered list item"
        text = text_from_block(block)
        self.assertEqual(expected, text)

    def test_text_from_block_paragraph(self):
        expected = "This is a paragraph block"
        block = "This is a paragraph block"
        text = text_from_block(block)
        self.assertEqual(expected, text)

    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html,
        )

    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            html,
        )

    def test_markdown_to_html_node_headings(self):
        md = """
# Heading 1

This is the first heading.

## Heading 2

This is the second heading.

### Heading 3

This is the third heading.

#### Heading 4

This is the fourth heading.
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            "<div><h1>Heading 1</h1><p>This is the first heading.</p><h2>Heading 2</h2><p>This is the second heading.</p><h3>Heading 3</h3><p>This is the third heading.</p><h4>Heading 4</h4><p>This is the fourth heading.</p></div>",
            html,
        )

if __name__ == "__main__":
    unittest.main()
