const { contextBridge } = require('electron');
contextBridge.exposeInMainWorld('navarisDesktop', Object.freeze({
  version: '0.3.0',
  mode: 'offline-desktop-prototype',
  storage: 'renderer-local-only'
}));
