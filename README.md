# 🎓 Chatbot Akademik UPGRIS Berbasis Finite State Machine

> Simulasi Finite State Machine (FSM) untuk Layanan Informasi Akademik Universitas PGRI Semarang

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit&logoColor=white)
![FSM](https://img.shields.io/badge/Model-Finite%20State%20Machine-purple)
![TBO](https://img.shields.io/badge/Mata%20Kuliah-Teori%20Bahasa%20%26%20Otomata-green)

---

## Deskripsi

Chatbot Akademik UPGRIS adalah aplikasi chatbot berbasis **Finite State Machine (FSM)** yang dibuat menggunakan **Python** dan **Streamlit**. Chatbot ini mampu menjawab pertanyaan seputar informasi akademik di **Universitas PGRI Semarang** menggunakan pendekatan *rule-based keyword matching*.

Aplikasi ini **tidak menggunakan API AI eksternal** (seperti OpenAI, Gemini, HuggingFace, LangChain) — murni menggunakan logika FSM sesuai konsep Teori Bahasa dan Otomata.

---

## Tujuan Project

1. Mengimplementasikan konsep **Finite State Machine (FSM)** dari mata kuliah **Teori Bahasa dan Otomata**.
2. Membangun chatbot yang mampu menjawab pertanyaan akademik menggunakan FSM.
3. Menampilkan visualisasi FSM: diagram state, tabel transisi, riwayat transisi.
4. Menunjukkan bahwa FSM dapat diaplikasikan pada sistem percakapan sederhana.

---

##  Konsep Teori Bahasa dan Otomata

### Definisi Formal FSM

```
M = (Q, Σ, δ, q₀, F)
```

| Komponen | Keterangan |
|----------|-----------|
| **Q** | Himpunan state (24 state) |
| **Σ** | Input berupa teks pertanyaan pengguna |
| **δ** | Fungsi transisi berdasarkan intent yang terdeteksi dari keyword |
| **q₀** | START (state awal) |
| **F** | {IDLE, END} (himpunan state akhir) |

### Daftar State (Q)

| No | State | Keterangan |
|----|-------|-----------|
| 1 | START | State awal sistem |
| 2 | IDLE | State siap menerima input (accepting) |
| 3 | DETECT_INTENT | State mendeteksi intent dari input |
| 4 | PROFIL_UPGRIS | Menampilkan profil UPGRIS |
| 5 | PROFIL_INFORMATIKA | Menampilkan profil Informatika |
| 6 | FAKULTAS_INFO | Menampilkan info fakultas |
| 7 | PRODI_INFO | Menampilkan info prodi |
| 8 | DOSEN_INFO | Menampilkan info dosen |
| 9 | KURIKULUM_INFO | Menampilkan info kurikulum |
| 10 | PMB_INFO | Menampilkan info PMB |
| 11 | BIAYA_INFO | Menampilkan info biaya |
| 12 | BEASISWA_INFO | Menampilkan info beasiswa |
| 13 | MBKM_INFO | Menampilkan info MBKM |
| 14 | KRS_INFO | Menampilkan info KRS |
| 15 | KHS_INFO | Menampilkan info KHS |
| 16 | IPK_INFO | Menampilkan info IPK |
| 17 | JADWAL_INFO | Menampilkan info jadwal |
| 18 | SKRIPSI_INFO | Menampilkan info skripsi |
| 19 | WISUDA_INFO | Menampilkan info wisuda |
| 20 | LAYANAN_SURAT | Menampilkan info layanan surat |
| 21 | PENGADUAN_INFO | Menampilkan info pengaduan |
| 22 | FAQ_INFO | Menampilkan FAQ |
| 23 | ERROR | Fallback jika input tidak dikenali |
| 24 | END | State akhir sistem |

### Tabel Transisi (δ)

| State Awal | Input | State Tujuan | Output |
|-----------|-------|-------------|--------|
| START | Aplikasi dijalankan | IDLE | Sapaan awal chatbot |
| IDLE | User mengirim pertanyaan | DETECT_INTENT | Sistem memproses input |
| DETECT_INTENT | Keyword profil UPGRIS | PROFIL_UPGRIS | Info profil UPGRIS |
| DETECT_INTENT | Keyword informatika | PROFIL_INFORMATIKA | Info Informatika |
| DETECT_INTENT | Keyword fakultas | FAKULTAS_INFO | Info fakultas |
| DETECT_INTENT | Keyword prodi | PRODI_INFO | Info prodi |
| DETECT_INTENT | Keyword dosen | DOSEN_INFO | Info dosen |
| DETECT_INTENT | Keyword kurikulum | KURIKULUM_INFO | Info kurikulum |
| DETECT_INTENT | Keyword PMB | PMB_INFO | Info PMB |
| DETECT_INTENT | Keyword biaya | BIAYA_INFO | Info biaya |
| DETECT_INTENT | Keyword beasiswa | BEASISWA_INFO | Info beasiswa |
| DETECT_INTENT | Keyword MBKM | MBKM_INFO | Info MBKM |
| DETECT_INTENT | Keyword KRS | KRS_INFO | Info KRS |
| DETECT_INTENT | Keyword KHS | KHS_INFO | Info KHS |
| DETECT_INTENT | Keyword IPK | IPK_INFO | Info IPK |
| DETECT_INTENT | Keyword jadwal | JADWAL_INFO | Info jadwal |
| DETECT_INTENT | Keyword skripsi | SKRIPSI_INFO | Info skripsi |
| DETECT_INTENT | Keyword wisuda | WISUDA_INFO | Info wisuda |
| DETECT_INTENT | Keyword surat | LAYANAN_SURAT | Info layanan surat |
| DETECT_INTENT | Keyword pengaduan | PENGADUAN_INFO | Info pengaduan |
| DETECT_INTENT | Keyword FAQ | FAQ_INFO | Info FAQ |
| DETECT_INTENT | Keyword tidak dikenali | ERROR | Fallback & rekomendasi |
| STATE_INFO | Response selesai | IDLE | Siap menerima input baru |
| ERROR | Fallback selesai | IDLE | Siap menerima input baru |

### Diagram FSM (Teks)

```
START ──→ IDLE ──→ DETECT_INTENT ──→ STATE_INFO ──→ IDLE
                         │
                         ├──→ PROFIL_UPGRIS ──→ IDLE
                         ├──→ PROFIL_INFORMATIKA ──→ IDLE
                         ├──→ FAKULTAS_INFO ──→ IDLE
                         ├──→ PRODI_INFO ──→ IDLE
                         ├──→ DOSEN_INFO ──→ IDLE
                         ├──→ KURIKULUM_INFO ──→ IDLE
                         ├──→ PMB_INFO ──→ IDLE
                         ├──→ BIAYA_INFO ──→ IDLE
                         ├──→ BEASISWA_INFO ──→ IDLE
                         ├──→ MBKM_INFO ──→ IDLE
                         ├──→ KRS_INFO ──→ IDLE
                         ├──→ KHS_INFO ──→ IDLE
                         ├──→ IPK_INFO ──→ IDLE
                         ├──→ JADWAL_INFO ──→ IDLE
                         ├──→ SKRIPSI_INFO ──→ IDLE
                         ├──→ WISUDA_INFO ──→ IDLE
                         ├──→ LAYANAN_SURAT ──→ IDLE
                         ├──→ PENGADUAN_INFO ──→ IDLE
                         ├──→ FAQ_INFO ──→ IDLE
                         └──→ ERROR ──→ IDLE
```

---

##  Struktur Folder

```
UPGRIS_Academic_Assistant/
│
├── app.py                  # Frontend Streamlit
├── FSM.py                  # Finite State Machine (State, AcademicFSM)
├── engine.py               # Deteksi intent & response generator
├── utils.py                # Fungsi utilitas
├── requirements.txt        # Dependensi Python
├── README.md               # Dokumentasi project
│
├── data/                   # Data akademik (JSON)
│   ├── profil_upgris.json
│   ├── profil_informatika.json
│   ├── fakultas.json
│   ├── prodi.json
│   ├── dosen.json
│   ├── kurikulum.json
│   ├── pmb.json
│   ├── akademik.json
│   ├── beasiswa.json
│   ├── mbkm.json
│   └── faq.json
│
├── assets/                 # Asset gambar
│   └── logo_upgris.png     # Logo UPGRIS (opsional)
│
└── .streamlit/             # Konfigurasi Streamlit
    └── config.toml
```

---

##  Cara Instalasi & Menjalankan

### 1. Clone / Download Project

```bash
cd UPGRIS_Academic_Assistant
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# atau
venv\Scripts\activate           # Windows
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

---

##  Contoh Pertanyaan

| No | Pertanyaan |
|----|-----------|
| 1 | Apa itu UPGRIS? |
| 2 | Jelaskan Prodi Informatika |
| 3 | Siapa dosen Informatika? |
| 4 | Apa saja kurikulum Informatika? |
| 5 | Bagaimana cara daftar PMB? |
| 6 | Berapa biaya kuliah? |
| 7 | Apa saja beasiswa di UPGRIS? |
| 8 | Apa itu MBKM? |
| 9 | Apa itu KRS? |
| 10 | Bagaimana cara melihat KHS? |
| 11 | Apa itu IPK? |
| 12 | Bagaimana jadwal kuliah? |
| 13 | Bagaimana proses skripsi? |
| 14 | Apa syarat wisuda? |
| 15 | Bagaimana pengajuan surat? |
| 16 | Bagaimana cara pengaduan? |
| 17 | Daftar fakultas di UPGRIS? |
| 18 | FAQ |

---

##  Tabel Pengujian

| No | Input | Intent | State Tujuan | Status |
|----|-------|--------|-------------|--------|
| 1 | Apa itu UPGRIS? | profil_upgris | PROFIL_UPGRIS | ✅ Accepted |
| 2 | Jelaskan Prodi Informatika | profil_informatika | PROFIL_INFORMATIKA | ✅ Accepted |
| 3 | Siapa dosen Informatika? | dosen | DOSEN_INFO | ✅ Accepted |
| 4 | Apa saja kurikulum? | kurikulum | KURIKULUM_INFO | ✅ Accepted |
| 5 | Cara daftar PMB | pmb | PMB_INFO | ✅ Accepted |
| 6 | Berapa biaya kuliah? | biaya | BIAYA_INFO | ✅ Accepted |
| 7 | Info beasiswa | beasiswa | BEASISWA_INFO | ✅ Accepted |
| 8 | Apa itu MBKM? | mbkm | MBKM_INFO | ✅ Accepted |
| 9 | Apa itu KRS? | krs | KRS_INFO | ✅ Accepted |
| 10 | Bagaimana KHS? | khs | KHS_INFO | ✅ Accepted |
| 11 | IPK saya berapa? | ipk | IPK_INFO | ✅ Accepted |
| 12 | Jadwal kuliah | jadwal | JADWAL_INFO | ✅ Accepted |
| 13 | Proses skripsi | skripsi | SKRIPSI_INFO | ✅ Accepted |
| 14 | Syarat wisuda | wisuda | WISUDA_INFO | ✅ Accepted |
| 15 | Pengajuan surat | layanan_surat | LAYANAN_SURAT | ✅ Accepted |
| 16 | Cara pengaduan | pengaduan | PENGADUAN_INFO | ✅ Accepted |
| 17 | Daftar fakultas | fakultas | FAKULTAS_INFO | ✅ Accepted |
| 18 | FAQ | faq | FAQ_INFO | ✅ Accepted |
| 19 | xyz123 | unknown | ERROR | ❌ Fallback |
| 20 | Hello world | unknown | ERROR | ❌ Fallback |

---

## Fitur Aplikasi

- ✅ Chatbot akademik berbasis FSM
- ✅ Deteksi intent menggunakan keyword matching
- ✅ Visualisasi diagram FSM (Graphviz)
- ✅ Tabel transisi FSM lengkap
- ✅ Riwayat transisi real-time
- ✅ Detail proses FSM setiap percakapan
- ✅ Badge Accepted / Fallback
- ✅ Status FSM di sidebar (current state, last intent, total transisi)
- ✅ Quick question buttons
- ✅ Reset chatbot
- ✅ Export riwayat transisi ke CSV
- ✅ Dataset akademik viewer
- ✅ Penjelasan teori FSM
- ✅ Tampilan modern dan responsive
- ✅ Data terpisah di file JSON

---

## Kesimpulan

Project ini membuktikan bahwa **Finite State Machine (FSM)** — salah satu konsep fundamental dalam **Teori Bahasa dan Otomata** — dapat digunakan untuk membangun chatbot sederhana berbasis aturan (*rule-based*). Setiap pertanyaan pengguna diperlakukan sebagai input yang memicu transisi state, dan setiap state menghasilkan output berupa informasi akademik yang relevan.

Meskipun sederhana dibandingkan chatbot berbasis AI/LLM, pendekatan FSM ini memiliki keunggulan:
- **Transparan** — alur kerja dapat divisualisasikan dan dipahami sepenuhnya
- **Deterministik** — output selalu konsisten untuk input yang sama
- **Ringan** — tidak memerlukan GPU, API, atau koneksi internet
- **Edukatif** — mendemonstrasikan konsep otomata secara praktis

---

## Teknologi

| Teknologi | Fungsi |
|-----------|--------|
| Python 3.9+ | Bahasa pemrograman utama |
| Streamlit | Framework web UI |
| Pandas | Manipulasi data tabel |
| Graphviz | Visualisasi diagram FSM |

---

## Lisensi

Project ini dibuat untuk keperluan akademik mata kuliah **Teori Bahasa dan Otomata** — Program Studi Informatika, Universitas PGRI Semarang.
- Bintang Bradhiena Surya 23670058
- Ahmad Najmudin Afifi 23670078
- Mashfa Kamal Faza 23670105

---

*Dibuat dengan ❤️ menggunakan Python & Streamlit*
# AcademicUpgris-Chatbot-FSM
