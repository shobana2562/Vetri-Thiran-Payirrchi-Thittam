import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


# --------------------------------------------------
# ENVIRONMENT
# --------------------------------------------------

PROJECT_ROOT = (
    Path(__file__).resolve().parents[1]
)

load_dotenv(
    PROJECT_ROOT / ".env"
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide",
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 25px;
}

.preview-box {
    background-color: #111827;
    color: #f3f4f6;
    padding: 25px;
    border-radius: 12px;
    white-space: pre-wrap;
    line-height: 1.6;
    max-height: 650px;
    overflow-y: auto;
}

</style>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOGO
# --------------------------------------------------

logo_path = (
    PROJECT_ROOT
    / "assets"
    / "logo.png"
)

if logo_path.exists():

    col1, col2, col3 = (
        st.columns([1, 2, 1])
    )

    with col2:

        st.image(
            str(logo_path),
            width=120
        )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
AI-Powered Legal Document Draft Generator
</div>
""",
    unsafe_allow_html=True
)


st.info(
    """
LegalEase generates AI-assisted legal document drafts.
Review the generated content for your jurisdiction and
specific circumstances before signing or using it.
"""
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "document" not in st.session_state:

    st.session_state.document = ""


# --------------------------------------------------
# API FUNCTIONS
# --------------------------------------------------

def generate_document(payload):

    response = requests.post(

        f"{BACKEND_URL}/generate",

        json=payload,

        timeout=180,
    )

    response.raise_for_status()

    return response.json()


def export_document(
    document_type,
    content,
    file_format
):

    response = requests.post(

        f"{BACKEND_URL}/export",

        json={

            "document_type":
                document_type,

            "content":
                content,

            "format":
                file_format,
        },

        timeout=60,
    )

    response.raise_for_status()

    return response.content


# --------------------------------------------------
# LAYOUT
# --------------------------------------------------

left, right = st.columns(
    [1, 1]
)


# ==================================================
# LEFT SIDE
# ==================================================

with left:

    st.subheader(
        "📄 Document Details"
    )


    document_type = st.selectbox(

        "Document Type",

        [
            "Employment Contract",

            "Non-Disclosure Agreement (NDA)",

            "Residential Lease Agreement",

            "Freelance Work Contract",

            "Service Agreement",

            "General Agreement",

            "Other",
        ],
    )


    if document_type == "Other":

        document_type = st.text_input(

            "Enter Document Type",

            placeholder=(
                "Example: Partnership Agreement"
            ),
        )


    parties = st.text_area(

        "Parties Involved",

        height=130,

        placeholder="""
Example:

John Doe (Employee)
ABC Technologies Pvt Ltd (Employer)
""",
    )


    terms = st.text_area(

        "Terms & Conditions",

        height=180,

        placeholder="""
Separate each term using semicolon (;)

Example:

Payment within 30 days;
Confidentiality must be maintained;
Either party may terminate with 30 days notice
""",
    )


    dates = st.text_input(

        "Effective Date / Relevant Dates",

        placeholder="September 24, 2026",
    )


    additional_instructions = st.text_area(

        "Additional Instructions",

        height=120,

        placeholder=(
            "Example: Use clear professional language "
            "and include signature blocks."
        ),
    )


    generate_button = st.button(

        "✨ Generate Document",

        type="primary",

        use_container_width=True,
    )


# ==================================================
# RIGHT SIDE
# ==================================================

with right:

    st.subheader(
        "👁️ Document Preview"
    )


    if generate_button:

        if not document_type.strip():

            st.error(
                "Please enter document type."
            )

        elif not parties.strip():

            st.error(
                "Please enter the parties."
            )

        elif not terms.strip():

            st.error(
                "Please enter the terms."
            )

        elif not dates.strip():

            st.error(
                "Please enter the effective date."
            )

        else:

            payload = {

                "document_type":
                    document_type,

                "parties":
                    parties,

                "terms":
                    terms,

                "dates":
                    dates,

                "additional_instructions":
                    additional_instructions,
            }


            with st.spinner(
                "Generating document with Gemini..."
            ):

                try:

                    result = (
                        generate_document(
                            payload
                        )
                    )

                    st.session_state.document = (
                        result["content"]
                    )

                    st.success(
                        "Document generated successfully!"
                    )

                except requests.RequestException as exc:

                    if exc.response is not None:

                        try:

                            error_detail = (
                                exc.response.json()
                            )

                        except Exception:

                            error_detail = (
                                exc.response.text
                            )

                    else:

                        error_detail = str(exc)

                    st.error(
                        f"Backend error: {error_detail}"
                    )


    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    if st.session_state.document:

        preview_text = (
            st.session_state.document
        )

        st.markdown(

            f"""
<div class="preview-box">
{preview_text}
</div>
""",

            unsafe_allow_html=True
        )


        st.divider()


        # --------------------------------------------------
        # EDIT
        # --------------------------------------------------

        st.subheader(
            "✏️ Edit Document"
        )


        edited_document = st.text_area(

            "Edit generated document",

            value=(
                st.session_state.document
            ),

            height=450,

            label_visibility="collapsed",
        )


        st.session_state.document = (
            edited_document
        )


        st.divider()


        # --------------------------------------------------
        # DOWNLOAD
        # --------------------------------------------------

        st.subheader(
            "⬇️ Download"
        )


        col_txt, col_docx, col_pdf = (
            st.columns(3)
        )


        # TXT
        with col_txt:

            try:

                txt_data = (
                    export_document(
                        document_type,
                        edited_document,
                        "txt"
                    )
                )

                st.download_button(

                    "Download TXT",

                    data=txt_data,

                    file_name=(
                        "legalease_document.txt"
                    ),

                    mime="text/plain",

                    use_container_width=True,
                )

            except Exception as exc:

                st.error(
                    f"TXT export error: {exc}"
                )


        # DOCX
        with col_docx:

            try:

                docx_data = (
                    export_document(
                        document_type,
                        edited_document,
                        "docx"
                    )
                )

                st.download_button(

                    "Download DOCX",

                    data=docx_data,

                    file_name=(
                        "legalease_document.docx"
                    ),

                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),

                    use_container_width=True,
                )

            except Exception as exc:

                st.error(
                    f"DOCX export error: {exc}"
                )


        # PDF
        with col_pdf:

            try:

                pdf_data = (
                    export_document(
                        document_type,
                        edited_document,
                        "pdf"
                    )
                )

                st.download_button(

                    "Download PDF",

                    data=pdf_data,

                    file_name=(
                        "legalease_document.pdf"
                    ),

                    mime="application/pdf",

                    use_container_width=True,
                )

            except Exception as exc:

                st.error(
                    f"PDF export error: {exc}"
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "LegalEase • FastAPI • Streamlit • Google Gemini"
)