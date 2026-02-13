#!/usr/bin/env python

import re
import sys
import unittest


def header(content):
    if content.startswith("###"):
        content = f"<h3>{content[3:]}</h3>"
    if content.startswith("##"):
        content = f"<h2>{content[2:]}</h2>"
    if content.startswith("#"):
        content = f"<h1>{content[1:]}</h1>"
    return content


def ls(content):
    if content.startswith("-"):
        content = f"<li>{content[1:]}</li>"
    return content


def para(content):
    content = f"<p>{content}</p>"
    return content


def typo(data):
    data = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", data)
    data = re.sub(r"\*(.*?)\*", r"<em>\1</em>", data)
    data = re.sub(r"\`(.*?)\`", r"<code>\1</code>", data)
    return data


def parse(file):
    if not file.endswith(".md"):
        raise Exception("Input a valid file format given is not in .md format")

    with open(file, "r") as f:
        content = f.readlines()
        data = []
        for i in content:
            i = i.strip()
            if i:  # Only process non-empty lines
                if "#" == i[0]:
                    i = typo(i)
                    data.append(header(i))
                elif "-" == i[0]:
                    i = typo(i)
                    data.append(ls(i))
                else:
                    i = typo(i)
                    data.append(para(i))
        return data


def main():
    if len(sys.argv) < 2:
        print("md2html <input_markdown_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if ".md" in input_file:
        try:
            parsed_data = parse(input_file)
            with open("parsed.html", "w") as f:
                f.write("".join(parsed_data))
            print("Successfully created parsed.html")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Please provide a markdown (.md) file")


class TestMarkdownParser(unittest.TestCase):
    def test_header(self):
        self.assertEqual(header("# Title"), "<h1> Title</h1>")
        self.assertEqual(header("## Subtitle"), "<h2> Subtitle</h2>")
        self.assertEqual(header("### Small title"), "<h3> Small title</h3>")

    def test_list(self):
        self.assertEqual(ls("- List item"), "<li> List item</li>")

    def test_paragraph(self):
        self.assertEqual(para("Normal text"), "<p>Normal text</p>")

    def test_typo(self):
        self.assertEqual(typo("**bold**"), "<strong>bold</strong>")
        self.assertEqual(typo("*italic*"), "<em>italic</em>")
        self.assertEqual(typo("`code`"), "<code>code</code>")
        self.assertEqual(
            typo("**bold** and *italic* and `code`"),
            "<strong>bold</strong> and <em>italic</em> and <code>code</code>",
        )

    def test_parse_invalid_file(self):
        with self.assertRaises(Exception):
            parse("test.txt")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=[""])
    else:
        main()
