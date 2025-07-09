
const loadFileButton = document.getElementById('OpenFile');
const runScriptButton = document.getElementById('RunScript');
const filePicked = document.getElementById('FilePicked');
const outputFileButton = document.getElementById('outputFile');
const outputFilePath = document.getElementById('outputFilePath');

outputFileButton.onclick = getOutputFolder;
loadFileButton.onclick = getObsidianFolder;
runScriptButton.onclick = runScript;

async function getObsidianFolder() {
    const directory_path = await window.electronAPI.openDirectory();
    console.log('Directory path:', directory_path);
    if (directory_path){
        
        filePicked.innerText = directory_path;
        console.log('Directory path:', typeof filePicked.innerText);
        loadFileButton.classList.add('is-success');
        loadFileButton.classList.remove('is-white');
        runScriptButton.classList.remove('is-warning');
        runScriptButton.classList.add('is-link');
    }
       else{
        loadFileButton.classList.add('is-danger');
        loadFileButton.classList.remove('is-white');
        loadFileButton.classList.remove('is-success');
    }

}

async function runScript() {
    //run checks
    if (outputFileButton.classList.contains('is-success') &&
        loadFileButton.classList.contains('is-success')){
        const inputfile = filePicked.innerText;
        const outputfile = outputFilePath.innerText;
        if (inputfile !== '' && outputfile !== ''){
            console.log('Running script with output folder:', outputfile);
            console.log('Running script with input folder:', inputfile);
            window.electronAPI.openDocumentWindow(inputfile, outputfile);
        } else {
            console.error('Input or output folder path is empty.');
        }
    }
    else{
        console.error('Output folder or input folder not selected.');
        runScriptButton.classList.add('is-danger');
        runScriptButton.classList.remove('is-link');
        runScriptButton.classList.remove('is-warning');
    }
    // setTimeout(() => {
    //     console.log('Opening document window'); 
    //     subwindow = window.open('http://127.0.0.1:8000/', '_blank', 'width=1220,height=600');
    // }, 3000);



    
    //window.electronAPI.openDocumentWindow(input_path, output_path);
}


async function getOutputFolder() {
    const directory_path = await window.electronAPI.openDirectory();
    console.log('Directory path:', directory_path);
    if (directory_path){
        outputFilePath.innerText = directory_path;
        outputFileButton.classList.add('is-success');
        outputFileButton.classList.remove('is-white');
        outputFileButton.classList.remove('is-danger');
    }
    else{
        outputFileButton.classList.add('is-danger');
        outputFileButton.classList.remove('is-white');
        outputFileButton.classList.remove('is-success');
    }

}  