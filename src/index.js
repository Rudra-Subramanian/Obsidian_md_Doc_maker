const { app, BrowserWindow, ipcMain, dialog, utilityProcess } = require('electron');
const path = require('node:path');
const { spawn } = require("child_process");
const fs = require ('fs');

newprocess = null;
pythonprocess = null;
// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
    },
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  mainWindow.setMenuBarVisibility(false);

  // Open the DevTools.
  //mainWindow.webContents.openDevTools();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();

  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
  
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (pythonprocess){
    pythonprocess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

ipcMain.handle('dialog:openDirectory', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openDirectory', 'createDirectory'],
    title: 'Select a directory',
    buttonLabel: 'Select Directory',
  });
  if (result.canceled) {
    return null;
  } else {
    return result.filePaths[0];
  }
});

ipcMain.handle('dialog:openFile', async () => {
  const result = await dialog.showOpenDialog({
    properties: ['openFile'],
    title: 'Select a file',
    buttonLabel: 'Select File',
    filters: [
      { name: 'Markdown Files', extensions: ['md'] }]
  });
  if (result.canceled) {
    return null;
  } else {
    return result.filePaths[0];
  }
});

//Creating the html file by runnging the python script

ipcMain.on('window:create_folder', async (event, input, output) => {
  if (pythonprocess){
    pythonprocess.kill();
  }

  console.log('Input folder:', input);
  console.log('Output folder:',output);
  output_folder = output;
  pythonprocess = spawn('python3', [
    path.join(__dirname, 'MdtoHtmlconverter.py'),
    '--root_folder', input,
    '--output_folder', output,
    '--site_name', 'test_site',
    '--site_url', 'http://127.0.0.1:8000/'
  ]);
  pythonprocess.on('error', (error) => {
    console.error('Error starting Python process:', error);
    pythonprocess.kill();
  });

    // You can pass the URL to the new window if needed
  goToYaml();
});

ipcMain.on('window:create_file', async (event, input, output) => {
  if (pythonprocess){
    pythonprocess.kill();
  }

  console.log('Input folder:', input);
  console.log('Output folder:',output);
  output_folder = output;
  pythonprocess = spawn('python3', [
    path.join(__dirname, 'MdtoHtmlconverter.py'),
    '--root_md', input,
    '--output_folder', output,
    '--site_name', 'test_site',
    '--site_url', 'http://127.0.0.1:8000/'
  ]);
  pythonprocess.on('error', (error) => {
    console.error('Error starting Python process:', error);
    pythonprocess.kill();
  });

    // You can pass the URL to the new window if needed
  goToYaml();
});




// Switching view to the yamlview.html

const goToYaml = () => {
  console.log('Going to YAML view');
  setTimeout(() => {
    mainWindow.loadFile(path.join(__dirname, 'yamlview.html'));
  }, 3000);
  //mainWindow.loadFile(path.join(__dirname, 'yamlview.html'));
  // viewer_window = new BrowserWindow({
  //   width: 500,
  //   height: 500,
  //   webPreferences: {
  //     preload: path.join(__dirname, 'preload.js'),
  //     nodeIntegration: true,
      
  //   },
  // });
  // viewer_window.loadFile('http://127.0.0.1:8000/');
}

//Handles opening the yaml and getting the output text


ipcMain.handle('dialog:openYaml', async () => {
  output_path = path.join(output_folder, 'mkdocs.yml');
  //console.log('Output path for yaml:', output_path);
  try {
    const output_text = await fs.promises.readFile(output_path, 'utf8');
    return output_text;
  } catch (error) {
    console.error('Error reading YAML file:', error);
    return '';
  }
});

// Handling Saving the YAML file when editing


ipcMain.on('dialog:saveYaml', async (event, yamlContent) => {
  output_path = path.join(output_folder, 'mkdocs.yml');
  console.log('Saving YAML content to:', output_path);
  try {
    await fs.promises.writeFile(output_path, yamlContent, 'utf8');
    console.log('YAML file saved successfully.');
  } catch (error) {
    console.error('Error saving YAML file:', error);
  }
});




