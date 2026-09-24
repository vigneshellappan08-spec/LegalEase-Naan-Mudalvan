from fastapi.testclient import TestClient

from backend.main import app
from backend.routes import generator


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_generate_document(
    monkeypatch
):

    def fake_generator(**kwargs):

        return (
            "NON-DISCLOSURE AGREEMENT\n\n"
            "1. Confidentiality\n"
            "The parties agree."
        )


    monkeypatch.setattr(
        generator,
        "generate_document",
        fake_generator
    )


    response = client.post(

        "/generate",

        json={

            "document_type":
                "NDA",

            "parties":
                "Alice (Disclosing Party), "
                "Bob (Receiving Party)",

            "terms":
                "Confidentiality; "
                "No unauthorized disclosure",

            "effective_date":
                "2026-09-24"
        }
    )


    assert response.status_code == 200


    result = response.json()


    assert result["success"] is True


    assert (
        "NON-DISCLOSURE"
        in result["content"]
    )


def test_validation():

    response = client.post(

        "/generate",

        json={

            "document_type":
                "",

            "parties":
                "Alice",

            "terms":
                "Confidentiality",

            "effective_date":
                "2026-09-24"
        }
    )


    assert response.status_code == 422
