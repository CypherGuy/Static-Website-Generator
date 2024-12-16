from htmlnode import ParentNode
import re
from htmlnode import HTMLNode, ParentNode, text_node_to_html_node
from leafnode import LeafNode
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, you're missing a delimiter")
        for i, section in enumerate(sections):
            if not section:
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
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
        if not links:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text:
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
        [TextNode(text, TextType.TEXT)], "***", TextType.BOLD_ITALIC
    )
    splits = split_nodes_delimiter(splits, "**", TextType.BOLD)
    splits = split_nodes_delimiter(splits, "*", TextType.ITALIC)
    splits = split_nodes_delimiter(splits, "`", TextType.CODE)
    splits = split_nodes_link(splits)
    return splits


def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split('\n')
    inside_code_block = False
    code_block_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") and not inside_code_block:
            # Start of a code block
            inside_code_block = True
            code_block_lines = [line]
            # Check if it also ends on the same line
            if stripped.endswith("```") and stripped != "```":
                # Single-line code block: starts and ends on this line
                blocks.append('\n'.join(code_block_lines))
                inside_code_block = False
                code_block_lines = []
        elif stripped.endswith("```") and inside_code_block:
            # End of a code block
            code_block_lines.append(line)
            blocks.append('\n'.join(code_block_lines))
            inside_code_block = False
            code_block_lines = []
        elif inside_code_block:
            code_block_lines.append(line)
        else:
            # Normal line
            if stripped == "":
                # Blank line -> separate block
                continue
            else:
                blocks.append(stripped)

    return [b for b in blocks if b.strip()]


def block_to_block_type(markdown):
    if markdown.startswith("```") and markdown.endswith("```") and len(markdown) > 6:
        return ["code"]
    if markdown.startswith("###### "):
        return ["heading 6"]
    elif markdown.startswith("##### "):
        return ["heading 5"]
    elif markdown.startswith("#### "):
        return ["heading 4"]
    elif markdown.startswith("### "):
        return ["heading 3"]
    elif markdown.startswith("## "):
        return ["heading 2"]
    elif markdown.startswith("# "):
        return ["heading 1"]
    elif markdown.startswith("```") and markdown.endswith("```"):
        return ["code"]
    elif all(line.startswith("> ") for line in markdown.split("\n")):
        return ["quote"]
    elif all(line.startswith("* ") for line in markdown.split("\n")):
        return ["ulist"]
    if markdown.startswith("1. "):
        markdown = markdown.split("\n")
        i = 1
        for line in markdown:
            if not line.startswith(f"{i}. "):
                return ["paragraph"]
            i += 1
        return ["olist"]
    return ["paragraph"]


def text_to_children(text):
    if not text:
        return []
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print("Blocks:", blocks)

    children = []
    for block in blocks:
        block = block.strip()
        blockType = block_to_block_type(block)

        if blockType == ["code"]:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("Invalid code block")

            text = block[3:-3]  # Extract the code content exactly as is
            if text.strip() == "":
                # If after stripping it's empty, just make text empty
                text = ""

            code_children = text_to_children(text)
            code_node = ParentNode("code", code_children)
            children.append(ParentNode("pre", [code_node]))
            continue

        elif any(h in blockType for h in ["heading 1", "heading 2", "heading 3", "heading 4", "heading 5", "heading 6"]):
            # Determine the heading level from blockType
            heading_levels = ["heading 1", "heading 2",
                              "heading 3", "heading 4", "heading 5", "heading 6"]
            level = None
            for i, h in enumerate(heading_levels, start=1):
                if h in blockType:
                    level = i
                    break
            # Extract the heading text
            # Adjust indexing as needed based on your block format
            # For example, if the heading block starts with "# " for heading 1, "## " for heading 2, etc.
            # This depends on your markdown_to_blocks and block_to_block_type implementations.
            text = block.strip("# ").strip()
            heading_children = text_to_children(text)
            children.append(ParentNode(f"h{level}", children=heading_children))
            continue

        elif blockType == ["quote"]:
            # A blockquote, remove initial '>' or whatever marker you use
            # Assuming ">" is used as marker
            quoted_text = block.lstrip(">").strip()
            children.append(ParentNode(
                "blockquote", children=text_to_children(quoted_text)))
            continue

        elif blockType == ["ulist"]:
            # Unordered list item, assuming '* ' or '- ' prefix
            # This may depend on how markdown_to_blocks is implemented.
            list_text = block.lstrip("*-").strip()
            li_node = ParentNode("li", children=text_to_children(list_text))
            # If you handle multiple list items separately, you might need a separate step
            # For simplicity, assume this is a single list item. You might need additional logic.
            children.append(ParentNode("ul", children=[li_node]))
            continue

        elif blockType == ["olist"]:
            # Ordered list item, assuming '1. ' prefix
            list_text = block.lstrip("0123456789.").strip()
            li_node = ParentNode("li", children=text_to_children(list_text))
            children.append(ParentNode("ol", children=[li_node]))
            continue

        elif blockType == ["paragraph"]:
            # Regular paragraph
            children.append(ParentNode("p", children=text_to_children(block)))
            continue

        elif blockType == ["image"]:
            # Image block, assuming something like "![alt](url)" is handled by markdown_to_blocks
            # You may need additional parsing here depending on your code.
            # For simplicity, assume block contains URL after a space
            img_url = block.strip("![]() ")
            children.append(
                LeafNode("img", value=None, props={"src": img_url}))
            continue

        elif blockType == ["link"]:
            # Link block, similar parsing as image
            link_url = block.strip("[]() ")
            # If you want the link text same as URL
            link_children = text_to_children(link_url)
            children.append(LeafNode("a", value=link_url,
                            props={"href": link_url}))
            continue

        # If no recognized block type, treat as paragraph or ignore
        else:
            if block:
                children.append(ParentNode(
                    "p", children=text_to_children(block)))
                continue

    return ParentNode("div", children=children)
