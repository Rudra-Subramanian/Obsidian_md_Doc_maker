const {ContextBridge, ipcRenderer, contextBridge} = require('electron'); 



contextBridge.exposeInMainWorld('electronAPI', {
    openDirectory: () => ipcRenderer.invoke('dialog:openDirectory'),
    openDocumentWindow: (input, output) => ipcRenderer.send('window:create', input, output),
    openYaml: () => ipcRenderer.invoke('dialog:openYaml'),
    saveYaml: (yamlContent) => ipcRenderer.send('dialog:saveYaml', yamlContent),
});

