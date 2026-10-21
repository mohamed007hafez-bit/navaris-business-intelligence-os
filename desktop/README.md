# NAVARIS Local Desktop App (Sprint 2)

This Electron shell packages the repository's root `index.html` as a Windows desktop app. It does not require GitHub Pages at runtime after the interface has been packaged.

## Build on Windows
1. Install Node.js LTS (includes npm).
2. Clone the repository and open PowerShell in the repository root.
3. Run:
   ```powershell
   cd desktop
   npm install
   npm start
   ```
   This copies the current root `index.html` into `desktop/web/` and launches the desktop shell.
4. Build installers:
   ```powershell
   npm run dist:win
   ```
5. Output is in `desktop/dist/`: NSIS installer and portable EXE.

## Security and scope
- Renderer has `nodeIntegration: false`, `contextIsolation: true`, and sandboxing enabled.
- External HTTPS and mailto links open in the system browser/mail handler.
- This is a local UI wrapper. It does not itself add an AI backend, cloud sync, database, or authentication. Do not place API keys in renderer code.
- Validate calculators and any file export in the packaged app before production use.
