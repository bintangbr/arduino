"""
engine.py - Mesin Deteksi Intent dan Response untuk Chatbot Akademik UPGRIS
============================================================================
Modul ini bertugas:
  1. Preprocessing teks input pengguna
  2. Mendeteksi intent berdasarkan keyword matching
  3. Memuat data dari file JSON
  4. Menghasilkan response sesuai intent
"""

import json
import re
import string
from pathlib import Path
from typing import Optional


# ============================================================
# Path ke folder data
# ============================================================
DATA_DIR = Path(__file__).parent / "data"


# ============================================================
# 1. Preprocessing Teks
# ============================================================
def preprocess_text(text: str) -> str:
    """
    Membersihkan teks input:
    - Lowercase
    - Hapus tanda baca
    - Normalisasi spasi
    """
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text)
    return text


# ============================================================
# 2. Load JSON
# ============================================================
def load_json(filename: str) -> dict:
    """Memuat file JSON dari folder data/. Mengembalikan dict kosong jika gagal."""
    filepath = DATA_DIR / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ============================================================
# 3. Helper: Cari prodi berdasarkan keyword dari input user
# ============================================================
def find_prodi_by_keyword(user_text: str) -> Optional[dict]:
    """
    Mencari prodi di akademik2.json berdasarkan keyword dari input user.
    Mengembalikan dict prodi + nama fakultas jika ditemukan, None jika tidak.
    """
    cleaned = preprocess_text(user_text)
    data = load_json("akademik2.json")
    if not data:
        return None

    # Mapping keyword -> id/nama prodi (keyword lebih spesifik didahulukan)
    prodi_keywords = [
        # Teknik & IT
        ("teknik informatika", ["TINFORMATIKA", "informatika"]),
        ("informatika", ["TINFORMATIKA", "informatika"]),
        ("teknik sipil", ["TSIPIL", "sipil"]),
        ("teknik elektro", ["TELEKTRO", "elektro"]),
        ("teknik mesin", ["TMESIN", "mesin"]),
        ("teknologi pangan", ["TPANGAN", "pangan"]),
        ("arsitektur", ["ARSITEKTUR", "arsitektur"]),
        # Pendidikan
        ("pgsd", ["PGSD", "pendidikan guru sekolah dasar"]),
        ("pgpaud", ["PGPAUD", "pendidikan guru pendidikan anak"]),
        ("bimbingan konseling", ["BK", "bimbingan"]),
        ("bk", ["BK"]),
        ("ppkn", ["PPKN", "pendidikan pancasila"]),
        ("pendidikan ekonomi", ["PEKONOMI"]),
        ("pjkr", ["PJKR", "pendidikan jasmani"]),
        ("pendidikan bahasa indonesia", ["PBSI"]),
        ("pbsi", ["PBSI"]),
        ("pendidikan bahasa inggris", ["PBI"]),
        ("pbi", ["PBI"]),
        ("pendidikan bahasa daerah", ["PBD", "bahasa jawa"]),
        ("pbd", ["PBD"]),
        ("pendidikan matematika", ["PMATEMATIKA"]),
        ("pendidikan biologi", ["PBIOLOGI"]),
        ("pendidikan fisika", ["PFISIKA"]),
        ("pendidikan teknologi informasi", ["PTI"]),
        ("pti", ["PTI"]),
        # Hukum & Bisnis
        ("hukum", ["HUKUM"]),
        ("manajemen", ["MANAJEMEN"]),
        ("akuntansi", ["AKUNTANSI"]),
        ("bisnis digital", ["BISNIS_DIGITAL"]),
        # Kedokteran
        ("kedokteran", ["KEDOKTERAN"]),
        ("profesi dokter", ["PROFESI_DOKTER"]),
        # Pascasarjana
        ("s2 manajemen pendidikan", ["S2MP"]),
        ("s2 pendidikan bahasa indonesia", ["S2PBI"]),
        ("s2 pendidikan matematika", ["S2PM"]),
        ("s2 pendidikan dasar", ["S2PDES"]),
        ("s2 pendidikan bahasa inggris", ["S2PENG"]),
        ("ppg", ["PPG", "profesi guru"]),
    ]

    matched_id = None
    for keyword, ids in prodi_keywords:
        if keyword in cleaned:
            matched_id = ids[0]
            break

    if not matched_id:
        return None

    # Cari di data
    for fak in data.get("fakultas", []):
        for prodi in fak.get("prodi", []):
            if prodi.get("id") == matched_id:
                return {
                    "prodi": prodi,
                    "fakultas": fak.get("nama", ""),
                    "singkatan_fak": fak.get("singkatan", ""),
                }

    return None


