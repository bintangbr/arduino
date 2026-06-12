"""
FSM.py - Finite State Machine untuk Chatbot Akademik UPGRIS
===========================================================
Modul ini berisi definisi State (Enum) dan class AcademicFSM
yang mengimplementasikan konsep Finite State Machine:
  M = (Q, Σ, δ, q0, F)
"""

from enum import Enum, auto
from typing import Optional
from engine import detect_intent, get_response_by_intent


# ============================================================
# Q = Himpunan State
# ============================================================
class State(Enum):
    """Himpunan state (Q) dalam FSM Chatbot Akademik UPGRIS."""
    START = auto()
    IDLE = auto()
    DETECT_INTENT = auto()

    # State informasi akademik
    PROFIL_UPGRIS = auto()
    PROFIL_INFORMATIKA = auto()
    FAKULTAS_INFO = auto()
    PRODI_INFO = auto()
    DOSEN_INFO = auto()
    KURIKULUM_INFO = auto()
    PMB_INFO = auto()
    BIAYA_INFO = auto()
    BEASISWA_INFO = auto()
    MBKM_INFO = auto()
    KRS_INFO = auto()
    KHS_INFO = auto()
    IPK_INFO = auto()
    JADWAL_INFO = auto()
    SKRIPSI_INFO = auto()
    WISUDA_INFO = auto()
    PKL_INFO = auto()
    KKN_INFO = auto()
    LAYANAN_SURAT = auto()
    PENGADUAN_INFO = auto()
    FAQ_INFO = auto()

    # State khusus
    ERROR = auto()
    END = auto()


# Mapping dari nama intent ke State
INTENT_TO_STATE = {
    "profil_upgris": State.PROFIL_UPGRIS,
    "profil_informatika": State.PROFIL_INFORMATIKA,
    "fakultas": State.FAKULTAS_INFO,
    "prodi": State.PRODI_INFO,
    "dosen": State.DOSEN_INFO,
    "kurikulum": State.KURIKULUM_INFO,
    "pmb": State.PMB_INFO,
    "biaya": State.BIAYA_INFO,
    "beasiswa": State.BEASISWA_INFO,
    "mbkm": State.MBKM_INFO,
    "krs": State.KRS_INFO,
    "khs": State.KHS_INFO,
    "ipk": State.IPK_INFO,
    "jadwal": State.JADWAL_INFO,
    "skripsi": State.SKRIPSI_INFO,
    "wisuda": State.WISUDA_INFO,
    "pkl": State.PKL_INFO,
    "kkn": State.KKN_INFO,
    "layanan_surat": State.LAYANAN_SURAT,
    "pengaduan": State.PENGADUAN_INFO,
    "faq": State.FAQ_INFO,
}


