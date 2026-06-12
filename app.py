"""
app.py - Website UPGRIS dengan Chatbot Akademik FSM
====================================================
Aplikasi Streamlit yang menampilkan landing page ala website
Universitas PGRI Semarang dengan chatbot terintegrasi.

Jalankan: streamlit run app.py
"""

import streamlit as st
import pandas as pd

from FSM import AcademicFSM, State
from engine import load_json
from utils import (
    get_logo_path,
    get_data_summary,
    export_transitions_csv,
    load_all_json_files,
    CONTOH_PERTANYAAN,
)

# ============================================================
# Konfigurasi Halaman
# ============================================================
st.set_page_config(
    page_title="Universitas PGRI Semarang — UPGRIS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# Session State
# ============================================================
if "fsm" not in st.session_state:
    st.session_state.fsm = AcademicFSM()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Halo! Selamat datang di **Chatbot Akademik UPGRIS**! 👋\n\n"
                "Saya asisten virtual berbasis **Finite State Machine** yang siap membantu "
                "Anda mendapatkan informasi akademik UPGRIS.\n\n"
                "Silakan ketik pertanyaan atau pilih topik di bawah!"
            ),
        }
    ]

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "active_page" not in st.session_state:
    st.session_state.active_page = "beranda"

fsm: AcademicFSM = st.session_state.fsm


# ============================================================
# Custom CSS — Website UPGRIS Style
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ─── Reset ─── */
* { font-family: 'Inter', sans-serif; }
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stDeployButton { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

/* ─── Navbar ─── */
.upgris-navbar {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: 0 4px 20px rgba(30, 27, 75, 0.3);
}
.navbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    color: white;
    text-decoration: none;
}
.navbar-brand-text h1 {
    font-size: 1.05rem;
    font-weight: 800;
    margin: 0;
    color: white;
    letter-spacing: -0.3px;
}
.navbar-brand-text p {
    font-size: 0.68rem;
    margin: 0;
    color: rgba(255,255,255,0.65);
    font-weight: 400;
}
.navbar-links {
    display: flex;
    gap: 0.5rem;
    list-style: none;
    margin: 0;
    padding: 0;
}
.navbar-links a {
    color: rgba(255,255,255,0.8);
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.2s;
}
.navbar-links a:hover, .navbar-links a.active {
    background: rgba(255,255,255,0.15);
    color: white;
}

/* ─── Hero ─── */
.hero-section {
    background: linear-gradient(160deg, #1e1b4b 0%, #312e81 25%, #4338ca 55%, #6366f1 80%, #818cf8 100%);
    padding: 5rem 2rem 4rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -15%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-section::after {
    content: '';
    position: absolute;
    bottom: -25%;
    left: -10%;
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-content {
    position: relative;
    z-index: 1;
    max-width: 750px;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.9);
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.hero-content h1 {
    color: white;
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 1rem;
}
.hero-content h1 span {
    background: linear-gradient(135deg, #c4b5fd, #a78bfa, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    color: rgba(255,255,255,0.72);
    font-size: 1.05rem;
    max-width: 580px;
    margin: 0 auto 2rem;
    font-weight: 400;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin-top: 2.5rem;
}
.hero-stat { text-align: center; }
.hero-stat-num {
    font-size: 2rem;
    font-weight: 800;
    color: white;
}
.hero-stat-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.6);
    font-weight: 400;
}

/* ─── Section ─── */
.section {
    padding: 4rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
}
.section-header {
    text-align: center;
    margin-bottom: 2.5rem;
}
.section-header h2 {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1e1b4b;
    margin-bottom: 0.4rem;
}
.section-header p {
    color: #64748b;
    font-size: 0.95rem;
    max-width: 500px;
    margin: 0 auto;
}
.section-alt {
    background: #f1f5f9;
}

/* ─── Cards Grid ─── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}
.ucard {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.8rem;
    transition: transform 0.3s, box-shadow 0.3s;
}
.ucard:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.1);
}
.ucard-icon {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    background: #eef2ff;
}
.ucard h3 {
    font-size: 1.02rem;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 0.5rem;
}
.ucard p {
    color: #64748b;
    font-size: 0.85rem;
    line-height: 1.6;
}

/* ─── Fakultas Cards ─── */
.fakultas-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    transition: transform 0.3s, box-shadow 0.3s;
    border-left: 4px solid #4338ca;
}
.fakultas-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}
.fakultas-card h3 {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 0.6rem;
}
.fakultas-card .prodi-list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.prodi-tag {
    background: #eef2ff;
    color: #4338ca;
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 0.72rem;
    font-weight: 500;
}

