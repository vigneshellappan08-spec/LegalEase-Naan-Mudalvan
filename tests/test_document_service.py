from services.document_service import (
    format_docx,
    format_pdf,
    format_txt
)

from services.sanitization import (
    sanitize_text,
    split_terms
)


def test_sanitize_text():

    result = sanitize_text(
        '“Hello”—world'
    )

    assert result == '"Hello"-world'


def test_split_terms():

    result = split_terms(
        "One; Two; ; Three"
    )

    assert result == [
        "One",
        "Two",
        "Three"
    ]


def test_txt_export():

    result = format_txt(
        "Hello LegalEase"
    )

    assert result == (
        b"Hello LegalEase"
    )


def test_docx_export():

    result = format_docx(

        "1. Confidentiality\n"
        "The parties agree.",

        "NDA",

        terms=(
            "Confidentiality;"
            "No unauthorized disclosure"
        )
    )


    assert result[:2] == b"PK"


def test_pdf_export():

    result = format_pdf(

        "1. Confidentiality\n"
        "The parties agree.",

        "NDA"
    )


    assert result.startswith(
        b"%PDF"
    )
