const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('upload');

uploadButton.addEventListener('click', () => {
    const file = fileInput.files[0]

    if (file) {
        console.log(`Uploading file: ${file.name}`)

        const formData = new FormData()
        formData.append('file', file)

        
    }
})