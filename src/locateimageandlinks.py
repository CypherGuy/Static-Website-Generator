import re


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^()\s]+)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^()\s]+)\)", text)
