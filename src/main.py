from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


def main():
    text = TextNode("lorem ipsum", TextType.TEXT)
    print(text)


if __name__ == "__main__":
    main()
