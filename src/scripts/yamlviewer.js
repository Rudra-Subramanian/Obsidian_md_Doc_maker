const text_area = document.getElementById('yamlTextArea');
const saveButton = document.getElementById('saveButton');

saveButton.onclick = SaveFile;

loadYamlFile();

// setTimeout(() => {
//      console.log('Opening document window'); 
//      subwindow = window.open('http://127.0.0.1:8000/', '_blank', 'width=1220,height=600');
     
//  }, 3000);

async function loadYamlFile() {
    const yaml_text = await window.electronAPI.openYaml();
    text_area.value = yaml_text;
    console.log('YAML file loaded:', yaml_text);
    if (text_area.value === 'undefined' || text_area.value === '') {
        console.error('YAML file is empty or not loaded properly.');
        setTimeout(() => {
            loadYamlFile();
        }, 1000);

    }
    else {
        console.log('YAML file loaded successfully.');
        text_area.classList.remove('is-loading');
        text_area.classList.remove('is-warning');
        text_area.removeAttribute('disabled');
        console.log('Opening document window'); 
        subwindow = window.open('http://127.0.0.1:8000/', '_blank', 'width=1220,height=600');
     
    }
}


async function SaveFile() {
    const yamlContent = text_area.value;
    console.log('Saving YAML content:', yamlContent);
    window.electronAPI.saveYaml(yamlContent);
}