from datetime import date
from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

DB = Path(__file__).parent / "casa.db"
conn = sqlite3.connect(DB, check_same_thread=False)
conn.executescript("""
CREATE TABLE IF NOT EXISTS spese (id INTEGER PRIMARY KEY AUTOINCREMENT,
 data TEXT, descrizione TEXT, categoria TEXT, importo REAL, ricorrenza TEXT);
""")

st.set_page_config(page_title="Gestionale Casa", page_icon="🏠", layout="wide")
st.title("🏠 Gestionale Casa")

with st.form("f_sp", clear_on_submit=True):
    c1, c2, c3, c4 = st.columns([1, 2, 1.5, 1])
    dt = c1.date_input("Data", value=date.today())
    ds = c2.text_input("Descrizione")
    ct = c3.selectbox("Categoria", ["Bollette", "Manutenzione", "Arredo", "Altro"])
    im = c4.number_input("Importo €", min_value=0.0, step=1.0)
    if st.form_submit_button("Aggiungi", type="primary"):
        if ds.strip() and im > 0:
            conn.execute(
                "INSERT INTO spese (data,descrizione,categoria,importo,ricorrenza)"
                " VALUES (?,?,?,?,?)",
                (dt.isoformat(), ds.strip(), ct, im, "una tantum"))
            conn.commit()
            st.rerun()

df = pd.read_sql_query("SELECT * FROM spese ORDER BY data DESC", conn)
if df.empty:
    st.info("Nessuna spesa registrata. Aggiungi la prima! 👆")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.write(f"**Totale: €{df['importo'].sum():,.2f}**")
