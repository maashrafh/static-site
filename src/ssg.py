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
