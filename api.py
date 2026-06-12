"""
api.py - REST API untuk Chatbot Akademik UPGRIS
================================================
Menyediakan endpoint API agar chatbot FSM bisa diakses
dari landing page website atau aplikasi eksternal.

Jalankan: uvicorn api:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uuid

from FSM import AcademicFSM
from utils import CONTOH_PERTANYAAN, get_data_summary, export_transitions_csv


# ============================================================
# Pydantic Models
# ============================================================
class ChatRequest(BaseModel):
    """Request body untuk endpoint chat."""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response body dari endpoint chat."""
    session_id: str
    response: str
    intent: str
    state: str
    accepted: bool
    transition: str
    current_state: str
    total_transitions: int


class ResetRequest(BaseModel):
    """Request body untuk reset session."""
    session_id: str


class StatusResponse(BaseModel):
    """Response body untuk status FSM."""
    session_id: str
    current_state: str
    last_intent: Optional[str]
    total_transitions: int
    transition_history: list[dict]


# ============================================================
# App & Session Store
# ============================================================
app = FastAPI(
    title="Chatbot Akademik UPGRIS API",
    description=(
        "REST API untuk Chatbot Akademik UPGRIS berbasis Finite State Machine. "
        "Dibuat untuk tugas Teori Bahasa dan Otomata — Prodi Informatika UPGRIS."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — izinkan semua origin agar bisa diakses dari landing page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Penyimpanan session (in-memory)
# Setiap session memiliki instance FSM sendiri
sessions: dict[str, AcademicFSM] = {}

MAX_SESSIONS = 500  # Batas maksimal session aktif


def get_or_create_session(session_id: Optional[str] = None) -> tuple[str, AcademicFSM]:
    """Mendapatkan session yang ada atau membuat session baru."""
    if session_id and session_id in sessions:
        return session_id, sessions[session_id]

    # Buat session baru
    new_id = str(uuid.uuid4())[:8]
    # Bersihkan session lama jika terlalu banyak
    if len(sessions) >= MAX_SESSIONS:
        oldest_key = next(iter(sessions))
        del sessions[oldest_key]

    sessions[new_id] = AcademicFSM()
    return new_id, sessions[new_id]


# ============================================================
# Endpoints
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Halaman root — redirect ke docs."""
    return """
    <html>
    <head><title>Chatbot Akademik UPGRIS API</title></head>
    <body style="font-family: Inter, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; background: #f8fafc;">
        <div style="text-align: center; background: white; padding: 3rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h1 style="color: #1e1b4b;">🎓 Chatbot Akademik UPGRIS API</h1>
            <p style="color: #64748b;">REST API berbasis Finite State Machine</p>
            <div style="margin-top: 1.5rem; display: flex; gap: 1rem; justify-content: center;">
                <a href="/docs" style="background: #4338ca; color: white; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;">📄 API Docs (Swagger)</a>
                <a href="/redoc" style="background: #6366f1; color: white; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;">📘 ReDoc</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Mengirim pesan ke chatbot dan mendapatkan respons.

    - Kirim `message` berisi pertanyaan pengguna.
    - Opsional kirim `session_id` untuk melanjutkan sesi sebelumnya.
    - Jika `session_id` tidak dikirim, akan dibuat sesi baru.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong.")

    session_id, fsm = get_or_create_session(request.session_id)

    # Proses melalui FSM
    result = fsm.process_input(request.message.strip())

    return ChatResponse(
        session_id=session_id,
        response=result["response"],
        intent=result["intent"],
        state=result["state"],
        accepted=result["accepted"],
        transition=result["transition"],
        current_state=fsm.get_current_state(),
        total_transitions=len(fsm.get_transition_history()),
    )


@app.post("/api/reset")
async def reset_session(request: ResetRequest):
    """Reset sesi chatbot ke kondisi awal."""
    if request.session_id in sessions:
        sessions[request.session_id].reset()
        return {
            "status": "ok",
            "message": "Sesi berhasil direset.",
            "session_id": request.session_id,
        }
    else:
        raise HTTPException(status_code=404, detail="Session ID tidak ditemukan.")


@app.get("/api/status/{session_id}", response_model=StatusResponse)
async def get_status(session_id: str):
    """Mendapatkan status FSM dari sesi tertentu."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session ID tidak ditemukan.")

    fsm = sessions[session_id]
    return StatusResponse(
        session_id=session_id,
        current_state=fsm.get_current_state(),
        last_intent=fsm.last_intent,
        total_transitions=len(fsm.get_transition_history()),
        transition_history=fsm.get_transition_history(),
    )


@app.get("/api/suggestions")
async def get_suggestions():
    """Mendapatkan daftar contoh pertanyaan."""
    return {
        "suggestions": CONTOH_PERTANYAAN,
    }


@app.get("/api/transition-table")
async def get_transition_table():
    """Mendapatkan tabel transisi FSM."""
    fsm = AcademicFSM()
    return {
        "transition_table": fsm.get_transition_table(),
    }


@app.get("/api/data-summary")
async def get_data_summary_api():
    """Mendapatkan ringkasan dataset akademik."""
    return {
        "data_summary": get_data_summary(),
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Chatbot Akademik UPGRIS API",
        "active_sessions": len(sessions),
    }
