document.addEventListener('DOMContentLoaded', () => {
    const fileUploadInput = document.getElementById('file-upload');
    const uploadButton = document.querySelector('.upload-button');
    const progressBar = document.querySelector('.progress-bar');
    const dynamicMessage = document.querySelector('.dynamic-message');
    const cannotUploadMessage = document.querySelector('.cannot-upload-message');
    const fileBlock = document.querySelector('.file-block');
    const fileDetailsContainer = document.getElementById('file-details-container');
    const cards = document.querySelectorAll('.card');
    
    let selectedFiles = [];
    let selectedCardData = '';

    // Handle file selection
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

                const removeIcon = document.createElement('span');
                removeIcon.classList.add('remove-file-icon');
                removeIcon.innerHTML = '<i class="fas fa-trash"></i>';
                removeIcon.addEventListener('click', () => {
                    selectedFiles = selectedFiles.filter(f => f !== file);
                    fileDetail.remove();
                    updateUploadButtonState();
                });

                fileDetail.appendChild(fileNameElement);
                fileDetail.appendChild(fileSizeElement);
                fileDetail.appendChild(removeIcon);

                fileDetailsContainer.appendChild(fileDetail);
            });
            fileBlock.style.display = 'block';
        } else {
            fileBlock.style.display = 'none';
        }
        updateUploadButtonState();
    });

    // Handle card selection
    cards.forEach(card => {
        card.addEventListener('click', () => {
            cards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            selectedCardData = card.dataset.cardIds; // Update to use 'card-ids'
            console.log("Selected Card Data:", selectedCardData); // For debugging
            updateUploadButtonState();
        });
    });

    // Update upload button state based on file and card selection
    function updateUploadButtonState() {
        console.log("Selected Files:", selectedFiles);
        console.log("Selected Card Data:", selectedCardData);
        if (selectedFiles.length > 0 && selectedCardData) {
            uploadButton.classList.add('enabled');
            uploadButton.disabled = false;
        } else {
            uploadButton.classList.remove('enabled');
            uploadButton.disabled = true;
        }
    }

    // Handle file removal
    function handleRemoveFileIcon() {
        const removeFileIcons = document.querySelectorAll('.remove-file-icon');
        removeFileIcons.forEach(icon => {
            icon.addEventListener('click', () => {
                const fileDetail = icon.parentElement;
                const fileName = fileDetail.querySelector('.file-name').textContent;
                selectedFiles = selectedFiles.filter(file => file.name !== fileName);
                fileDetail.remove();
                updateUploadButtonState();
            });
        });
    }

    // Handle file upload
    uploadButton.addEventListener('click', () => {
        console.log("Upload Button Clicked");
        if (selectedFiles.length > 0 && selectedCardData) {
            uploadFiles(selectedFiles, selectedCardData);
        } else {
            cannotUploadMessage.style.display = 'block';
            setTimeout(() => {
                cannotUploadMessage.style.display = 'none';
            }, 3000);
        }
    });

    // Upload files to server
    function uploadFiles(files, cardData) {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        formData.append('cardData', cardData); // Ensure cardData is correctly appended

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
                window.location.href = '/preview'; // Redirect to results page
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