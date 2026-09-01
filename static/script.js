async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");

    if (fileInput.files.length === 0) {

        alert("Select a PDF");

        return;
    }

    const formData = new FormData();

    formData.append(
        "pdf",
        fileInput.files[0]
    );

    const response = await fetch("/upload", {

        method: "POST",

        body: formData

    });

    const data = await response.json();

    alert(data.message);

}