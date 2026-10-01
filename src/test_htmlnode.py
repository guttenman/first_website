import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_none(self):
        node = HTMLNode("p", "Hello")

        self.assertEqual(node.props_to_html(), "")

    def test_props_empty(self):
        node = HTMLNode("p", "Hello", None, {})

        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
