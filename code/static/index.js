document.addEventListener('DOMContentLoaded', () => {
    const fileUploadInput = document.getElementById('file-upload');
    const uploadButton = document.querySelector('.upload-button');
    const progressBar = document.querySelector('.progress-bar');
    const dynamicMessage = document.querySelector('.dynamic-message');
    const cannotUploadMessage = document.querySelector('.cannot-upload-message');
    const fileBlock = document.querySelector('.file-block');
    const fileDetailsContainer = document.getElementById('file-details-container');

    let selectedFiles = [];
    let selectedCardData = '';

    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', () => {
            cards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            selectedCardData = card.dataset.cardId; // Ensure this is correctly assigned
            console.log("Selected Card Data:", selectedCardData); // For debugging
            updateUploadButtonState();
        });
    });

    function updateUploadButtonState() {
        if (selectedFiles.length > 0 && selectedCardData) {
            uploadButton.classList.add('enabled');
            uploadButton.disabled = false;
        } else {
            uploadButton.classList.remove('enabled');
            uploadButton.disabled = true;
        }
    }

    fileUploadInput.addEventListener('change', (event) => {
        fileDetailsContainer.innerHTML = '';
        selectedFiles = Array.from(event.target.files);

        if (selectedFiles.length > 0) {
            selectedFiles.forEach(file => {
                const fileDetail = document.createElement('div');
                fileDetail.classList.add('file-detail');

                const fileNameElement = document.createElement('span');
                fileNameElement.classList.add('file-name');
                fileNameElement.textContent = file.name;

                const fileSizeElement = document.createElement('span');
                fileSizeElement.classList.add('file-size');
                fileSizeElement.textContent = `${(file.size / 1024).toFixed(2)} KB`;

                const removeFileIcon = document.createElement('span');
                removeFileIcon.classList.add('remove-file-icon');
                removeFileIcon.innerHTML = '<i class="fas fa-trash"></i>';
                removeFileIcon.addEventListener('click', () => {
                    selectedFiles = selectedFiles.filter(f => f !== file);
                    fileDetail.remove();
                    updateUploadButtonState();
                });

                fileDetail.appendChild(fileNameElement);
                fileDetail.appendChild(fileSizeElement);
                fileDetail.appendChild(removeFileIcon);

                fileDetailsContainer.appendChild(fileDetail);
            });
            fileBlock.style.display = 'block';
            updateUploadButtonState();
        } else {
            fileBlock.style.display = 'none';
            updateUploadButtonState();
        }
    });

    uploadButton.addEventListener('click', () => {
        if (selectedFiles.length > 0 && selectedCardData) {
            uploadFiles(selectedFiles, selectedCardData);
        } else {
            cannotUploadMessage.style.display = 'block';
        }
    });

    function uploadFiles(files, cardData) {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        formData.append('cardData', cardData);  // Ensure cardData is correctly appended

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);

        xhr.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                progressBar.style.width = percentComplete + '%';
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                progressBar.style.width = '100%';
                dynamicMessage.textContent = 'Files uploaded successfully!';
                window.location.href = '/preview';
            } else {
                dynamicMessage.textContent = 'Upload failed.';
            }
        });

        xhr.addEventListener('error', () => {
            dynamicMessage.textContent = 'Upload failed.';
        });

        xhr.send(formData);
    }
});
