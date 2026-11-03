from functools import reduce

class HTMLNode:
    def __init__(self, tag: None | str = None, 
                       value: None | str = None, 
                       children: None | list["HTMLNode"] = None, 
                       props: None | dict = None):
        self.tag = tag 
        self.value = value 
        self.children = children 
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(sefl):
        raise NotImplementedError("to_html method is not implemented")

    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0: return ""
        attribute_str = ""
        for attribute in self.props:
            attribute_str += f" {attribute}=\"{self.props[attribute]}\""
        return attribute_str

class LeafNode(HTMLNode):
    def __init__(self, tag: None | str, 
                       value: None | str, 
                       props: None | dict = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self) -> str:
        if self.value is None: raise ValueError("Leaf has no value")
        if self.tag is None: return self.value 
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: None | str,
                       children: None | list["HTMLNode"],
                       props: None | dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None: raise ValueError("Parent has no tag")
        if self.children is None: raise ValueError("Parent has no children")
        html_code = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children: html_code += child.to_html() 
        html_code += f"</{self.tag}>"
        return html_code 