def format_rupiah(nominal: int) -> str:
    """Format angka ke Rupiah: 5406250 -> Rp 5.406.250"""
    return f"Rp {nominal:,.0f}".replace(",", ".")


# ============================================================
# 4. Keyword mapping untuk deteksi intent
# ============================================================
# Urutan penting: keyword yang lebih spesifik harus dicek lebih dulu
INTENT_KEYWORDS: list[tuple[str, list[str]]] = [
    ("profil_informatika", [
        "profil informatika", "prodi informatika", "teknik informatika",
        "tentang informatika", "informatika upgris",
    ]),
    ("profil_upgris", [
        "upgris", "universitas pgri semarang", "profil kampus",
        "tentang upgris", "alamat upgris", "visi misi upgris",
        "visi upgris", "misi upgris", "sejarah upgris",
        "rektor", "wakil rektor", "pimpinan upgris",
    ]),
    ("fakultas", [
        "fakultas", "daftar fakultas", "fakultas di upgris",
        "fti", "fakultas teknik dan informatika", "fakultas teknik",
    ]),
    ("dosen", [
        "dosen", "pengajar", "kaprodi", "sekretaris prodi",
        "laboran", "dosen informatika", "daftar dosen",
    ]),
    ("kurikulum", [
        "kurikulum", "mata kuliah", "matkul", "sks",
        "semester", "peminatan", "ai engineer", "web programmer",
    ]),
    ("pmb", [
        "pmb", "pendaftaran", "mahasiswa baru", "daftar kuliah",
        "jalur masuk", "registrasi", "cara daftar",
    ]),
    ("biaya", [
        "biaya", "ukt", "uang kuliah", "spp",
        "biaya kuliah", "pembayaran", "berapa biaya",
    ]),
    ("beasiswa", [
        "beasiswa", "kip", "kip kuliah", "bantuan kuliah",
        "bantuan biaya",
    ]),
    ("mbkm", [
        "mbkm", "kampus merdeka", "magang", "studi independen",
        "pertukaran mahasiswa", "kampus mengajar", "merdeka belajar",
    ]),
    ("skripsi", [
        "skripsi", "tugas akhir", "proposal skripsi",
        "sidang skripsi", "judul skripsi", "sidang",
    ]),
    ("pkl", [
        "pkl", "magang kampus", "praktik kerja lapangan",
        "praktek kerja",
    ]),
    ("kkn", [
        "kkn", "kuliah kerja nyata", "pengabdian masyarakat",
    ]),
    ("krs", [
        "krs", "kartu rencana studi", "ambil mata kuliah",
        "input krs", "isi krs", "pengisian krs",
    ]),
    ("khs", [
        "khs", "kartu hasil studi", "nilai semester",
        "hasil studi", "lihat nilai",
    ]),
    ("ipk", [
        "ipk", "indeks prestasi", "nilai akademik",
        "indeks prestasi kumulatif",
    ]),
    ("jadwal", [
        "jadwal", "jadwal kuliah", "jadwal perkuliahan",
        "kelas", "ruang kuliah", "jadwal kelas",
        "kalender akademik",
    ]),
    ("wisuda", [
        "wisuda", "yudisium", "kelulusan", "ijazah",
        "lulus", "pengukuhan",
    ]),
    ("layanan_surat", [
        "surat", "pengajuan surat", "surat aktif",
        "surat keterangan", "administrasi", "surat pengantar",
    ]),
    ("pengaduan", [
        "pengaduan", "lapor", "keluhan", "aspirasi",
        "infocare", "whistleblowing", "komplain",
    ]),
    ("prodi", [
        "prodi", "program studi", "jurusan", "daftar prodi",
        "daftar jurusan",
    ]),
    ("faq", [
        "faq", "bantuan", "help", "menu",
        "bisa tanya apa", "informasi apa saja", "apa saja",
        "topik", "daftar pertanyaan",
    ]),
]