/* ─── Dosen Card ─── */
.dosen-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
}
.dosen-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}
.dosen-avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4338ca, #7c3aed);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 auto 1rem;
}
.dosen-card h3 {
    font-size: 0.9rem;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 0.3rem;
}
.dosen-card p {
    font-size: 0.78rem;
    color: #64748b;
}
.dosen-badge {
    display: inline-block;
    background: #eef2ff;
    color: #4338ca;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.68rem;
    font-weight: 600;
    margin-top: 8px;
}

/* ─── Info Boxes ─── */
.info-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.info-box h3 {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 0.6rem;
}
.info-box p, .info-box li {
    color: #475569;
    font-size: 0.88rem;
    line-height: 1.65;
}
.info-box ul {
    padding-left: 1.2rem;
}

/* ─── PMB Banner ─── */
.pmb-banner {
    background: linear-gradient(135deg, #7c3aed 0%, #4338ca 50%, #1e1b4b 100%);
    border-radius: 20px;
    padding: 3rem;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.pmb-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.pmb-banner h2 {
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
    color: white;
}
.pmb-banner p {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.8);
    max-width: 500px;
    margin: 0 auto 1.5rem;
    position: relative;
    z-index: 1;
}
.pmb-btn {
    display: inline-block;
    background: white;
    color: #4338ca;
    padding: 12px 28px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
    position: relative;
    z-index: 1;
    transition: transform 0.2s;
}
.pmb-btn:hover { transform: translateY(-2px); }

/* ─── FSM Section ─── */
.fsm-definition {
    background: #1e1b4b;
    border-radius: 16px;
    padding: 2rem;
    color: white;
}
.fsm-definition h3 {
    color: #a78bfa;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.fsm-definition .formula {
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    text-align: center;
    padding: 1rem;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    margin-bottom: 1rem;
    font-family: 'Georgia', serif;
    letter-spacing: 1px;
}
.fsm-definition li {
    color: rgba(255,255,255,0.8);
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
    line-height: 1.5;
}
.fsm-definition strong { color: #c4b5fd; }

/* ─── Footer ─── */
.site-footer {
    background: #0f172a;
    color: rgba(255,255,255,0.7);
    padding: 3rem 2rem;
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    max-width: 1100px;
    margin: 0 auto 2rem;
}
.footer-col h4 {
    color: white;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.footer-col p, .footer-col li {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.55);
    line-height: 1.7;
}
.footer-col ul {
    list-style: none;
    padding: 0;
}
.footer-col ul li { margin-bottom: 0.3rem; }
.footer-col a {
    color: rgba(255,255,255,0.55);
    text-decoration: none;
    transition: color 0.2s;
}
.footer-col a:hover { color: #a78bfa; }
.footer-bottom {
    text-align: center;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.08);
    font-size: 0.75rem;
    color: rgba(255,255,255,0.35);
    max-width: 1100px;
    margin: 0 auto;
}

/* ─── Chatbot Widget ─── */
.chat-overlay {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9999;
}

/* ─── Status Badge ─── */
.status-accepted {
    background: linear-gradient(135deg, #059669, #10b981);
    color: white;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    display: inline-block;
}
.status-rejected {
    background: linear-gradient(135deg, #dc2626, #ef4444);
    color: white;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    display: inline-block;
}

/* ─── Metric Mini ─── */
.metric-mini {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.metric-mini-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: rgba(255,255,255,0.5);
    margin-bottom: 2px;
}
.metric-mini-value {
    font-size: 0.95rem;
    font-weight: 700;
    color: white;
}

/* ─── Quick Links ─── */
.quick-links {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
    padding: 1.5rem 2rem;
    background: white;
    border-bottom: 1px solid #e2e8f0;
}
.quick-link {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    font-size: 0.78rem;
    font-weight: 500;
    color: #475569;
    text-decoration: none;
    transition: all 0.2s;
}
.quick-link:hover {
    background: #eef2ff;
    border-color: #6366f1;
    color: #4338ca;
}

/* ─── Tabs Override ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 0.83rem;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* ─── Responsive ─── */
@media (max-width: 768px) {
    .hero-content h1 { font-size: 1.8rem; }
    .hero-stats { gap: 1.5rem; }
    .navbar-links { display: none; }
    .cards-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# NAVBAR
# ============================================================
logo_path = get_logo_path()
st.markdown(f"""
<div class="upgris-navbar">
    <div class="navbar-brand">
        <div class="navbar-brand-text">
            <h1>UNIVERSITAS PGRI SEMARANG</h1>
            <p>Unggul dan Berjatidiri</p>
        </div>
    </div>
    <div class="navbar-links">
        <a href="#beranda" class="active">Beranda</a>
        <a href="#profil">Profil</a>
        <a href="#fakultas">Fakultas</a>
        <a href="#akademik">Akademik</a>
        <a href="#chatbot">Chatbot FSM</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================
profil_data = load_json("profil_upgris.json")

st.markdown(f"""
<div class="hero-section" id="beranda">
    <div class="hero-content">
        <div class="hero-badge">Universitas PGRI Semarang</div>
        <h1>Membangun Generasi<br><span>Unggul & Berjatidiri</span></h1>
        <p class="hero-subtitle">
            {profil_data.get('deskripsi', 'Universitas PGRI Semarang merupakan perguruan tinggi yang menyelenggarakan pendidikan akademik dan profesional.')}
        </p>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-num">5+</div>
                <div class="hero-stat-label">Fakultas</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">20+</div>
                <div class="hero-stat-label">Program Studi</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">200+</div>
                <div class="hero-stat-label">Dosen</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">10K+</div>
                <div class="hero-stat-label">Mahasiswa</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Links
st.markdown("""
<div class="quick-links">
    <span class="quick-link">📋 PMB 2025/2026</span>
    <span class="quick-link">🎓 Beasiswa</span>
    <span class="quick-link">📊 Sistem Akademik</span>
    <span class="quick-link">🌍 MBKM</span>
    <span class="quick-link">📞 Kontak</span>
</div>
""", unsafe_allow_html=True)


# ============================================================
# TABS: Konten Website
# ============================================================
tab_beranda, tab_chatbot, tab_fsm = st.tabs([
    "🏛 Website UPGRIS",
    "💬 Chatbot Akademik",
    "⚙ Simulasi FSM",
])


# ────────────────────────────────────────────────────────────
# TAB 1: Website UPGRIS
# ────────────────────────────────────────────────────────────
with tab_beranda:

    # ── Visi Misi ──
    st.markdown("""
    <div class="section" id="profil">
        <div class="section-header">
            <h2>Visi & Misi UPGRIS</h2>
            <p>Komitmen kami dalam dunia pendidikan tinggi</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_v, col_m = st.columns(2)
    with col_v:
        st.markdown(f"""
        <div class="info-box">
            <h3>🔭 Visi</h3>
            <p>{profil_data.get('visi', '-')}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_m:
        misi_list = profil_data.get("misi", [])
        misi_html = "".join([f"<li>{m}</li>" for m in misi_list])
        st.markdown(f"""
        <div class="info-box">
            <h3>🎯 Misi</h3>
            <ul>{misi_html}</ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Prodi Informatika ──
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <h2>Program Studi Informatika</h2>
            <p>Mencetak profesional IT yang kompeten dan berdaya saing</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    info_data = load_json("profil_informatika.json")
    prodi_data = load_json("prodi.json")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        peminatan = info_data.get("peminatan", [])
        pem_html = "".join([f"<li><strong>{p}</strong></li>" for p in peminatan])
        st.markdown(f"""
        <div class="info-box">
            <h3>💻 Tentang Prodi</h3>
            <p>{info_data.get('deskripsi', '-')}</p>
            <br><h3>🔬 Peminatan</h3>
            <ul>{pem_html}</ul>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        karir_list = prodi_data.get("prospek_karir", [])
        karir_html = "".join([f"<li>{k}</li>" for k in karir_list])
        st.markdown(f"""
        <div class="info-box">
            <h3>🎯 Prospek Karir</h3>
            <ul>{karir_html}</ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Fakultas ──
    st.markdown("""
    <div class="section" id="fakultas">
        <div class="section-header">
            <h2>Fakultas di UPGRIS</h2>
            <p>Beragam pilihan bidang ilmu untuk masa depan Anda</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fakultas_data = load_json("fakultas.json")
    fak_list = fakultas_data.get("fakultas", [])

    cols_fak = st.columns(min(len(fak_list), 3))
    for i, fak in enumerate(fak_list):
        with cols_fak[i % 3]:
            prodi_tags = "".join(
                [f'<span class="prodi-tag">{p}</span>' for p in fak.get("prodi", [])]
            )
            st.markdown(f"""
            <div class="fakultas-card">
                <h3>{fak.get('nama', '')} ({fak.get('singkatan', '')})</h3>
                <div class="prodi-list">{prodi_tags}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

    # ── Dosen ──
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <h2>Dosen Informatika</h2>
            <p>Tenaga pengajar profesional di bidangnya</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    dosen_data = load_json("dosen.json")
    dosen_list = dosen_data.get("dosen", [])

    cols_dosen = st.columns(min(len(dosen_list), 3) if dosen_list else 1)
    for i, d in enumerate(dosen_list):
        with cols_dosen[i % 3]:
            initials = "".join([w[0] for w in d.get("nama", "").split()[:2]])
            st.markdown(f"""
            <div class="dosen-card">
                <div class="dosen-avatar">{initials}</div>
                <h3>{d.get('nama', '')}</h3>
                <p>{d.get('bidang', '')}</p>
                <span class="dosen-badge">{d.get('jabatan', '')}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

    # ── PMB Banner ──
    st.markdown("")
    pmb_data = load_json("pmb.json")
    st.markdown(f"""
    <div style="padding: 0 2rem; max-width: 1100px; margin: 0 auto;">
        <div class="pmb-banner">
            <h2>Pendaftaran Mahasiswa Baru</h2>
            <p>{pmb_data.get('deskripsi', 'Informasi PMB dapat diakses melalui website resmi.')}</p>
            <a href="{pmb_data.get('website', '#')}" target="_blank" class="pmb-btn">Daftar Sekarang →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Kurikulum ──
    st.markdown("""
    <div class="section" id="akademik">
        <div class="section-header">
            <h2>Kurikulum & Layanan Akademik</h2>
            <p>Informasi penting seputar akademik mahasiswa</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    kurikulum_data = load_json("kurikulum.json")
    akademik_data = load_json("akademik.json")

    st.markdown(f"""
    <div style="max-width:1100px; margin:0 auto; padding:0 2rem;">
    <div class="cards-grid">
        <div class="ucard">
            <div class="ucard-icon">📖</div>
            <h3>Kurikulum</h3>
            <p>{kurikulum_data.get('deskripsi', '-')[:150]}...</p>
        </div>
        <div class="ucard">
            <div class="ucard-icon">📝</div>
            <h3>KRS & KHS</h3>
            <p>Kartu Rencana Studi untuk pengambilan mata kuliah dan Kartu Hasil Studi berisi nilai semester.</p>
        </div>
        <div class="ucard">
            <div class="ucard-icon">📊</div>
            <h3>IPK & Jadwal</h3>
            <p>Indeks Prestasi Kumulatif dan jadwal perkuliahan melalui sistem akademik online.</p>
        </div>
        <div class="ucard">
            <div class="ucard-icon">📄</div>
            <h3>Skripsi</h3>
            <p>Tahapan tugas akhir mulai dari pengajuan judul, seminar proposal, penelitian, hingga sidang.</p>
        </div>
        <div class="ucard">
            <div class="ucard-icon">🎓</div>
            <h3>Wisuda</h3>
            <p>Upacara pengukuhan kelulusan mahasiswa setelah menyelesaikan seluruh kewajiban akademik.</p>
        </div>
        <div class="ucard">
            <div class="ucard-icon">📨</div>
            <h3>Layanan Surat</h3>
            <p>Pengajuan surat keterangan aktif, pengantar penelitian, rekomendasi, dan transkrip nilai.</p>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")


# ────────────────────────────────────────────────────────────
# TAB 2: Chatbot Akademik
# ────────────────────────────────────────────────────────────
with tab_chatbot:

    st.markdown("""
    <div style="max-width:900px; margin:0 auto; padding:2rem;">
    """, unsafe_allow_html=True)

    # FSM Status Bar
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("State Saat Ini", fsm.get_current_state())
    with col_s2:
        st.metric("Intent Terakhir", fsm.last_intent or "-")
    with col_s3:
        st.metric("Total Transisi", len(fsm.get_transition_history()))
    with col_s4:
        if st.button("🔄 Reset Chat", width="stretch"):
            st.session_state.fsm.reset()
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Chatbot telah direset!\n\n"
                        "FSM kembali ke state awal. Silakan ajukan pertanyaan baru."
                    ),
                }
            ]
            st.session_state.pending_question = None
            st.rerun()

    st.markdown("---")

    # Quick Questions
    st.markdown("**Contoh pertanyaan:**")
    q_cols = st.columns(6)
    quick_qs = [
        "Apa itu UPGRIS?", "Prodi Informatika", "Dosen",
        "Kurikulum", "Cara daftar PMB", "Beasiswa",
    ]
    for i, q in enumerate(quick_qs):
        with q_cols[i]:
            if st.button(q, key=f"qq_{q}", width="stretch"):
                st.session_state.pending_question = q
                st.rerun()

    st.markdown("---")

    # Chat Messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "fsm_detail" in msg:
                detail = msg["fsm_detail"]
                with st.expander("Detail Proses FSM", expanded=False):
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        st.markdown(f"**Input:** {detail.get('input', '-')}")
                        st.markdown(f"**Intent:** `{detail.get('intent', '-')}`")
                        st.markdown(f"**State Tujuan:** `{detail.get('state', '-')}`")
                    with dc2:
                        st.markdown(f"**Transisi:** `{detail.get('transition', '-')}`")
                        if detail.get("accepted"):
                            st.markdown('<span class="status-accepted">Accepted</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="status-rejected">Fallback</span>', unsafe_allow_html=True)

    # Pending question
    pending = st.session_state.pending_question
    if pending:
        st.session_state.pending_question = None
        st.session_state.messages.append({"role": "user", "content": pending})
        result = fsm.process_input(pending)
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "fsm_detail": {
                "input": pending,
                "intent": result["intent"],
                "state": result["state"],
                "transition": result["transition"],
                "accepted": result["accepted"],
            },
        })
        st.rerun()

    # Chat input
    user_input = st.chat_input("Ketik pertanyaan Anda di sini...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        result = fsm.process_input(user_input)
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "fsm_detail": {
                "input": user_input,
                "intent": result["intent"],
                "state": result["state"],
                "transition": result["transition"],
                "accepted": result["accepted"],
            },
        })
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # More questions in expander
    with st.expander("📋 Semua Contoh Pertanyaan"):
        for q in CONTOH_PERTANYAAN:
            if st.button(f"→ {q}", key=f"allq_{q}"):
                st.session_state.pending_question = q
                st.rerun()

    # Export
    history = fsm.get_transition_history()
    if history:
        csv_data = export_transitions_csv(history)
        st.download_button(
            label="Export Riwayat Transisi (CSV)",
            data=csv_data,
            file_name="riwayat_transisi_fsm.csv",
            mime="text/csv",
        )


# ────────────────────────────────────────────────────────────
# TAB 3: Simulasi FSM
# ────────────────────────────────────────────────────────────
with tab_fsm:

    st.markdown("""
    <div style="max-width:1100px; margin:0 auto; padding:2rem;">
    """, unsafe_allow_html=True)

    # ── Definisi Formal ──
    col_def, col_about = st.columns([1, 1])

    with col_def:
        st.markdown("""
        <div class="fsm-definition">
            <h3>Definisi Formal FSM</h3>
            <div class="formula">M = (Q, Σ, δ, q₀, F)</div>
            <ul>
                <li><strong>Q</strong> = Himpunan 24 state (START, IDLE, DETECT_INTENT, 19 state info, ERROR, END)</li>
                <li><strong>Σ</strong> = Input berupa teks pertanyaan pengguna</li>
                <li><strong>δ</strong> = Fungsi transisi berdasarkan intent keyword</li>
                <li><strong>q₀</strong> = START (state awal)</li>
                <li><strong>F</strong> = {IDLE, END} (accepting states)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_about:
        st.markdown("""
        <div class="info-box">
            <h3>Tentang Sistem</h3>
            <p>Chatbot ini dibuat sebagai tugas <strong>Teori Bahasa dan Otomata</strong> di 
            Prodi Informatika UPGRIS. Sistem menggunakan <strong>FSM rule-based</strong> 
            dengan keyword matching — tanpa API AI eksternal.</p>
            <br>
            <p><strong>Alur:</strong> IDLE → DETECT_INTENT → STATE_INFO → IDLE</p>
            <p><strong>Fallback:</strong> IDLE → DETECT_INTENT → ERROR → IDLE</p>
            <br>
            <p>Setiap pertanyaan pengguna adalah <strong>input (Σ)</strong>. Intent menentukan 
            <strong>transisi state (δ)</strong>. State menghasilkan <strong>output</strong> 
            berupa informasi akademik.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── Diagram FSM ──
    st.markdown("### Diagram FSM")

    dot_diagram = """
    digraph FSM {
        rankdir=LR;
        bgcolor="transparent";
        node [fontname="Inter", fontsize=9, style="filled,rounded", shape=box];
        edge [fontname="Inter", fontsize=7, color="#64748b"];

        START [fillcolor="#1e1b4b", fontcolor="white", shape=circle, label="START"];
        IDLE [fillcolor="#059669", fontcolor="white", shape=doublecircle, label="IDLE"];
        DETECT_INTENT [fillcolor="#d97706", fontcolor="white", label="DETECT\\nINTENT"];
        ERROR [fillcolor="#dc2626", fontcolor="white", label="ERROR"];

        PROFIL_UPGRIS [fillcolor="#4338ca", fontcolor="white", label="PROFIL\\nUPGRIS"];
        PROFIL_INFORMATIKA [fillcolor="#4338ca", fontcolor="white", label="PROFIL\\nINFO"];
        FAKULTAS_INFO [fillcolor="#6366f1", fontcolor="white", label="FAKULTAS"];
        PRODI_INFO [fillcolor="#6366f1", fontcolor="white", label="PRODI"];
        DOSEN_INFO [fillcolor="#6366f1", fontcolor="white", label="DOSEN"];
        KURIKULUM_INFO [fillcolor="#6366f1", fontcolor="white", label="KURIKULUM"];
        PMB_INFO [fillcolor="#7c3aed", fontcolor="white", label="PMB"];
        BIAYA_INFO [fillcolor="#7c3aed", fontcolor="white", label="BIAYA"];
        BEASISWA_INFO [fillcolor="#7c3aed", fontcolor="white", label="BEASISWA"];
        MBKM_INFO [fillcolor="#7c3aed", fontcolor="white", label="MBKM"];
        KRS_INFO [fillcolor="#0891b2", fontcolor="white", label="KRS"];
        KHS_INFO [fillcolor="#0891b2", fontcolor="white", label="KHS"];
        IPK_INFO [fillcolor="#0891b2", fontcolor="white", label="IPK"];
        JADWAL_INFO [fillcolor="#0891b2", fontcolor="white", label="JADWAL"];
        SKRIPSI_INFO [fillcolor="#0d9488", fontcolor="white", label="SKRIPSI"];
        WISUDA_INFO [fillcolor="#0d9488", fontcolor="white", label="WISUDA"];
        LAYANAN_SURAT [fillcolor="#0d9488", fontcolor="white", label="SURAT"];
        PENGADUAN_INFO [fillcolor="#0d9488", fontcolor="white", label="PENGADUAN"];
        FAQ_INFO [fillcolor="#475569", fontcolor="white", label="FAQ"];

        START -> IDLE [label="init", color="#059669", penwidth=2];
        IDLE -> DETECT_INTENT [label="user input", color="#d97706", penwidth=2];

        DETECT_INTENT -> PROFIL_UPGRIS; DETECT_INTENT -> PROFIL_INFORMATIKA;
        DETECT_INTENT -> FAKULTAS_INFO; DETECT_INTENT -> PRODI_INFO;
        DETECT_INTENT -> DOSEN_INFO; DETECT_INTENT -> KURIKULUM_INFO;
        DETECT_INTENT -> PMB_INFO; DETECT_INTENT -> BIAYA_INFO;
        DETECT_INTENT -> BEASISWA_INFO; DETECT_INTENT -> MBKM_INFO;
        DETECT_INTENT -> KRS_INFO; DETECT_INTENT -> KHS_INFO;
        DETECT_INTENT -> IPK_INFO; DETECT_INTENT -> JADWAL_INFO;
        DETECT_INTENT -> SKRIPSI_INFO; DETECT_INTENT -> WISUDA_INFO;
        DETECT_INTENT -> LAYANAN_SURAT; DETECT_INTENT -> PENGADUAN_INFO;
        DETECT_INTENT -> FAQ_INFO;
        DETECT_INTENT -> ERROR [color="#dc2626", penwidth=2];

        PROFIL_UPGRIS -> IDLE [style=dashed, color="#059669"];
        PROFIL_INFORMATIKA -> IDLE [style=dashed, color="#059669"];
        FAKULTAS_INFO -> IDLE [style=dashed, color="#059669"];
        PRODI_INFO -> IDLE [style=dashed, color="#059669"];
        DOSEN_INFO -> IDLE [style=dashed, color="#059669"];
        KURIKULUM_INFO -> IDLE [style=dashed, color="#059669"];
        PMB_INFO -> IDLE [style=dashed, color="#059669"];
        BIAYA_INFO -> IDLE [style=dashed, color="#059669"];
        BEASISWA_INFO -> IDLE [style=dashed, color="#059669"];
        MBKM_INFO -> IDLE [style=dashed, color="#059669"];
        KRS_INFO -> IDLE [style=dashed, color="#059669"];
        KHS_INFO -> IDLE [style=dashed, color="#059669"];
        IPK_INFO -> IDLE [style=dashed, color="#059669"];
        JADWAL_INFO -> IDLE [style=dashed, color="#059669"];
        SKRIPSI_INFO -> IDLE [style=dashed, color="#059669"];
        WISUDA_INFO -> IDLE [style=dashed, color="#059669"];
        LAYANAN_SURAT -> IDLE [style=dashed, color="#059669"];
        PENGADUAN_INFO -> IDLE [style=dashed, color="#059669"];
        FAQ_INFO -> IDLE [style=dashed, color="#059669"];
        ERROR -> IDLE [style=dashed, color="#dc2626"];
    }
    """
    st.graphviz_chart(dot_diagram, use_container_width=True)

    # Legenda
    lc1, lc2, lc3 = st.columns(3)
    with lc1:
        st.markdown("""
        **Legenda State:**
        - 🟣 Ungu = Profil
        - 🔵 Biru = Info Akademik
        - 🟡 Kuning = Deteksi Intent
        """)
    with lc2:
        st.markdown("""
        **Legenda Transisi:**
        - Garis solid = Transisi utama
        - Garis putus = Kembali IDLE
        - Merah = Error / Fallback
        """)
    with lc3:
        st.markdown("""
        **Legenda Bentuk:**
        - Lingkaran = START
        - Lingkaran ganda = IDLE (accepting)
        - Kotak = State proses
        """)

    st.markdown("---")

    # ── Tabel Transisi ──
    st.markdown("### Tabel Transisi (δ)")
    transition_table = fsm.get_transition_table()
    df_transition = pd.DataFrame(transition_table)
    df_transition.columns = ["State Awal", "Input", "State Tujuan", "Output"]
    df_transition.index = range(1, len(df_transition) + 1)
    df_transition.index.name = "No"
    st.dataframe(df_transition, use_container_width=True, height=500)

    st.markdown("---")

    # ── Riwayat Runtime ──
    st.markdown("### Riwayat Transisi Runtime")
    runtime_history = fsm.get_transition_history()
    if runtime_history:
        df_runtime = pd.DataFrame(runtime_history)
        df_runtime.columns = ["Dari State", "Ke State", "Input", "Intent"]
        df_runtime.index = range(1, len(df_runtime) + 1)
        df_runtime.index.name = "No"
        st.dataframe(df_runtime, use_container_width=True)
    else:
        st.info("Belum ada riwayat transisi. Mulai bertanya di tab Chatbot!")

    st.markdown("---")

    # ── Dataset ──
    st.markdown("### Dataset Akademik")
    st.caption("Data disimpan dalam format JSON di folder `data/`. Dapat diperbarui sesuai sumber resmi UPGRIS.")
    data_summary = get_data_summary()
    if data_summary:
        df_summary = pd.DataFrame(data_summary)
        df_summary.columns = ["File", "Ukuran", "Jumlah Key", "Keys"]
        df_summary.index = range(1, len(df_summary) + 1)
        st.dataframe(df_summary, use_container_width=True)

    with st.expander("Preview Data JSON"):
        all_data = load_all_json_files()
        if all_data:
            selected = st.selectbox("Pilih file:", list(all_data.keys()), format_func=lambda x: f"{x}.json")
            if selected:
                st.json(all_data[selected])

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div class="site-footer">
    <div class="footer-grid">
        <div class="footer-col">
            <h4>Universitas PGRI Semarang</h4>
            <p>{profil_data.get('alamat', 'Semarang, Jawa Tengah')}</p>
            <p>Telp: {profil_data.get('telepon', '(024) 8316377')}</p>
            <p>Website: <a href="{profil_data.get('website', '#')}" target="_blank">{profil_data.get('website', 'upgris.ac.id')}</a></p>
        </div>
        <div class="footer-col">
            <h4>Tautan Penting</h4>
            <ul>
                <li><a href="https://pmb.upgris.ac.id" target="_blank">PMB UPGRIS</a></li>
                <li><a href="https://informatika.upgris.ac.id" target="_blank">Prodi Informatika</a></li>
                <li><a href="https://upgris.ac.id" target="_blank">Website Resmi UPGRIS</a></li>
            </ul>
        </div>
        <div class="footer-col">
            <h4>Chatbot Akademik</h4>
            <p>Dibuat untuk tugas Teori Bahasa dan Otomata — Prodi Informatika UPGRIS.</p>
            <p>Menggunakan Finite State Machine & Rule-Based Keyword Matching.</p>
        </div>
    </div>
    <div class="footer-bottom">
        <p>Dibuat Oleh Kelompok Three Squad - Academic &middot; Program Studi Informatika UPGRIS</p>
    </div>
</div>
""", unsafe_allow_html=True)
