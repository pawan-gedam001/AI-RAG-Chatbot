async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF.");
        return;
    }

    const formData = new FormData();

    formData.append("pdf", fileInput.files[0]);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    alert(data.message);
}


async function sendMessage() {

    const question = document.getElementById("question").value;

    if (question.trim() === "") {
        alert("Please enter a question.");
        return;
    }

    document.getElementById("answer").innerHTML = "Thinking...";

    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })

    });

    const data = await response.json();

    document.getElementById("answer").innerHTML = data.answer;
}