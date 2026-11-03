import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test(self):
        self.assertEqual(
            TextNode("This is a text node", TextType.BOLD), 
            TextNode("This is a text node", TextType.BOLD)                 
        )

        self.assertNotEqual(
            TextNode("This is not a text node", TextType.IMAGE),
            TextNode("This is still a text node", TextType.BOLD)
        )

        self.assertEqual(
            TextNode("not an url", TextType.BOLD),
            TextNode("not an url", TextType.BOLD, None)
        )
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()