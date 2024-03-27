class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            raise TypeError("HTMLNode equalitycheck: comparison value is not HTMLNode")
        
        if self.children is None:
            if other.children is not None:
                return False
        else:
            if len(self.children) != len(other.children):
                for i in self.children:
                    if self.children.count(i) != other.children.count(i):
                        return False


        if self.tag == other.tag and self.value == other.value and self.props == other.props:
            return True
        return False

    def to_html(self):
        raise NotImplementedError("Chesca add this method.")
    
    def props_to_html(self, props):
        if not props:
            return ""
        if not isinstance(props, dict):
            raise ValueError("Please input props as dict (props_to_html)")
        props_html = ""
        for i in props:
            props_html += f" {i}=\"{props[i]}\""
        return props_html

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if value is None:
            raise ValueError("LeafNode requires a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leafnode requires a value")

        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html(self.props)}>{self.value}</{self.tag}>"           
    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("This instance has no tag property")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        html = []
        html_string = ""
        for i in self.children:
            html.append(i.to_html())
        
        html_string = f"<{self.tag}{self.props_to_html(self.props)}>{"".join(html)}</{self.tag}>"


        return html_string
    