# ============================================================
# 5. Deteksi Intent
# ============================================================
def detect_intent(text: str) -> Optional[str]:
    """
    Mendeteksi intent berdasarkan keyword matching.
    Mengembalikan nama intent (string) atau None jika tidak ada yang cocok.
    """
    cleaned = preprocess_text(text)

    for intent_name, keywords in INTENT_KEYWORDS:
        for keyword in keywords:
            if keyword in cleaned:
                return intent_name

    return None


# ============================================================
# 6. Response Generator
# ============================================================
def get_response_by_intent(intent: str, user_text: str = "") -> str:
    """
    Mengambil dan memformat response berdasarkan intent yang terdeteksi.
    """

    if intent == "profil_upgris":
        data = load_json("profil.json")
        if not data:
            return "Maaf, data profil UPGRIS belum tersedia saat ini."
        lines = [
            f"🏛️ **{data.get('universitas', 'UPGRIS')}**\n",
            f"📜 **Sejarah:**\n{data.get('sejarah', '-')}\n",
            f"📌 **Visi:** {data.get('visi', '-')}",
        ]
        misi = data.get("misi", [])
        if misi:
            lines.append("\n📋 **Misi:**")
            for i, m in enumerate(misi, 1):
                lines.append(f"  {i}. {m}")

        pimpinan = data.get("pimpinan", {})
        if pimpinan:
            lines.append("\n👤 **Pimpinan:**")
            lines.append(f"  • Rektor: {pimpinan.get('rektor', '-')}")
            lines.append(f"  • WR I: {pimpinan.get('wakil_rektor_1', '-')}")
            lines.append(f"  • WR II: {pimpinan.get('wakil_rektor_2', '-')}")
            lines.append(f"  • WR III: {pimpinan.get('wakil_rektor_3', '-')}")
            lines.append(f"  • WR IV: {pimpinan.get('wakil_rektor_4', '-')}")

        kontak = data.get("kontak", {})
        if kontak:
            lines.append(f"\n📞 **Kontak:**")
            lines.append(f"  • Telepon: {kontak.get('telepon', '-')}")
            lines.append(f"  • Email: {kontak.get('email_rektorat', '-')}")
            lines.append(f"  • Website: {kontak.get('website', '-')}")

        lokasi = data.get("lokasi", {})
        if lokasi:
            lines.append(f"\n📍 **Lokasi Kampus:**")
            for key, val in lokasi.items():
                lines.append(f"  • {val}")

        return "\n".join(lines)

    elif intent == "profil_informatika":
        data = load_json("profil_informatika.json")
        if not data:
            return "Maaf, data profil Informatika belum tersedia saat ini."
        lines = [
            f"💻 **{data.get('nama', 'Informatika')}**\n",
            f"🏛️ Fakultas: {data.get('fakultas', '-')}",
            f"🎓 Jenjang: {data.get('jenjang', '-')} — Gelar: {data.get('gelar', '-')}\n",
            f"{data.get('deskripsi', '')}\n",
        ]
        # Tampilkan UKT dari akademik2.json
        result = find_prodi_by_keyword("informatika")
        if result:
            prodi = result["prodi"]
            lines.append(f"💰 **UKT:** {format_rupiah(prodi.get('biaya_ukt', 0))}")
            lines.append(f"📊 **Akreditasi:** {prodi.get('akreditasi', '-')}")

        peminatan = data.get("peminatan", [])
        if peminatan:
            lines.append("\n🔬 **Peminatan:**")
            for p in peminatan:
                lines.append(f"  • {p}")
        fasilitas = data.get("fasilitas", [])
        if fasilitas:
            lines.append("\n🏢 **Fasilitas:**")
            for f in fasilitas:
                lines.append(f"  • {f}")
        lines.append(f"\n🌐 **Website:** {data.get('website', '-')}")
        return "\n".join(lines)

    elif intent == "fakultas":
        data = load_json("akademik2.json")
        if not data:
            return "Maaf, data fakultas belum tersedia saat ini."
        lines = ["🏛️ **Daftar Fakultas & Program Studi di UPGRIS:**\n"]
        for fak in data.get("fakultas", []):
            lines.append(f"**{fak.get('nama', '')}** ({fak.get('singkatan', '')})")
            for prodi in fak.get("prodi", []):
                akred = prodi.get("akreditasi", "-")
                lines.append(f"  • {prodi.get('nama', '')} — Akreditasi: {akred}")
            lines.append("")
        return "\n".join(lines)

    elif intent == "prodi":
        data = load_json("prodi.json")
        if not data:
            return "Maaf, data program studi belum tersedia saat ini."
        lines = [
            f"📚 **{data.get('prodi_utama', 'Informatika')}** — Jenjang {data.get('jenjang', 'S1')}\n",
            f"{data.get('deskripsi', '')}\n",
            "🎯 **Prospek Karir:**",
        ]
        for karir in data.get("prospek_karir", []):
            lines.append(f"  • {karir}")
        komp = data.get("kompetensi_lulusan", [])
        if komp:
            lines.append("\n🏅 **Kompetensi Lulusan:**")
            for k in komp:
                lines.append(f"  • {k}")
        return "\n".join(lines)

    elif intent == "dosen":
        data = load_json("dosen.json")
        if not data:
            return "Maaf, data dosen belum tersedia saat ini."
        lines = ["👨‍🏫 **Dosen Program Studi Informatika UPGRIS:**\n"]
        for dosen in data.get("dosen", []):
            lines.append(f"• **{dosen.get('nama', '')}**")
            lines.append(f"  Jabatan: {dosen.get('jabatan', '-')}")
            lines.append(f"  Bidang: {dosen.get('bidang', '-')}")
            lines.append("")
        lines.append(f"_Catatan: {data.get('catatan', '')}_")
        return "\n".join(lines)

    elif intent == "kurikulum":
        data = load_json("kurikulum.json")
        if not data:
            return "Maaf, data kurikulum belum tersedia saat ini."
        lines = [
            f"📖 **Kurikulum Informatika UPGRIS**\n",
            f"{data.get('deskripsi', '')}\n",
            f"📅 Total Semester: {data.get('total_semester', '-')}",
            f"📊 Total SKS: {data.get('total_sks', '-')}\n",
            "📝 **Topik Utama:**",
        ]
        for topik in data.get("topik_utama", []):
            lines.append(f"  • {topik}")
        peminatan = data.get("peminatan", [])
        if peminatan:
            lines.append("\n🔬 **Peminatan:**")
            for p in peminatan:
                if isinstance(p, dict):
                    lines.append(f"  • **{p.get('nama', '')}**: {p.get('fokus', '')}")
                else:
                    lines.append(f"  • {p}")
        return "\n".join(lines)

    elif intent == "pmb":
        data = load_json("akademik2.json")
        pmb = data.get("pmb", {})
        if not pmb:
            # Fallback ke pmb.json lama
            data = load_json("pmb.json")
            if not data:
                return "Maaf, data PMB belum tersedia saat ini."
            lines = [
                "📋 **Penerimaan Mahasiswa Baru (PMB) UPGRIS**\n",
                f"{data.get('deskripsi', '')}\n",
                "🚪 **Jalur Pendaftaran:**",
            ]
            for jalur in data.get("jalur", []):
                if isinstance(jalur, dict):
                    lines.append(f"  • **{jalur.get('nama', '')}**: {jalur.get('keterangan', '')}")
                else:
                    lines.append(f"  • {jalur}")
            lines.append(f"\n🌐 **Website PMB:** {data.get('website', '-')}")
            return "\n".join(lines)

        lines = [
            "📋 **Penerimaan Mahasiswa Baru (PMB) UPGRIS**\n",
            f"📝 **Cara Daftar:**\n{pmb.get('cara_daftar', '-')}\n",
            f"💰 **Biaya Pendaftaran:**\n{pmb.get('biaya_pendaftaran', '-')}\n",
            "🚪 **Jalur Pendaftaran:**",
        ]
        for jalur in pmb.get("jalur_pendaftaran", []):
            lines.append(f"  • **{jalur.get('nama', '')}**: {jalur.get('deskripsi', '')}")
        persyaratan = pmb.get("persyaratan", [])
        if persyaratan:
            lines.append("\n📄 **Persyaratan:**")
            for i, p in enumerate(persyaratan, 1):
                lines.append(f"  {i}. {p}")
        lines.append("\n🌐 **Website PMB:** https://pmb.upgris.ac.id")
        return "\n".join(lines)

    elif intent == "biaya":
        # Cek apakah user menyebut prodi spesifik
        result = find_prodi_by_keyword(user_text)
        if result:
            prodi = result["prodi"]
            fak_nama = result["fakultas"]
            lines = [
                f"💰 **Biaya Kuliah — {prodi.get('nama', '')}**\n",
                f"🏛️ Fakultas: {fak_nama}",
                f"📊 Akreditasi: {prodi.get('akreditasi', '-')}\n",
                f"📌 **UKT Total: {format_rupiah(prodi.get('biaya_ukt', 0))}** per semester\n",
            ]
            detail = prodi.get("biaya_detail")
            if detail:
                lines.append("📋 **Rincian Biaya Masuk (Gelombang 2):**")
                lines.append(f"  • Angsuran 1: {format_rupiah(detail.get('angsuran_1', 0))}")
                lines.append(f"  • Pra Kuliah: {format_rupiah(detail.get('pra_kuliah', 0))}")
                lines.append(f"  • UKP: {format_rupiah(detail.get('ukp', 0))}")
                lines.append(f"  • **Total: {format_rupiah(detail.get('total', 0))}**")
            lines.append(f"\n_Sumber: pmb.upgris.ac.id — Jalur Reguler_")
            return "\n".join(lines)

        # Jika tidak menyebut prodi, tampilkan daftar semua UKT
        data = load_json("akademik2.json")
        if not data:
            return "Maaf, data biaya kuliah belum tersedia saat ini."

        lines = [
            "💰 **Informasi Biaya Kuliah (UKT) UPGRIS**\n",
            "Berikut daftar UKT per program studi (Jalur Reguler):\n",
        ]
        for fak in data.get("fakultas", []):
            lines.append(f"**{fak.get('singkatan', '')} — {fak.get('nama', '')}**")
            for prodi in fak.get("prodi", []):
                ukt = prodi.get("biaya_ukt", 0)
                lines.append(f"  • {prodi.get('nama', '')}: **{format_rupiah(ukt)}**")
            lines.append("")
        lines.append("💡 _Untuk melihat rincian biaya prodi tertentu, ketik misalnya:_")
        lines.append("_\"UKT Informatika\" atau \"biaya PGSD\"_")
        return "\n".join(lines)

    elif intent == "beasiswa":
        data = load_json("akademik2.json")
        beasiswa_list = data.get("beasiswa", [])
        if not beasiswa_list:
            # Fallback ke beasiswa.json lama
            data = load_json("beasiswa.json")
            if not data:
                return "Maaf, data beasiswa belum tersedia saat ini."
            lines = [
                "🎓 **Informasi Beasiswa UPGRIS**\n",
                f"{data.get('deskripsi', '')}\n",
                "📜 **Jenis Beasiswa:**",
            ]
            for b in data.get("jenis", []):
                if isinstance(b, dict):
                    lines.append(f"  • **{b.get('nama', '')}**: {b.get('keterangan', '')}")
                else:
                    lines.append(f"  • {b}")
            return "\n".join(lines)

        lines = ["🎓 **Informasi Beasiswa UPGRIS**\n"]
        for b in beasiswa_list:
            lines.append(f"📌 **{b.get('nama', '')}**")
            lines.append(f"  Sumber: {b.get('sumber', '-')}")
            lines.append(f"  Syarat: {b.get('syarat', '-')}")
            lines.append("")
        return "\n".join(lines)

    elif intent == "mbkm":
        data = load_json("mbkm.json")
        if not data:
            return "Maaf, data MBKM belum tersedia saat ini."
        lines = [
            "🌍 **Merdeka Belajar - Kampus Merdeka (MBKM)**\n",
            f"{data.get('deskripsi', '')}\n",
            "📋 **Program MBKM:**",
        ]
        for prog in data.get("program", []):
            if isinstance(prog, dict):
                lines.append(f"  • **{prog.get('nama', '')}**: {prog.get('keterangan', '')}")
            else:
                lines.append(f"  • {prog}")
        manfaat = data.get("manfaat", [])
        if manfaat:
            lines.append("\n✅ **Manfaat MBKM:**")
            for m in manfaat:
                lines.append(f"  • {m}")
        return "\n".join(lines)

    elif intent == "krs":
        data = load_json("akademik2.json")
        krs = data.get("layanan_akademik", {}).get("krs", {})
        if not krs:
            # Fallback ke akademik.json lama
            data = load_json("akademik.json")
            krs = data.get("krs", {})
            if isinstance(krs, str):
                return f"📝 **Kartu Rencana Studi (KRS)**\n\n{krs}"
        lines = [
            "📝 **Kartu Rencana Studi (KRS)**\n",
            f"{krs.get('deskripsi', '')}\n",
            "📌 **Prosedur Pengisian KRS:**",
            f"{krs.get('prosedur', '-')}",
        ]
        return "\n".join(lines)

    elif intent == "khs":
        data = load_json("akademik2.json")
        khs = data.get("layanan_akademik", {}).get("khs", {})
        if not khs:
            data = load_json("akademik.json")
            khs = data.get("khs", {})
            if isinstance(khs, str):
                return f"📊 **Kartu Hasil Studi (KHS)**\n\n{khs}"
        lines = [
            "📊 **Kartu Hasil Studi (KHS)**\n",
            f"{khs.get('deskripsi', '')}\n",
            "📌 **Prosedur Akses KHS:**",
            f"{khs.get('prosedur', '-')}",
        ]
        return "\n".join(lines)

    elif intent == "ipk":
        data = load_json("akademik.json")
        ipk = data.get("ipk", {})
        if isinstance(ipk, str):
            return f"📈 **Indeks Prestasi Kumulatif (IPK)**\n\n{ipk}"
        lines = [
            f"📈 **{ipk.get('nama', 'IPK')}**\n",
            f"{ipk.get('deskripsi', '')}\n",
            f"📊 **Skala:** {ipk.get('skala', '-')}\n",
        ]
        kategori = ipk.get("kategori", {})
        if kategori:
            lines.append("🏆 **Kategori Kelulusan:**")
            labels = {
                "cum_laude": "Cum Laude",
                "sangat_memuaskan": "Sangat Memuaskan",
                "memuaskan": "Memuaskan",
            }
            for key, label in labels.items():
                if key in kategori:
                    lines.append(f"  • {label}: {kategori[key]}")
        return "\n".join(lines)

    elif intent == "jadwal":
        data = load_json("akademik2.json")
        kalender = data.get("layanan_akademik", {}).get("kalender_akademik", {})
        if not kalender:
            data = load_json("akademik.json")
            jadwal = data.get("jadwal", {})
            if isinstance(jadwal, str):
                return f"📅 **Jadwal Perkuliahan**\n\n{jadwal}"
            lines = [
                f"📅 **{jadwal.get('nama', 'Jadwal Kuliah')}**\n",
                f"{jadwal.get('deskripsi', '')}\n",
                f"📌 **Akses:** {jadwal.get('akses', '-')}",
            ]
            return "\n".join(lines)

        lines = [
            "📅 **Kalender Akademik UPGRIS**\n",
            f"📗 **Semester Ganjil:** {kalender.get('semester_ganjil', '-')}\n",
            f"📘 **Semester Genap:** {kalender.get('semester_genap', '-')}\n",
            f"🏖️ **Libur Akademik:** {kalender.get('libur_akademik', '-')}",
        ]
        return "\n".join(lines)

    elif intent == "skripsi":
        data = load_json("akademik2.json")
        skripsi = data.get("alur_kelulusan", {}).get("skripsi", {})
        if not skripsi:
            data = load_json("akademik.json")
            skripsi = data.get("skripsi", {})
            if isinstance(skripsi, str):
                return f"📄 **Skripsi / Tugas Akhir**\n\n{skripsi}"
        lines = ["📄 **Skripsi / Tugas Akhir**\n"]
        syarat = skripsi.get("syarat", [])
        if syarat:
            lines.append("📋 **Syarat Mengambil Skripsi:**")
            for i, s in enumerate(syarat, 1):
                lines.append(f"  {i}. {s}")
        prosedur = skripsi.get("prosedur", "")
        if prosedur:
            lines.append(f"\n📌 **Prosedur:**\n{prosedur}")
        return "\n".join(lines)

    elif intent == "pkl":
        data = load_json("akademik2.json")
        pkl = data.get("alur_kelulusan", {}).get("pkl", {})
        if not pkl:
            return "Maaf, data PKL belum tersedia saat ini."
        lines = ["🏢 **Praktik Kerja Lapangan (PKL)**\n"]
        syarat = pkl.get("syarat", [])
        if syarat:
            lines.append("📋 **Syarat PKL:**")
            for i, s in enumerate(syarat, 1):
                lines.append(f"  {i}. {s}")
        prosedur = pkl.get("prosedur", "")
        if prosedur:
            lines.append(f"\n📌 **Prosedur:**\n{prosedur}")
        return "\n".join(lines)

    elif intent == "kkn":
        data = load_json("akademik2.json")
        kkn = data.get("alur_kelulusan", {}).get("kkn", {})
        if not kkn:
            return "Maaf, data KKN belum tersedia saat ini."
        lines = ["🌏 **Kuliah Kerja Nyata (KKN)**\n"]
        syarat = kkn.get("syarat", [])
        if syarat:
            lines.append("📋 **Syarat KKN:**")
            for i, s in enumerate(syarat, 1):
                lines.append(f"  {i}. {s}")
        prosedur = kkn.get("prosedur", "")
        if prosedur:
            lines.append(f"\n📌 **Prosedur:**\n{prosedur}")
        return "\n".join(lines)

    elif intent == "wisuda":
        data = load_json("akademik2.json")
        wisuda = data.get("alur_kelulusan", {}).get("wisuda", {})
        if not wisuda:
            data = load_json("akademik.json")
            wisuda = data.get("wisuda", {})
            if isinstance(wisuda, str):
                return f"🎓 **Wisuda**\n\n{wisuda}"
        lines = ["🎓 **Wisuda UPGRIS**\n"]
        syarat = wisuda.get("syarat", [])
        if syarat:
            lines.append("📋 **Syarat Wisuda:**")
            for i, s in enumerate(syarat, 1):
                lines.append(f"  {i}. {s}")
        prosedur = wisuda.get("prosedur", "")
        if prosedur:
            lines.append(f"\n📌 **Prosedur:**\n{prosedur}")
        return "\n".join(lines)

    elif intent == "layanan_surat":
        data = load_json("akademik.json")
        surat = data.get("layanan_surat", {})
        if isinstance(surat, str):
            return f"📨 **Layanan Surat**\n\n{surat}"
        lines = [
            f"📨 **{surat.get('nama', 'Layanan Surat')}**\n",
            f"{surat.get('deskripsi', '')}\n",
        ]
        jenis = surat.get("jenis_surat", [])
        if jenis:
            lines.append("📄 **Jenis Surat yang Tersedia:**")
            for j in jenis:
                lines.append(f"  • {j}")
        return "\n".join(lines)

    elif intent == "pengaduan":
        data = load_json("akademik.json")
        pengaduan = data.get("pengaduan", {})
        if isinstance(pengaduan, str):
            return f"📢 **Layanan Pengaduan**\n\n{pengaduan}"
        lines = [
            f"📢 **{pengaduan.get('nama', 'Pengaduan')}**\n",
            f"{pengaduan.get('deskripsi', '')}\n",
        ]
        kanal = pengaduan.get("kanal", [])
        if kanal:
            lines.append("📞 **Kanal Pengaduan:**")
            for k in kanal:
                lines.append(f"  • {k}")
        return "\n".join(lines)

    elif intent == "faq":
        data = load_json("faq2.json")
        if not data:
            # Fallback ke faq.json lama
            data = load_json("faq.json")
            if not data:
                return "Maaf, data FAQ belum tersedia saat ini."
            lines = ["❓ **Pertanyaan yang Sering Ditanyakan (FAQ):**\n"]
            for faq_item in data.get("faq", []):
                lines.append(f"**Q: {faq_item.get('question', '')}**")
                lines.append(f"A: {faq_item.get('answer', '')}\n")
            return "\n".join(lines)

        # faq2.json adalah list langsung
        if isinstance(data, list):
            # Cari FAQ yang relevan dengan input user
            cleaned = preprocess_text(user_text)
            relevant = []
            for faq_item in data:
                q = preprocess_text(faq_item.get("pertanyaan", ""))
                # Hitung kecocokan kata
                user_words = set(cleaned.split())
                q_words = set(q.split())
                common = user_words & q_words
                # Minimal 2 kata sama (selain kata umum)
                stopwords = {"apa", "di", "dan", "yang", "untuk", "ini", "itu", "ada", "dari",
                             "ke", "dengan", "adalah", "bisa", "cara", "bagaimana", "berapa",
                             "apakah", "saya", "mau", "ingin", "tanya", "upgris"}
                meaningful = common - stopwords
                if len(meaningful) >= 1:
                    relevant.append((len(meaningful), faq_item))

            if relevant:
                relevant.sort(key=lambda x: x[0], reverse=True)
                top = relevant[:5]
                lines = ["❓ **FAQ yang relevan dengan pertanyaan Anda:**\n"]
                for _, faq_item in top:
                    lines.append(f"**Q: {faq_item.get('pertanyaan', '')}**")
                    lines.append(f"A: {faq_item.get('jawaban', '')}\n")
                return "\n".join(lines)

            # Jika tidak ada yang relevan, tampilkan 10 FAQ pertama
            lines = ["❓ **Pertanyaan yang Sering Ditanyakan (FAQ):**\n"]
            for faq_item in data[:10]:
                lines.append(f"**Q: {faq_item.get('pertanyaan', '')}**")
                lines.append(f"A: {faq_item.get('jawaban', '')}\n")
            lines.append(f"_... dan {len(data) - 10} FAQ lainnya. Coba tanyakan topik spesifik!_")
            return "\n".join(lines)

        return "Maaf, data FAQ belum tersedia saat ini."

    else:
        # Fallback / ERROR — coba cocokkan dengan FAQ
        faq_data = load_json("faq2.json")
        if isinstance(faq_data, list) and faq_data:
            cleaned = preprocess_text(user_text)
            best_match = None
            best_score = 0
            for faq_item in faq_data:
                q = preprocess_text(faq_item.get("pertanyaan", ""))
                user_words = set(cleaned.split())
                q_words = set(q.split())
                stopwords = {"apa", "di", "dan", "yang", "untuk", "ini", "itu", "ada", "dari",
                             "ke", "dengan", "adalah", "bisa", "cara", "bagaimana", "berapa",
                             "apakah", "saya", "mau", "ingin", "tanya", "upgris"}
                common = (user_words & q_words) - stopwords
                if len(common) > best_score:
                    best_score = len(common)
                    best_match = faq_item

            if best_match and best_score >= 2:
                return (
                    f"💡 Mungkin ini yang Anda maksud:\n\n"
                    f"**Q: {best_match.get('pertanyaan', '')}**\n"
                    f"A: {best_match.get('jawaban', '')}"
                )

        return (
            "🤔 Maaf, saya belum memahami pertanyaan tersebut.\n\n"
            "Anda dapat mencoba bertanya tentang topik berikut:\n"
            "  • **Profil UPGRIS** — informasi tentang universitas\n"
            "  • **Informatika** — profil program studi\n"
            "  • **Fakultas** — daftar fakultas di UPGRIS\n"
            "  • **Dosen** — informasi dosen Informatika\n"
            "  • **Kurikulum** — mata kuliah dan peminatan\n"
            "  • **PMB** — pendaftaran mahasiswa baru\n"
            "  • **Biaya / UKT** — informasi biaya kuliah per prodi\n"
            "  • **Beasiswa** — jenis beasiswa\n"
            "  • **MBKM** — program Kampus Merdeka\n"
            "  • **KRS / KHS / IPK** — informasi akademik\n"
            "  • **Jadwal** — kalender akademik\n"
            "  • **Skripsi / PKL / KKN** — alur kelulusan\n"
            "  • **Wisuda** — informasi wisuda\n"
            "  • **Surat** — layanan surat akademik\n"
            "  • **Pengaduan** — layanan pengaduan\n"
            "  • **FAQ** — pertanyaan umum\n\n"
            "_Contoh: \"Berapa UKT Informatika?\" atau \"Cara daftar PMB\"_"
        )
