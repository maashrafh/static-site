import textnode as tn
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not tn.TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("delimiter not closed!")

        for i in range(0, len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 != 0:
                new_nodes.append(tn.TextNode(split_text[i], text_type=text_type))
                continue
            new_nodes.append(tn.TextNode(split_text[i], tn.TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_from_markdown_extract(type, old_nodes):
    new_nodes = []
    if type == 'images':
        node_type = tn.TextType.IMAGE
        extractor = extract_markdown_images
        def delimiter(text, url):
            return f'![{text}]({url})'
    elif type == 'links':
        node_type = tn.TextType.LINK
        extractor = extract_markdown_links
        def delimiter(text, url):
            return f'[{text}]({url})'

    for node in old_nodes:
        if node.text_type is not tn.TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extractor(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for text, url in matches:
            delim = delimiter(text, url)
            split_text = remaining_text.split(delim)
            remaining_text = split_text[1] if len(split_text) > 1 else ''
            if split_text[0]:
                new_nodes.append(tn.TextNode(split_text[0], tn.TextType.TEXT))
            new_nodes.append(tn.TextNode(text, node_type, url))

        if remaining_text:
            new_nodes.append(tn.TextNode(remaining_text, tn.TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_from_markdown_extract('images', old_nodes)

def split_nodes_link(old_nodes):
    return split_nodes_from_markdown_extract('links', old_nodes)

def text_to_textnodes(text):
    md_delimiters = {
        '**' : tn.TextType.BOLD,
        '_' : tn.TextType.ITALIC,
        '`' : tn.TextType.CODE,
    }

    nodes = [tn.TextNode(text, tn.TextType.TEXT)]
    for delimiter in md_delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, md_delimiters[delimiter])

    nodes = split_nodes_image(split_nodes_link(nodes))
    return nodes
