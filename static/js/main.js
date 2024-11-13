let currentFiles = [];
let chatHistory = [];

function addMessage(message, type = 'user') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message mb-3 p-3 rounded`;
    messageDiv.innerHTML = `<div class="message-content">${message}</div>`;
    document.getElementById('chatHistory').appendChild(messageDiv);
    document.getElementById('chatHistory').scrollTop = document.getElementById('chatHistory').scrollHeight;
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    const modelSelector = document.getElementById('modelSelector');
    const selectedModel = modelSelector.value;
    const templateSelector = document.getElementById('templateSelector');
    const selectedTemplate = templateSelector.value;
    
    if (!message) {
        showError('Please enter a message');
        return;
    }
    
    showProgress();
    hideError();
    
    // Add user message to chat
    addMessage(message, 'user');
    chatHistory.push({ role: 'user', content: message });
    messageInput.value = '';
    
    try {
        console.log('Generating code with:', { message, model: selectedModel, template_id: selectedTemplate });
        
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                model: selectedModel,
                template_id: selectedTemplate || null
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
        
        // Add assistant response to chat
        addMessage('Generated code files:', 'assistant');
        data.files.forEach(file => {
            addMessage(`📄 ${file.path}`, 'assistant');
        });
        
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

// Template description handling
document.getElementById('templateSelector').addEventListener('change', function() {
    const description = this.options[this.selectedIndex].dataset.description;
    const descriptionElement = document.getElementById('templateDescription');
    
    if (description) {
        descriptionElement.textContent = description;
        descriptionElement.classList.remove('d-none');
    } else {
        descriptionElement.classList.add('d-none');
    }
});

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

// Add event listener for Enter key in message input
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
