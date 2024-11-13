let editor;

document.addEventListener('DOMContentLoaded', function() {
    editor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
        mode: 'javascript',
        theme: 'monokai',
        lineNumbers: true,
        readOnly: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4
    });
});

function setEditorMode(filename) {
    const extension = filename.split('.').pop();
    let mode;
    
    switch(extension) {
        case 'py':
            mode = 'python';
            break;
        case 'js':
            mode = 'javascript';
            break;
        case 'html':
            mode = 'xml';
            break;
        default:
            mode = 'javascript';
    }
    
    editor.setOption('mode', mode);
}

function setEditorContent(content) {
    editor.setValue(content);
    editor.refresh();
}
