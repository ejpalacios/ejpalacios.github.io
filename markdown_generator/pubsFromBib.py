#!/usr/bin/env python

# # Publications markdown generator for academicpages
#
# Takes a set of bibtex of publications and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)).
#
# The core python code is also in `pubsFromBibs.py`.
# Run either from the `markdown_generator` folder after replacing updating the publist dictionary with:
# * bib file names
# * specific venue keys based on your bib file preferences
# * any specific pre-text for specific files
# * Collection Name (future feature)

import re
from time import strptime

from pybtex.database.input import bibtex

html_escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;"}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)


def clean_names(authors):
    authors = authors.replace("{\\'{a}}", "á")
    authors = authors.replace("{\\'{e}}", "é")
    authors = authors.replace("{\\`{e}}", "è")
    authors = authors.replace("{\\'{i}}", "í")
    authors = authors.replace("{\\`{u}}", "ù")
    authors = authors.replace("{\\~{n}", "ñ")
    authors = authors.replace("{~}", "-")
    return authors


def clean_protected(test):
    return test.replace("{", "").replace("}", "").replace("\\", "")


def main():
    parser = bibtex.Parser()
    bibdata = parser.parse_file("./assets/bib/bio.bib")
    for key, entry in bibdata.entries.items():
        entry_type = entry.type
        match entry_type:
            case "article":
                venue = clean_protected(entry.fields["journal"])
                category = "article"
            case "incollection":
                venue = clean_protected(entry.fields["booktitle"])
                category = "book"
            case "inproceedings":
                venue = clean_protected(entry.fields["booktitle"])
                category = "conference"
            case _:
                print(entry_type)
                venue = ""
                category = ""

        authors = ""
        n_authors = len(entry.persons["author"])
        for i, author in enumerate(entry.persons["author"]):
            first_name = author.first_names[0][0] + ". "
            middle_name = (
                "" if len(author.middle_names) == 0 else author.middle_names[0] + " "
            )
            last_name = author.last_names[0]
            authors += f"{first_name}{middle_name}{last_name}"
            if i != n_authors - 1:
                authors += ", "
        authors = clean_names(authors)
        authors = clean_protected(authors)

        title = clean_protected(entry.fields["title"])
        doi = entry.fields.get("doi", None)
        month = strptime(entry.fields.get("month", "jan")[:3], "%b").tm_mon
        year = entry.fields.get("year", "1900")
        day = entry.fields.get("day", "01")
        date = f"{year}-{month:02d}-{day}"
        abstract = entry.fields.get("abstract", None)
        google_id = entry.fields.get("google_scholar_id", None)

        url_slug = key.replace(" ", "-")
        url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", url_slug)
        url_slug = url_slug.replace("--", "-")
        filename = f"{date}-{url_slug}"

        md = "---\n"
        md += f'title: "{html_escape(title)}"\n'
        md += "collection: publications\n"
        md += f'authors: "{html_escape(authors)}"\n'
        md += f'venue: "{html_escape(venue)}"\n'
        md += f'category: "{category}"\n'
        md += f"date: {date}\n"
        md += f"entry_type: {entry_type}\n"
        # md += f"permalink: /publications/{filename}\n"
        if google_id:
            md += f"google_id: {google_id}\n"
        if doi:
            md += f"doi: {doi}\n"
        md += "---\n\n"
        md += f"*{authors}*\n\n"
        md += f"{html_escape(venue)}\n\n"
        if abstract:
            md += "## Abstract\n"
            md += f"{html_escape(abstract)}\n\n"
        if doi:
            md += f"DOI: [{doi}](https://doi.org/{doi})\n"

        with open(f"./_publications/{filename}.md", "w", encoding="utf-8") as f:
            f.write(md)
        print(f"SUCESSFULLY PARSED {key}")


if __name__ == "__main__":
    main()
