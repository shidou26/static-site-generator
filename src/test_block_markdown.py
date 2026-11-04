import unittest
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Invalid Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpaceHeading"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        code_block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\ninline-like code\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nunclosed code"), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        quote_single = "> This is a single line quote"
        quote_multi = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(quote_single), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quote_multi), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        ulist = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ulist), BlockType.ULIST)

    def test_block_to_block_type_ordered_list(self):
        olist = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(olist), BlockType.OLIST)
        
        # Out of order numbers should be a paragraph
        invalid_olist = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(invalid_olist), BlockType.PARAGRAPH)
        
        # Starting with wrong number should be a paragraph
        wrong_start_olist = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(wrong_start_olist), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        paragraph = "This is a regular paragraph with no special markdown block prefixes."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
