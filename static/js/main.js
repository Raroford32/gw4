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
        console.log('Generating code with:', { projectTitle, requirements, specifications });
        
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
        console.log('Received response:', data);
        
        if (data.error) {
            console.error('Generation error:', data.error);
            showError(data.error);
            return;
        }
        
        if (!data.files || data.files.length === 0) {
            console.warn('No files received in response');
            showError('No code files were generated');
            return;
        }
        
        currentFiles = data.files;
        console.log('Updating file list with:', currentFiles);
        updateFileList(currentFiles);
        
        displayFile(currentFiles[0]);
        
    } catch (error) {
        console.error('Error during code generation:', error);
        showError('An error occurred while generating code');
    } finally {
        hideProgress();
    }
}

function updateFileList(files) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    
    console.log('Populating file list with:', files);
    
    files.forEach((file, index) => {
        const item = document.createElement('a');
        item.className = 'list-group-item list-group-item-action file-item';
        item.textContent = file.path;
        item.onclick = () => displayFile(file);
        fileList.appendChild(item);
    });
}

function displayFile(file) {
    console.log('Displaying file:', file);
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
    console.error('Showing error:', message);
    const errorElement = document.getElementById('generationError');
    errorElement.textContent = message;
    errorElement.classList.remove('d-none');
}

function hideError() {
    document.getElementById('generationError').classList.add('d-none');
}
