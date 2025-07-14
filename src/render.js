
const loadFileButton = document.getElementById('OpenFolder');
const runScriptButton = document.getElementById('RunScript');
const filePicked = document.getElementById('FolderPicked');
const outputFileButton = document.getElementById('outputFile');
const outputFilePath = document.getElementById('outputFilePath');
const loadmdFile = document.getElementById('OpenFile');
//loading the logo
const logoloader = document.getElementById('logoPathButton');
const logoPath = document.getElementById('logoPathDisplay');
//getting the website name
const websiteName = document.getElementById('WebsiteNameInput');
var button = 'folder';


outputFileButton.onclick = getOutputFolder;
loadFileButton.onclick = getObsidianFolder;
loadmdFile.onclick = getObsidianFile;
runScriptButton.onclick = runScript;


async function getObsidianFolder() {
    const directory_path = await window.electronAPI.openDirectory();
    console.log('Directory path:', directory_path);
    if (directory_path){
        
        filePicked.innerText = directory_path;
        console.log('Directory path:', typeof filePicked.innerText);
        loadFileButton.classList.add('is-success');
        loadFileButton.classList.remove('is-white');
        loadFileButton.classList.remove('is-warning');
        runScriptButton.classList.remove('is-warning');
        runScriptButton.classList.add('is-link');
        //load md file button
        loadmdFile.classList.add('is-white');
        loadmdFile.classList.remove('is-warning');
        loadmdFile.classList.remove('is-success');

    }
       else{
        loadFileButton.classList.add('is-warning');
        loadFileButton.classList.remove('is-white');
        loadFileButton.classList.remove('is-success');
        loadmdFile.classList.add('is-warning');
        loadmdFile.classList.remove('is-white');
        loadmdFile.classList.remove('is-success');
        runScriptButton.classList.add('is-warning');
        runScriptButton.classList.remove('is-link');
    }

}


async function getObsidianFile() {
    const directory_path = await window.electronAPI.openFile();
    console.log('Directory path:', directory_path);
    if (directory_path){
        filePicked.innerText = directory_path;
        loadFileButton.classList.add('is-white');
        loadFileButton.classList.remove('is-warning');
        loadFileButton.classList.remove('is-info');
        loadFileButton.classList.remove('is-success');
        //runscript button
        runScriptButton.classList.remove('is-warning');
        runScriptButton.classList.add('is-link');
        //add to file picked
        loadmdFile.classList.add('is-success');
        loadmdFile.classList.remove('is-white');
        loadmdFile.classList.remove('is-warning');
    }   
    else{
        loadmdFile.classList.add('is-warning');
        loadmdFile.classList.remove('is-white');
        loadmdFile.classList.remove('is-success');
        runScriptButton.classList.add('is-warning');
        runScriptButton.classList.remove('is-link');
        loadFileButton.classList.add('is-warning');
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
    else if (outputFileButton.classList.contains('is-success') && 
            loadmdFile.classList.contains('is-success')){
            const inputfile = filePicked.innerText;
            const outputfile = outputFilePath.innerText;
            if (inputfile !== '' && outputfile !== ''){
                console.log('Running script with output folder:', outputfile);
            console.log('Running script with input folder:', inputfile);
            window.electronAPI.openDocumentFile(inputfile, outputfile);
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