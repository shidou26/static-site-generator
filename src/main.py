from textnode import TextNode, TextType

def __main__():
    boot_dev = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(boot_dev)

__main__()