import re
from enum import Enum
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    blocks = [block.strip() for block in blocks]

    blocks = [block for block in blocks if block != ""]

    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code block
    if lines[0].startswith("```") and lines[-1] == "```":
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    if all(re.match(r"^[0-9]+\. ", line) for line in lines):
        expected_number = 1

        for line in lines:
            number = int(line.split(".")[0])

            if number != expected_number:
                return BlockType.PARAGRAPH

            expected_number += 1

        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
