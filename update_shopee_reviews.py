"""
==========================================================
  SHOPEE REVIEW UPDATER - Nirfama
  Cara mudah mengupdate testimoni dari Shopee
==========================================================

CARA PAKAI:
  1. Buka produk Shopee Anda di browser biasa
  2. Scroll ke bagian "Penilaian Produk"  
  3. Salin komentar-komentar terbaik
  4. Jalankan script ini: python update_shopee_reviews.py
  5. Ikuti instruksi di layar untuk memasukkan ulasan

Script ini akan menghasilkan file reviews.json yang
otomatis ditampilkan di website landing page Anda.
"""

import json
import os
import sys

# Fix encoding untuk Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def load_existing_reviews(json_path):
    """Muat ulasan yang sudah ada."""
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_reviews(reviews, json_path):
    """Simpan ulasan ke file JSON."""
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)


def add_review_interactive(reviews):
    """Tambahkan ulasan baru secara interaktif."""
    print("\n--- Tambah Ulasan Baru ---")
    
    username = input("  Username pembeli (misal: agung_w): ").strip()
    if not username:
        print("  Username tidak boleh kosong!")
        return False
    
    comment = input("  Komentar pembeli: ").strip()
    if not comment:
        print("  Komentar tidak boleh kosong!")
        return False
    
    while True:
        stars_input = input("  Jumlah bintang (1-5, default 5): ").strip()
        if not stars_input:
            stars = 5
            break
        try:
            stars = int(stars_input)
            if 1 <= stars <= 5:
                break
            print("  Masukkan angka 1-5!")
        except ValueError:
            print("  Masukkan angka yang valid!")
    
    # Assign warna avatar secara bergantian
    colors = [
        ("bg-primary-container", "text-white"),
        ("bg-secondary-container", "text-on-secondary-container"),
        ("bg-tertiary-container", "text-on-tertiary-container"),
    ]
    color_idx = len(reviews) % len(colors)
    
    review = {
        "username": username,
        "stars": stars,
        "comment": comment,
        "avatar_bg": colors[color_idx][0],
        "avatar_text": colors[color_idx][1],
    }
    
    reviews.append(review)
    print(f"\n  [OK] Ulasan dari @{username} berhasil ditambahkan!")
    return True


def show_reviews(reviews):
    """Tampilkan semua ulasan yang sudah ada."""
    if not reviews:
        print("\n  Belum ada ulasan tersimpan.")
        return
    
    print(f"\n--- Daftar Ulasan ({len(reviews)} total) ---")
    for i, r in enumerate(reviews, 1):
        stars_str = "*" * r.get("stars", 5)
        comment_preview = r["comment"][:70] + "..." if len(r["comment"]) > 70 else r["comment"]
        print(f"  {i}. [{stars_str}] @{r['username']}: \"{comment_preview}\"")


def delete_review(reviews):
    """Hapus ulasan berdasarkan nomor."""
    show_reviews(reviews)
    if not reviews:
        return
    
    try:
        num = int(input("\n  Nomor ulasan yang ingin dihapus (0 = batal): ").strip())
        if num == 0:
            return
        if 1 <= num <= len(reviews):
            removed = reviews.pop(num - 1)
            print(f"  [OK] Ulasan dari @{removed['username']} berhasil dihapus!")
        else:
            print("  Nomor tidak valid!")
    except ValueError:
        print("  Masukkan angka yang valid!")


def bulk_add_reviews(reviews):
    """Tambahkan beberapa ulasan sekaligus dengan format cepat."""
    print("\n--- Tambah Ulasan Cepat (Bulk) ---")
    print("  Masukkan ulasan dengan format: username | bintang | komentar")
    print("  Contoh: agung_w | 5 | Pupuk KCL nya sangat bagus, tanaman jadi subur!")
    print("  Ketik 'selesai' untuk berhenti.\n")
    
    colors = [
        ("bg-primary-container", "text-white"),
        ("bg-secondary-container", "text-on-secondary-container"),
        ("bg-tertiary-container", "text-on-tertiary-container"),
    ]
    
    count = 0
    while True:
        line = input("  > ").strip()
        if line.lower() in ['selesai', 'done', 'exit', 'quit', '']:
            break
        
        parts = line.split('|')
        if len(parts) < 3:
            print("    Format salah! Gunakan: username | bintang | komentar")
            continue
        
        username = parts[0].strip()
        try:
            stars = int(parts[1].strip())
            stars = max(1, min(5, stars))
        except ValueError:
            stars = 5
        comment = '|'.join(parts[2:]).strip()  # Gabungkan kembali jika komentar mengandung |
        
        if not username or not comment:
            print("    Username dan komentar tidak boleh kosong!")
            continue
        
        color_idx = len(reviews) % len(colors)
        reviews.append({
            "username": username,
            "stars": stars,
            "comment": comment,
            "avatar_bg": colors[color_idx][0],
            "avatar_text": colors[color_idx][1],
        })
        count += 1
        print(f"    [OK] @{username} ditambahkan!")
    
    print(f"\n  {count} ulasan baru berhasil ditambahkan!")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "reviews.json")
    
    print("=" * 56)
    print("  SHOPEE REVIEW UPDATER - Nirfama Landing Page")
    print("=" * 56)
    print(f"\n  File reviews.json: {json_path}")
    
    reviews = load_existing_reviews(json_path)
    print(f"  Ulasan tersimpan: {len(reviews)} ulasan")
    
    while True:
        print("\n--- Menu ---")
        print("  1. Lihat semua ulasan")
        print("  2. Tambah ulasan baru (satu per satu)")
        print("  3. Tambah ulasan cepat (bulk / banyak sekaligus)")
        print("  4. Hapus ulasan")
        print("  5. Simpan & keluar")
        print("  0. Keluar tanpa menyimpan")
        
        choice = input("\n  Pilihan Anda: ").strip()
        
        if choice == '1':
            show_reviews(reviews)
        elif choice == '2':
            add_review_interactive(reviews)
        elif choice == '3':
            bulk_add_reviews(reviews)
        elif choice == '4':
            delete_review(reviews)
        elif choice == '5':
            save_reviews(reviews, json_path)
            print(f"\n  [OK] {len(reviews)} ulasan berhasil disimpan ke reviews.json!")
            print("  Website Anda akan otomatis menampilkan ulasan terbaru.")
            break
        elif choice == '0':
            print("\n  Keluar tanpa menyimpan perubahan.")
            break
        else:
            print("  Pilihan tidak valid!")
    
    print("\n  Selesai. Terima kasih!\n")


if __name__ == "__main__":
    main()
