import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)  # Skips non-text
            continue
        split_nodes = []
        # Splits the text based on the delimiter
        sections = old_node.text.split(delimiter)
        # The amount of sections is always (Amount of delimiters + 1). 0 Delims gives 1 whole section etc..
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, you're missing a delimiter")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:  # Checks if there's an even amount of sections left. If so it's a TextNode
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:  # And if not, it's not a TextNode
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            # Splits the text into sections before and after the link
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":  # The content before the link is pure text
                # First adds a TextNode for text...
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            # ...Then adds one for a Link
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]  # Cuts off the text before the link
        if original_text != "":  # Handles any remaining text
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    splits = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "***", TextType.BOLD_ITALIC)
    splits = split_nodes_delimiter(splits, "**", TextType.BOLD)
    splits = split_nodes_delimiter(splits, "*", TextType.ITALIC)
    splits = split_nodes_delimiter(splits, "`", TextType.CODE)
    splits = split_nodes_link(splits)
    splits = split_nodes_image(splits)
    return splits


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


print(markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


                         
* This is the first list item in a list block
* This is a list item
* This is another list item"""))
