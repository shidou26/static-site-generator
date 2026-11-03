import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test(self):
        self.assertEqual(
            HTMLNode(
                "div",
                "I hate General Physics I",
                [],
                {"id": "content"}
            ).props_to_html(),
            " id=\"content\""
        )

        self.assertEqual(
            HTMLNode(
                "p",
                "This is a paragraph",
                [],
                {"id": "another-content", "class": "paragraph"}
            ).props_to_html(),
            " id=\"another-content\" class=\"paragraph\""
        )

        self.assertNotEqual(
            HTMLNode(
                "p",
                "This is a paragraph",
                [],
                {"id": "another-content", "class": "paragraph"}
            ).props_to_html(),
            " id=\"another_content\" class=\"paragraph\""
        )

    def test_leaf(self):
        self.assertEqual(
            LeafNode(
                "p",
                "This is a paragraph of text."
            ).to_html(),
            "<p>This is a paragraph of text.</p>"
        )

        self.assertEqual(
            LeafNode(
                "a",
                "Click me!",
                {"href": "https://www.google.com"}
            ).to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

        self.assertEqual(
            LeafNode(
                "p", 
                "Hello, world!"
            ).to_html(), 
            "<p>Hello, world!</p>"
        )       

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
if __name__ == "__main__":
    unittest.main()