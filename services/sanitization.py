import re
import unicodedata


def sanitize_text(text: str) -> str:

    if not text:
        return ""


    text = unicodedata.normalize(
        "NFKC",
        text
    )


    replacements = {

        "\u2018": "'",
        "\u2019": "'",

        "\u201c": '"',
        "\u201d": '"',

        "\u2013": "-",
        "\u2014": "-",

        "\u2022": "-",

        "\u00a0": " "
    }


    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )


    text = "".join(

        char

        for char in text

        if (
            char in "\n\t"
            or unicodedata.category(char)[0] != "C"
        )
    )


    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )


    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text
    )


    return text.strip()


def split_terms(terms: str):

    return [
        term.strip()

        for term in terms.split(";")

        if term.strip()
    ]
