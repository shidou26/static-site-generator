from htmlnode import HTMLNode, ParentNode, LeafNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    root = ParentNode("div", [])

    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        # print(markdown_block)
        # print(block_type)

        if block_type == BlockType.PARAGRAPH:
            child = ParentNode("p", [])
            paragraph_text = " ".join(markdown_block.split("\n"))
            sections = text_to_textnodes(paragraph_text)
            for section in sections:
                child.children.append(text_node_to_html_node(section))
            root.children.append(child)
        elif block_type == BlockType.HEADING:
            level = 0
            for c in markdown_block:
                if c == '#': level += 1 
                else: break 
            child = ParentNode(f"h{level}", [])
            sections = text_to_textnodes(markdown_block[level+1:])
            for section in sections:
                child.children.append(text_node_to_html_node(section))
            root.children.append(child)
        elif block_type == BlockType.QUOTE:
            child = ParentNode("blockquote", [])
            lines = markdown_block.split("\n")
            cleaned_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                cleaned_lines.append(line.lstrip(">").strip())
            quote_text = " ".join(cleaned_lines)
            sections = text_to_textnodes(quote_text)
            for section in sections:
                child.children.append(text_node_to_html_node(section))
            root.children.append(child)
        elif block_type == BlockType.ULIST:
            child = ParentNode("ul", [])
            markdown_inline = markdown_block.split("\n")
            for line in markdown_inline:
                sections = text_to_textnodes(line[2:])
                mid = ParentNode("li", [])
                for section in sections:
                    mid.children.append(text_node_to_html_node(section))
                child.children.append(mid)
            root.children.append(child)
        elif block_type == BlockType.OLIST:
            child = ParentNode("ol", [])
            markdown_inline = markdown_block.split("\n")
            for line in markdown_inline:
                sections = text_to_textnodes(line.split(". ", 1)[1])
                mid = ParentNode("li", [])
                for section in sections:
                    mid.children.append(text_node_to_html_node(section))
                child.children.append(mid)
            root.children.append(child) 
        elif block_type == BlockType.CODE:
            child = ParentNode("pre", [])
            another_child = ParentNode("code", [])
            lines = markdown_block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"
            another_child.children.append(LeafNode(None, code_text))
            child.children.append(another_child)
            root.children.append(child)
        else:
            # print(len(markdown_blocks))
            # print(markdown_blocks)
            raise Exception(f"{block_type} is not recognized")

    return root
