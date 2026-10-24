# NAVARIS Intelligence OS — Desktop shell v2.0

## Requirements
Node.js 18+ and npm. Native build prerequisites may be required for Electron and better-sqlite3.

## Install and run
```bash
cd navaris-exe
npm install
npm start
```

## Build installers
```bash
npm run build:win
npm run build:mac
npm run build:all
```

Build and validate Windows/macOS installers on the respective host runners. This commit contains source, not signed prebuilt installers.
