import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: nodes.append(node)
        else: 
            i = 0
            substr = ""
            while i < len(node.text):
                if node.text[i:i+len(delimiter)] != delimiter: 
                    substr += node.text[i]
                    i += 1  
                else: 
                    nodes.append(TextNode(substr, TextType.TEXT))
                    j = i + 1
                    while j < len(node.text):
                        if node.text[j:j+len(delimiter)] == delimiter: break 
                        j += 1
                    if node.text[j:j+len(delimiter)] != delimiter: raise Exception("Invalid markdown") 
                    nodes.append(TextNode(node.text[i+len(delimiter):j], text_type))
                    i = j + len(delimiter)
                    substr = ""
            if len(substr) > 0:
                nodes.append(TextNode(substr, TextType.TEXT))

    return nodes 


def extract_markdown_images(text: str) -> list[tuple[str, str]]: 
    matches = re.findall(r"!\[.*?\]\(.*?\)", text)

    links = []
    for match in matches:
        split = match.find(']')
        links.append((match[2:split], match[split+2:len(match)-1]))

    return links

def extract_markdown_links(text: str):
    matches = re.findall(r"(?<!\!)\[.*?\]\(.*?\)", text)

    links = []
    for match in matches:
        split = match.find(']')
        links.append((match[1:split], match[split+2:len(match)-1]))

    return links

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: nodes.append(node)
        else:
            original_text = node.text
            images = extract_markdown_images(node.text)
            if len(images) == 0: 
                nodes.append(node)
                continue
            for image in images:
                sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(sections) != 2: raise ValueError("invalid markdown, image section not closed")
                if sections[0] != "":
                    nodes.append(TextNode(sections[0], TextType.TEXT))
                nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                original_text = sections[1]
            if original_text != "":
                nodes.append(TextNode(original_text, TextType.TEXT))
    return nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: nodes.append(node)
        else:
            original_text = node.text
            links = extract_markdown_links(node.text)
            if len(links) == 0: 
                nodes.append(node)
                continue
            for link in links:
                sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
                if len(sections) != 2: raise ValueError("invalid markdown, link section not closed")
                if sections[0] != "": 
                    nodes.append(TextNode(sections[0], TextType.TEXT))
                nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                original_text = sections[1]
            if original_text != "": 
                nodes.append(TextNode(original_text, TextType.TEXT))
    return nodes

def text_to_textnodes(text: str) -> list[TextNode]: 
    base = [TextNode(text, TextType.TEXT)]
    base = split_nodes_delimiter(base, "**", TextType.BOLD)
    base = split_nodes_delimiter(base, "_", TextType.ITALIC)
    base = split_nodes_delimiter(base, "`", TextType.CODE)
    base = split_nodes_link(base)
    base = split_nodes_image(base)
    return base