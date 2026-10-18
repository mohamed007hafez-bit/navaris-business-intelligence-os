# Tauri shell setup

The Tauri shell is intentionally not hand-written in this scaffold. Generate the platform-native files with the supported CLI after installing Rust and platform prerequisites:

```bash
cd cross-platform
npm install
npx tauri init
```

When prompted, use:
- App name: NAVARIS
- Window title: NAVARIS
- Web assets directory: ../dist (adjust based on CLI prompt and generated config)
- Dev server URL: http://localhost:5173
- Frontend dev command: npm run dev
- Frontend build command: npm run build

Review the generated `tauri.conf.json` and set `frontendDist` to `../dist` relative to `src-tauri`. Then run `npm run tauri:build`.

Do not add secrets or grant broad filesystem/shell permissions. Configure the minimum Tauri capabilities needed for each feature. Test installer behavior on a clean Windows VM before distribution.