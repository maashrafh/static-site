from enum import Enum
import re
import src.htmlnode as hn
import src.nodecoverter as nconv


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    LIST = "unordered_list"
    NUM_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split('\n\n'):
        stripped_block = block.strip(' \n')
        if stripped_block:
            blocks.append(stripped_block)
    return blocks

def block_to_blocktype(block):
    blocktype = BlockType.PARAGRAPH
    if re.search(r'(^#{1,6}\s)', block):
        blocktype = BlockType.HEADING
    elif re.search(r'(^```.+?```$)', block, flags=re.DOTALL):
        blocktype = BlockType.CODE
    elif re.search(r'(^>.)', block, flags=re.MULTILINE):
        blocktype = BlockType.QUOTE
    elif re.search(r'(^-.)', block, flags=re.MULTILINE):
        blocktype = BlockType.LIST
    elif re.search(r'(^[0-9]+.)', block, flags=re.MULTILINE):
        blocktype = BlockType.NUM_LIST
    return blocktype

def text_from_block(block):
    text = []
    match block_to_blocktype(block):
        case BlockType.HEADING:
            text = block.strip('# ')
        case BlockType.CODE:
            text = ''.join(re.findall(r'(?!`|\n)(.*)(?<!`)', block, flags=re.DOTALL))
        case BlockType.QUOTE:
            text = block.strip('> ')
        case BlockType.LIST:
            text = re.findall(r'(?<=-\s)(.*)', block)
        case BlockType.NUM_LIST:
            text = re.findall(r'(?<=[1-9].\s)(.*)', block)
        case BlockType.PARAGRAPH:
            text = block.replace('\n', ' ')
    return text

def htmlnode_from_block(block):
    blocktype = block_to_blocktype(block)
    tag_dict = {
        "paragraph" : "p",
        "heading" : "h",
        "code" : "code",
        "quote" : "quote",
        "unordered_list" : "ul",
        "ordered_list" : "ol",
    }
    if blocktype is BlockType.CODE:
        child_node = hn.LeafNode(tag="code", value=text_from_block(block))
        return hn.ParentNode(tag="pre", children=[child_node])
    elif blocktype is BlockType.HEADING:
        tag = f'{tag_dict[blocktype.value]}' + f'{len(re.findall(r'#', block))}'
        return hn.LeafNode(tag=tag, value=text_from_block(block))
    else:
        text = text_from_block(block)
        text_nodes = nconv.text_to_textnodes(text)
        child_node = list(map(nconv.textnode_to_htmlnode, text_nodes))
    return hn.ParentNode(tag=tag_dict[blocktype.value], children=child_node)

def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        node = htmlnode_from_block(block)
        child_nodes.append(node)
    return hn.ParentNode(tag="div",children=child_nodes)