class AcademicFSM:
    """
    Implementasi Finite State Machine untuk Chatbot Akademik UPGRIS.

    Definisi formal:
        M = (Q, Σ, δ, q0, F)
        Q  = himpunan state (class State)
        Σ  = input teks pertanyaan pengguna
        δ  = fungsi transisi (method process_input)
        q0 = START
        F  = {IDLE, END}
    """

    def __init__(self) -> None:
        self.current_state: State = State.START
        self.previous_state: Optional[State] = None
        self.transition_history: list[dict] = []
        self.last_intent: Optional[str] = None
        self.last_input: str = ""

        # Transisi awal START → IDLE
        self.transition_to(State.IDLE, input_text="Aplikasi dijalankan", intent="init")

    # --------------------------------------------------------
    # Fungsi transisi
    # --------------------------------------------------------
    def transition_to(self, new_state: State, input_text: str = "", intent: str = "") -> None:
        """Melakukan transisi dari current_state ke new_state dan mencatat riwayat."""
        self.previous_state = self.current_state
        from_state = self.current_state.name
        self.current_state = new_state
        self.last_input = input_text
        if intent:
            self.last_intent = intent

        self.transition_history.append({
            "from": from_state,
            "to": new_state.name,
            "input": input_text[:80] if input_text else "",
            "intent": intent,
        })

    # --------------------------------------------------------
    # Reset FSM
    # --------------------------------------------------------
    def reset(self) -> None:
        """Reset FSM ke kondisi awal: START → IDLE."""
        self.current_state = State.START
        self.previous_state = None
        self.transition_history = []
        self.last_intent = None
        self.last_input = ""
        self.transition_to(State.IDLE, input_text="Reset FSM", intent="init")

    # --------------------------------------------------------
    # Proses input utama
    # --------------------------------------------------------
    def process_input(self, user_input: str) -> dict:
        """
        Memproses input pengguna melalui alur FSM:
        IDLE → DETECT_INTENT → STATE_INFO → IDLE
        Jika intent tidak dikenali:
        IDLE → DETECT_INTENT → ERROR → IDLE

        Returns:
            dict berisi response, intent, state, accepted, transition
        """
        # 1. IDLE → DETECT_INTENT
        self.transition_to(State.DETECT_INTENT, input_text=user_input, intent="detecting")

        # 2. Deteksi intent dari input
        intent = detect_intent(user_input)

        # 3. Tentukan state tujuan berdasarkan intent
        if intent and intent in INTENT_TO_STATE:
            target_state = INTENT_TO_STATE[intent]
            accepted = True
        else:
            target_state = State.ERROR
            intent = "unknown"
            accepted = False

        # 4. DETECT_INTENT → STATE_INFO / ERROR
        self.transition_to(target_state, input_text=user_input, intent=intent)

        # 5. Ambil response
        response = get_response_by_intent(intent, user_input)

        # 6. STATE_INFO / ERROR → IDLE
        self.transition_to(State.IDLE, input_text="Response selesai", intent=intent)

        # Bangun string transisi
        transition_str = f"IDLE → DETECT_INTENT → {target_state.name} → IDLE"

        return {
            "response": response,
            "intent": intent,
            "state": target_state.name,
            "accepted": accepted,
            "transition": transition_str,
        }

    # --------------------------------------------------------
    # Getter
    # --------------------------------------------------------
    def get_current_state(self) -> str:
        """Mengembalikan nama state saat ini."""
        return self.current_state.name

    def get_transition_history(self) -> list[dict]:
        """Mengembalikan seluruh riwayat transisi."""
        return self.transition_history

    def get_transition_table(self) -> list[dict]:
        """
        Mengembalikan tabel transisi FSM lengkap.
        Digunakan untuk menampilkan di UI.
        """
        table = [
            {
                "state_awal": "START",
                "input": "Aplikasi dijalankan",
                "state_tujuan": "IDLE",
                "output": "Sapaan awal chatbot",
            },
            {
                "state_awal": "IDLE",
                "input": "User mengirim pertanyaan",
                "state_tujuan": "DETECT_INTENT",
                "output": "Sistem memproses input",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword profil UPGRIS",
                "state_tujuan": "PROFIL_UPGRIS",
                "output": "Menampilkan profil UPGRIS",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword profil Informatika",
                "state_tujuan": "PROFIL_INFORMATIKA",
                "output": "Menampilkan profil Informatika",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword fakultas",
                "state_tujuan": "FAKULTAS_INFO",
                "output": "Menampilkan informasi fakultas",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword prodi",
                "state_tujuan": "PRODI_INFO",
                "output": "Menampilkan informasi prodi",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword dosen",
                "state_tujuan": "DOSEN_INFO",
                "output": "Menampilkan informasi dosen",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword kurikulum",
                "state_tujuan": "KURIKULUM_INFO",
                "output": "Menampilkan informasi kurikulum",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword PMB",
                "state_tujuan": "PMB_INFO",
                "output": "Menampilkan informasi PMB",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword biaya",
                "state_tujuan": "BIAYA_INFO",
                "output": "Menampilkan informasi biaya",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword beasiswa",
                "state_tujuan": "BEASISWA_INFO",
                "output": "Menampilkan informasi beasiswa",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword MBKM",
                "state_tujuan": "MBKM_INFO",
                "output": "Menampilkan informasi MBKM",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword KRS",
                "state_tujuan": "KRS_INFO",
                "output": "Menampilkan informasi KRS",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword KHS",
                "state_tujuan": "KHS_INFO",
                "output": "Menampilkan informasi KHS",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword IPK",
                "state_tujuan": "IPK_INFO",
                "output": "Menampilkan informasi IPK",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword jadwal",
                "state_tujuan": "JADWAL_INFO",
                "output": "Menampilkan informasi jadwal",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword skripsi",
                "state_tujuan": "SKRIPSI_INFO",
                "output": "Menampilkan informasi skripsi",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword wisuda",
                "state_tujuan": "WISUDA_INFO",
                "output": "Menampilkan informasi wisuda",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword layanan surat",
                "state_tujuan": "LAYANAN_SURAT",
                "output": "Menampilkan informasi layanan surat",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword pengaduan",
                "state_tujuan": "PENGADUAN_INFO",
                "output": "Menampilkan informasi pengaduan",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword FAQ / bantuan",
                "state_tujuan": "FAQ_INFO",
                "output": "Menampilkan FAQ / bantuan",
            },
            {
                "state_awal": "DETECT_INTENT",
                "input": "Keyword tidak dikenali",
                "state_tujuan": "ERROR",
                "output": "Fallback dan rekomendasi pertanyaan",
            },
            {
                "state_awal": "STATE_INFO (semua)",
                "input": "Response selesai",
                "state_tujuan": "IDLE",
                "output": "Siap menerima pertanyaan berikutnya",
            },
            {
                "state_awal": "ERROR",
                "input": "Response fallback selesai",
                "state_tujuan": "IDLE",
                "output": "Siap menerima pertanyaan berikutnya",
            },
        ]
        return table
