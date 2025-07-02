// src/services/documentService.js
export async function generateDocument(data) {
    const response = await fetch("https://hoso-vayvon-1.onrender.com/generate-document", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    const json = await response.json();
    return json.document;
}
