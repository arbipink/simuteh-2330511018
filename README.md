# SIMUTEH: Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra

Evaluasi Hasil Belajar Praktikum Pertemuan 1–4  
Mata Kuliah: Computer Vision  
Program Studi Teknik Informatika, Fakultas Sains dan Teknologi  
Universitas Muhammadiyah Sukabumi (UMMI)

---

## 1. Identitas Mahasiswa
- **Nama:** Arbinda Rizki Muhammad
- **NIM:** 2330511018
- **Kelas:** A
- **SEED Dataset:** `2330511018` (4 digit terakhir NIM: `1018`)

---

## 2. Struktur Repositori
```text
simuteh-2330511018/
|-- data/
|   `-- sintetis/                  # Citra sintetis, mask, label.csv (SEED: 2330511018)
|-- notebook/
|   |-- B1_lingkungan.ipynb        # Uji pustaka, larik piksel, semantic gap
|   |-- B2_citra_warna.ipynb       # Ruang warna (BGR, Gray, HSV), KB kanal, sampling
|   |-- B3_histogram.ipynb         # Statistik histogram 5 kondisi, perbaikan CLAHE
|   |-- B4_penapisan.ipynb         # Konvolusi manual, penapis derau, PSNR, preservasi
|   `-- B5_praproses.ipynb         # Rangkaian integrasi praproses dan evaluasi KB
|-- src/
|   |-- buat_dataset_sintetis.py   # Generator dataset daun teh sintetis
|   |-- utils_cv.py                # Fungsi bantu baca, tampil, kontras_bercak, statistik
|   `-- praproses.py               # Rangkaian praproses SIMUTEH terpadu
|-- hasil/                         # Gambar grafik, artefak diagram, tabel csv, JSON
|-- laporan/                       # Laporan evaluasi Markdown
|-- requirements.txt               # Daftar pustaka dan versi lingkungan
`-- README.md                      # Panduan reprodusibilitas proyek
```

---

## 3. Persiapan Lingkungan dan Cara Menjalankan

### A. Instalasi Dependensi
Pastikan menggunakan Python 3.10 atau versi yang lebih baru:
```bash
pip install -r requirements.txt
```

### B. Membangkitkan Dataset Sintetis
Jalankan skrip generator dataset dari direktori utama:
```bash
python src/buat_dataset_sintetis.py
```
Skrip akan menghasilkan 60 citra sintetis pada direktori `data/sintetis/`:
- 20 citra kelas sehat (`teh_001.png` - `teh_020.png`)
- 20 citra kelas bercak ringan (`teh_021.png` - `teh_040.png`)
- 20 citra kelas bercak berat (`teh_041.png` - `teh_060.png`)
Dengan 5 kondisi pencahayaan berulang: Normal, Gelap, Terang, Kontras Rendah, dan Bayangan.

### C. Menjalankan Notebook Eksperimen
Jalankan Jupyter Notebook dan buka berkas di folder `notebook/` secara berurutan:
1. `B1_lingkungan.ipynb`
2. `B2_citra_warna.ipynb`
3. `B3_histogram.ipynb`
4. `B4_penapisan.ipynb`
5. `B5_praproses.ipynb`

Seluruh notebook telah diverifikasi dapat dijalankan dari awal hingga akhir (*Restart & Run All*) tanpa galat.

---

## 4. Ringkasan Temuan Teknis Utama
1. **Kanal Warna Pemisah Terbaik:**
   - **Kanal Red ($R$)** secara konsisten memberikan Kontras Bercak (KB) tertinggi dengan rerata **7.68** di semua kondisi cahaya (jauh melampaui Gray 3.40 dan Green 0.72). Hal ini selaras dengan sifat biofisik di mana klorofil daun sehat menyerap spektrum merah, sementara lesi cacar daun memantulkannya.
2. **Pemerataan Iluminasi Adaptif:**
   - Metode **CLAHE pada kanal Value ($V$)** ruang warna HSV mendongkrak kontras bercak pada kondisi bayangan sebesar **+74.5%** tanpa menyebabkan distorsi warna (*color shift*).
3. **Peredaman Derau dan Preservasi Lesi Kecil:**
   - **Penapis Median $3 \times 3$** memberikan kombinasi optimal: komputasi sangat cepat ($0.11\text{ ms}$), kebal terhadap derau impulsif debu perkebunan ($PSNR = 48.09\text{ dB}$), dan mempertahankan integritas bercak kecil ($dI = 28.82$).
4. **Evaluasi Modul Praproses Terpadu:**
   - Rangkaian modul `praproses.py` meningkatkan nilai Kontras Bercak (KB) rata-rata pada mayoritas kondisi cahaya tanpa memunculkan bercak palsu (*false positive*) pada 20 citra kontrol kelas sehat.

---

## 5. Berkas Laporan
Laporan lengkap praktikum evaluasi tersedia dalam format Markdown di:
`laporan/Laporan_EvalP1-P4_2330511018_Arbinda Rizki Muhammad.md`
