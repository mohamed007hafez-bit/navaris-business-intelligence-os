const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('navarisDesktop', Object.freeze({
  isDesktop: true,
  platform: process.platform,
  appName: 'NAVARIS Business Intelligence OS'
}));
