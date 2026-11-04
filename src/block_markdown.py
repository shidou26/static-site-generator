import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    base_blocks = markdown.split("\n\n")
    blocks = []
    for block in base_blocks:
        if len(block) == 0: continue 
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block_markdown: str) -> BlockType:
    if re.fullmatch(r"#{1,6} .*", block_markdown): 
        return BlockType.HEADING
    elif block_markdown.startswith("```") and block_markdown.endswith("```"):
        return BlockType.CODE
    elif block_markdown.startswith('>'):
        return BlockType.QUOTE
    else:
        lines = block_markdown.split("\n")
        is_unordered = True 
        is_ordered = True
        order = 0 
        for line in lines:
            order += 1
            if not line.startswith('-'):
                is_unordered = False 
            if not line.startswith(f"{order}. "):
                is_ordered = False 
        if is_unordered: return BlockType.ULIST
        if is_ordered: return BlockType.OLIST
        
    return BlockType.PARAGRAPH