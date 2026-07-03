const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// Folder gambar utama di proyek Anda
const inputFolder = path.join(__dirname, 'images');

// Fungsi rekursif untuk membaca folder dan subfolder
function processDirectory(directory) {
    if (!fs.existsSync(directory)) {
        console.error(`Folder ${directory} tidak ditemukan!`);
        return;
    }

    fs.readdir(directory, { withFileTypes: true }, (err, dirents) => {
        if (err) return console.error('Gagal membaca direktori', directory, err);

        dirents.forEach(dirent => {
            const fullPath = path.join(directory, dirent.name);
            
            if (dirent.isDirectory()) {
                // Jika itu folder, panggil fungsi ini lagi secara rekursif
                processDirectory(fullPath);
            } else {
                // Jika itu file, periksa ekstensinya
                const ext = path.extname(dirent.name).toLowerCase();
                
                if (['.jpg', '.jpeg', '.png', '.webp'].includes(ext)) {
                    // Mengubah nama ekstensi menjadi .avif dan menyimpannya di folder yang sama
                    const outputPath = path.join(directory, dirent.name.replace(new RegExp(`${ext}$`), '.avif'));

                    // (Opsional) Lewati jika file avif sudah ada agar tidak mengonversi ulang
                    if (fs.existsSync(outputPath)) {
                        console.log(`Lewati: ${dirent.name.replace(ext, '.avif')} sudah ada.`);
                        return;
                    }

                    sharp(fullPath)
                        .resize({ width: 1200, withoutEnlargement: true }) // Batasi lebar max 1200px agar tidak pecah
                        .avif({ quality: 75 }) // Konversi ke format AVIF dengan kualitas 75 (sweet spot)
                        .toFile(outputPath)
                        .then(() => console.log(`Berhasil: ${dirent.name} -> AVIF`))
                        .catch(err => console.error(`Gagal memproses ${dirent.name}:`, err));
                }
            }
        });
    });
}

console.log(`Memulai proses konversi AVIF pada folder: ${inputFolder}`);
processDirectory(inputFolder);
