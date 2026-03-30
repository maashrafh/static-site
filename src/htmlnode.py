class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_props = ""
        if self.props:
            for prop in self.props:
                html_props += f' {prop}="{self.props[prop]}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if len(self.children) == 0:
            raise ValueError("child value missing")
        return (
            f"<{self.tag}>{''.join(list(map(lambda x: (
                            x.to_html()
                        ), self.children)))}</{self.tag}>"
        )
