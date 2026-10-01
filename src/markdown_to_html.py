from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    children = []

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children = text_to_children(text)
            block_nodes.append(ParentNode("p", children))

        elif block_type == BlockType.HEADING:
            parts = block.split(" ", 1)
            heading_level = len(parts[0])
            text = parts[1]

            children = text_to_children(text)

            block_nodes.append(
                ParentNode(f"h{heading_level}", children)
            )

        elif block_type == BlockType.CODE:
            code_text = block[4:-3]

            text_node = TextNode(code_text, TextType.TEXT)
            code_text_node = text_node_to_html_node(text_node)

            code_node = ParentNode(
                "code",
                [code_text_node]
            )

            pre_node = ParentNode(
                "pre",
                [code_node]
            )

            block_nodes.append(pre_node)

        elif block_type == BlockType.QUOTE:
            quote_text = "\n".join(
                line[1:].lstrip()
                for line in block.split("\n")
            )

            children = text_to_children(quote_text)

            block_nodes.append(
                ParentNode("blockquote", children)
            )

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                item_text = line[2:]
                children = text_to_children(item_text)

                list_items.append(
                    ParentNode("li", children)
                )

            block_nodes.append(
                ParentNode("ul", list_items)
            )

        elif block_type == BlockType.ORDERED_LIST:
            list_items = []

            for line in block.split("\n"):
                item_text = line.split(". ", 1)[1]
                children = text_to_children(item_text)

                list_items.append(
                    ParentNode("li", children)
                )

            block_nodes.append(
                ParentNode("ol", list_items)
            )

    return ParentNode("div", block_nodes)
