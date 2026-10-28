const {app,BrowserWindow,shell}=require("electron");
const path=require("node:path");
function createWindow(){
 const win=new BrowserWindow({width:1280,height:850,minWidth:760,minHeight:560,title:"NAVARIS Business Intelligence OS",backgroundColor:"#050505",autoHideMenuBar:true,webPreferences:{contextIsolation:true,nodeIntegration:false,sandbox:true}});
 win.webContents.setWindowOpenHandler(({url})=>{if(url.startsWith("mailto:")||url.startsWith("https://"))shell.openExternal(url);return {action:"deny"};});
 win.loadFile(path.join(__dirname,"index.html"));
}
app.whenReady().then(()=>{createWindow();app.on("activate",()=>{if(BrowserWindow.getAllWindows().length===0)createWindow();});});
app.on("window-all-closed",()=>{if(process.platform!=="darwin")app.quit();});
