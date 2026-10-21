const fs = require('node:fs');
const path = require('node:path');

const source = path.resolve(__dirname, '..', '..', 'index.html');
const targetDir = path.resolve(__dirname, '..', 'web');
const target = path.join(targetDir, 'index.html');

if (!fs.existsSync(source)) {
  console.error('Root index.html was not found. Run this from the repository checkout.');
  process.exit(1);
}
fs.mkdirSync(targetDir, { recursive: true });
fs.copyFileSync(source, target);
console.log('Prepared local NAVARIS interface:', target);
