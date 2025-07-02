// src/services/documentService.js
export async function generateDocument(data) {
    const response = await fetch("http://127.0.0.1:8000/generate-document", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    const json = await response.json();
    return json.document;
}
