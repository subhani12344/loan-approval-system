const fs = require('fs');
const path = require('path');

function copyFolderSync(from, to) {
    if (!fs.existsSync(to)) {
        fs.mkdirSync(to, { recursive: true });
    }
    fs.readdirSync(from).forEach(element => {
        const fromPath = path.join(from, element);
        const toPath = path.join(to, element);
        if (fs.lstatSync(fromPath).isDirectory()) {
            copyFolderSync(fromPath, toPath);
        } else {
            // Only copy if it doesn't end with .ts (TypeScript files are compiled by tsc)
            if (!element.endsWith('.ts')) {
                fs.copyFileSync(fromPath, toPath);
                console.log(`Copied: ${fromPath} -> ${toPath}`);
            }
        }
    });
}

const srcPublic = path.join(__dirname, 'src', 'public');
const distPublic = path.join(__dirname, 'dist', 'public');

console.log('Copying static frontend assets to dist/public...');
try {
    copyFolderSync(srcPublic, distPublic);
    console.log('Static assets copied successfully!');
} catch (err) {
    console.error('Error copying static assets:', err);
    process.exit(1);
}
