import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        ).strip()


    def create_client(self):

        if not self.api_key:

            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Please add it to the .env file."
            )

        return genai.Client(
            api_key=self.api_key
        )


    @staticmethod
    def build_prompt(
        document_type,
        parties,
        terms,
        effective_date
    ):

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Create a professional legal document DRAFT based only on the
information provided by the user.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not invent names.
3. Do not invent dates.
4. Do not invent monetary amounts.
5. Do not invent addresses.
6. Do not invent governing law.
7. If important information is missing, use:
   [MISSING INFORMATION]
8. Use professional legal language.
9. Organize the document using clear headings.
10. Number important sections.
11. Include signature blocks when appropriate.
12. Do not use Markdown code fences.
13. Return only the document.
14. This is an AI-generated draft and not legal advice.

DOCUMENT TYPE:

{document_type}

PARTIES:

{parties}

TERMS AND CONDITIONS:

{terms}

EFFECTIVE DATE:

{effective_date}

Create the complete document now.
"""

        return prompt.strip()


    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date
    ):

        client = self.create_client()

        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date
        )

        response = client.models.generate_content(

            model=self.model,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=0.2,

                max_output_tokens=8192
            )
        )

        generated_text = (
            response.text or ""
        ).strip()


        if not generated_text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )


        return generated_text
