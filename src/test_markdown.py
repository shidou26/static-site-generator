import unittest
from markdown import markdown_to_html_node

class TestMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        node = markdown_to_html_node("## A heading")
        self.assertEqual(node.to_html(), "<div><h2>A heading</h2></div>")

    def test_blockquote(self):
        node = markdown_to_html_node("> A quote")
        self.assertEqual(node.to_html(), "<div><blockquote>A quote</blockquote></div>")

    def test_unordered_list(self):
        md = "- First item\n- Second item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>First item</li><li>Second item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>First item</li><li>Second item</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()

