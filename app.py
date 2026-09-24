import html
import os

from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from services.document_service import (
    format_docx,
    format_pdf,
    format_txt
)

from services.sanitization import sanitize_text


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


# ------------------------------------------------
# CSS
# ------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 2.5rem;

        font-weight: 700;

        margin-bottom: 5px;

    }


    .subtitle {

        text-align: center;

        color: #777;

        margin-bottom: 25px;

    }


    .preview {

        background: #111827;

        color: #f3f4f6;

        border-radius: 12px;

        padding: 25px;

        max-height: 650px;

        overflow-y: auto;

        white-space: pre-wrap;

        font-family: Georgia, serif;

        line-height: 1.7;

        border: 1px solid #374151;

    }


    .notice {

        background: #fff7ed;

        border-left: 4px solid #f97316;

        padding: 12px;

        border-radius: 6px;

        margin-bottom: 20px;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------
# Session state
# ------------------------------------------------

if "generated_text" not in st.session_state:

    st.session_state.generated_text = ""


if "document_type" not in st.session_state:

    st.session_state.document_type = (
        "Legal Document"
    )


if "terms" not in st.session_state:

    st.session_state.terms = ""


# ------------------------------------------------
# Logo
# ------------------------------------------------

logo_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "logo.svg"
)


if os.path.exists(logo_path):

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.image(
            logo_path,
            width=110
        )


# ------------------------------------------------
# Header
# ------------------------------------------------

st.markdown(
    '<div class="main-title">'
    'LegalEase'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="notice">

    <b>Important:</b>

    LegalEase creates AI-assisted legal drafts.
    It is not a substitute for professional legal advice.
    Review important documents with a qualified legal
    professional before signing or relying on them.

    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------
# Layout
# ------------------------------------------------

left_column, right_column = st.columns(
    [1, 1],
    gap="large"
)


# =================================================
# LEFT SIDE
# =================================================

with left_column:

    st.subheader(
        "Document Details"
    )


    document_type = st.text_input(

        "Document Type",

        placeholder=(
            "Example: "
            "Non-Disclosure Agreement"
        )
    )


    parties = st.text_area(

        "Parties Involved",

        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=120
    )


    terms = st.text_area(

        "Terms & Conditions",

        placeholder=(
            "Separate each term with a semicolon.\n\n"
            "Example:\n"
            "Confidentiality must be maintained; "
            "Payment must be made within 30 days; "
            "Either party may terminate with 15 days notice"
        ),

        height=180
    )


    effective_date = st.date_input(

        "Effective Date",

        value=date.today()
    )


    logo = st.file_uploader(

        "Upload Company Logo (Optional)",

        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    generate_button = st.button(

        "Generate Document",

        type="primary",

        use_container_width=True
    )


    # --------------------------------------------
    # Generate document
    # --------------------------------------------

    if generate_button:

        if not document_type.strip():

            st.error(
                "Please enter the document type."
            )


        elif not parties.strip():

            st.error(
                "Please enter the parties."
            )


        elif not terms.strip():

            st.error(
                "Please enter the terms and conditions."
            )


        else:

            request_data = {

                "document_type":
                    document_type.strip(),

                "parties":
                    parties.strip(),

                "terms":
                    terms.strip(),

                "effective_date":
                    effective_date.isoformat()
            }


            try:

                with st.spinner(
                    "Generating legal document..."
                ):

                    response = requests.post(

                        f"{BACKEND_URL}/generate",

                        json=request_data,

                        timeout=120
                    )


                if response.status_code == 200:

                    result = response.json()


                    st.session_state.generated_text = (
                        result["content"]
                    )


                    st.session_state.document_type = (
                        document_type
                    )


                    st.session_state.terms = (
                        terms
                    )


                    st.success(
                        "Document generated successfully!"
                    )


                else:

                    try:

                        error_message = (
                            response.json()
                            .get(
                                "detail",
                                response.text
                            )
                        )

                    except Exception:

                        error_message = (
                            response.text
                        )


                    st.error(
                        f"Backend error: "
                        f"{error_message}"
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend. "
                    "Make sure the backend is running."
                )


            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Please try again."
                )


            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )


# =================================================
# RIGHT SIDE
# =================================================

with right_column:

    st.subheader(
        "Document Preview"
    )


    if st.session_state.generated_text:

        clean_text = sanitize_text(
            st.session_state.generated_text
        )


        # ----------------------------------------
        # Preview
        # ----------------------------------------

        st.markdown(

            f"""
            <div class="preview">
            {html.escape(clean_text)}
            </div>
            """,

            unsafe_allow_html=True
        )


        st.write("")


        # ----------------------------------------
        # Editable document
        # ----------------------------------------

        edited_document = st.text_area(

            "Edit Document",

            value=(
                st.session_state.generated_text
            ),

            height=500
        )


        st.session_state.generated_text = (
            edited_document
        )


        # ----------------------------------------
        # Downloads
        # ----------------------------------------

        st.subheader(
            "Download Document"
        )


        filename = (

            st.session_state.document_type

            .lower()

            .replace(" ", "_")

            .replace("/", "_")

            .replace("\\", "_")

        )


        if not filename:

            filename = "legalease_document"


        # TXT

        txt_file = format_txt(
            edited_document
        )


        # DOCX

        docx_file = format_docx(

            edited_document,

            st.session_state.document_type,

            terms=(
                st.session_state.terms
            ),

            logo_bytes=(
                logo.getvalue()
                if logo
                else None
            ),

            logo_name=(
                logo.name
                if logo
                else "logo.png"
            )
        )


        # PDF

        pdf_file = format_pdf(

            edited_document,

            st.session_state.document_type
        )


        download_1, download_2, download_3 = (
            st.columns(3)
        )


        with download_1:

            st.download_button(

                "Download TXT",

                data=txt_file,

                file_name=(
                    f"{filename}.txt"
                ),

                mime="text/plain",

                use_container_width=True
            )


        with download_2:

            st.download_button(

                "Download DOCX",

                data=docx_file,

                file_name=(
                    f"{filename}.docx"
                ),

                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),

                use_container_width=True
            )


        with download_3:

            st.download_button(

                "Download PDF",

                data=pdf_file,

                file_name=(
                    f"{filename}.pdf"
                ),

                mime="application/pdf",

                use_container_width=True
            )


    else:

        st.info(
            "Your generated document will "
            "appear here."
        )
