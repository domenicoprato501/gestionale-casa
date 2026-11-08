#!/usr/bin/env bash
set -e
CARTELLA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$HOME/gestionale-venv"
if [ ! -d "$VENV" ]; then
    echo "🔧 Creo il venv..."
    python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"
if ! python -c "import streamlit, pandas, firebase_admin" 2>/dev/null; then
    echo "📦 Installo dipendenze..."
    pip install --quiet streamlit pandas firebase-admin
fi
echo "🚀 Avvio su http://localhost:8501"
exec streamlit run "$CARTELLA/app.py"
