let currentFiles = [];

async function generateCode() {
    const projectTitle = document.getElementById('projectTitle').value;
    const requirements = document.getElementById('requirements').value;
    const specifications = document.getElementById('specifications').value;
    
    if (!requirements) {
        showError('Requirements are required');
        return;
    }
    
    showProgress();
    hideError();
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: projectTitle,
                requirements: requirements,
                specifications: specifications
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        currentFiles = data.files;
        updateFileList(data.files);
        
        if (currentFiles.length > 0) {
            displayFile(currentFiles[0]);
        }
        
    } catch (error) {
        showError('An error occurred while generating code');
    } finally {
        hideProgress();
    }
}

function updateFileList(files) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    
    files.forEach((file, index) => {
        const item = document.createElement('a');
        item.className = 'list-group-item list-group-item-action file-item';
        item.textContent = file.path;
        item.onclick = () => displayFile(file);
        fileList.appendChild(item);
    });
}

function displayFile(file) {
    setEditorMode(file.path);
    setEditorContent(file.content);
}

function showProgress() {
    document.getElementById('generationProgress').classList.remove('d-none');
}

function hideProgress() {
    document.getElementById('generationProgress').classList.add('d-none');
}

function showError(message) {
    const errorElement = document.getElementById('generationError');
    errorElement.textContent = message;
    errorElement.classList.remove('d-none');
}

function hideError() {
    document.getElementById('generationError').classList.add('d-none');
}
