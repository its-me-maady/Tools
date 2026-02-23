#!/usr/bin/env python

import re
import argparse
import unittest
import sys
import argcomplete


def header(content):
    if content.startswith("###"):
        content = f"<h3>{content[3:]}</h3>"
    elif content.startswith("##"):
        content = f"<h2>{content[2:]}</h2>"
    elif content.startswith("#"):
        content = f"<h1>{content[1:]}</h1>"
    return content


def ls(content):
    if content.startswith("-"):
        content = f"<li>{content[1:]}</li>"
    return content


def para(content):
    return f"<p>{content}</p>"


def typo(data):
    data = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", data)
    data = re.sub(r"\*(.*?)\*", r"<em>\1</em>", data)
    data = re.sub(r"\`(.*?)\`", r"<code>\1</code>", data)
    return data


def parse(file):
    if not file.endswith(".md"):
        raise Exception("Input file must be in .md format")

    with open(file, "r") as f:
        content = f.readlines()
        data = []

        for i in content:
            i = i.strip()
            if i:
                i = typo(i)

                if i.startswith("#"):
                    data.append(header(i))
                elif i.startswith("-"):
                    data.append(ls(i))
                else:
                    data.append(para(i))

        return data


def main():
    parser = argparse.ArgumentParser(
        prog="md2html",
        description="Simple Markdown to HTML converter",
        epilog="Thanks for using md2html :)",
    )

    parser.add_argument("input_file", nargs="?", help="Input markdown (.md) file")

    parser.add_argument("--test", action="store_true", help="Run unit tests")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # Run tests if --test is provided
    if args.test:
        unittest.main(argv=[sys.argv[0]])
        return

    # If no file provided
    if not args.input_file:
        parser.print_help()
        return

    # Validate extension
    if not args.input_file.endswith(".md"):
        print("Please provide a markdown (.md) file")
        return

    try:
        parsed_data = parse(args.input_file)
        with open("parsed.html", "w") as f:
            f.write("".join(parsed_data))
        print("Successfully created parsed.html")
    except Exception as e:
        print(f"Error: {e}")


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
    main()
