import streamlit as st
import pandas as pd

# ============================================================
# Defaults (export vars)
# ============================================================
DEFAULTS = {
    "Ca": 80.0, "c": 0.75, "Ta": 60.0, "t": 0.22, "Ia": 70.0, "G": 90.0, "b": 40.0,
    "M": 250.0, "P": 1.0, "k": 0.25, "h": 200.0,
    "EXNa": 5.0, "m": 0.18, "n": 15.0, "sigma": 60.0, "rf": 0.04,
    "DefTot": 0.0, "phi": 0.0
}

KEYS = list(DEFAULTS.keys())

PRESETS = {
    "Economie stabila": {**DEFAULTS},
    "Recesiune": {
        "Ca": 70.0, "c": 0.72, "Ta": 65.0, "t": 0.22, "Ia": 55.0, "G": 95.0, "b": 45.0,
        "M": 260.0, "P": 1.0, "k": 0.25, "h": 210.0,
        "EXNa": 0.0, "m": 0.20, "n": 15.0, "sigma": 55.0, "rf": 0.04,
        "DefTot": 10.0, "phi": 0.8
    },
}

TOOLTIP = {
    "Ca": "Consum autonom (mld lei)",
    "c": "Inclinația marginală spre consum (0..1)",
    "Ta": "Taxe autonome (mld lei)",
    "t": "Rata de impozitare (0..1)",
    "Ia": "Investiții autonome (mld lei)",
    "G": "Cheltuieli guvernamentale (mld lei)",
    "b": "Sensibilitatea investițiilor la r",
    "M": "Masa monetară (mld lei)",
    "P": "Nivelul prețurilor (>0)",
    "k": "Cererea de bani tranzacțională (0..1)",
    "h": "Cererea de bani speculativă (>0)",
    "EXNa": "Export net autonom",
    "m": "Înclinația spre import (0..1)",
    "n": "Sensibilitatea EXN la r",
    "sigma": "Mobilitatea capitalului (>=0)",
    "rf": "Rata dobânzii externe",
    "DefTot": "Deficit bugetar total",
    "phi": "Sensibilitatea primei de risc (>=0)",
}

# ============================================================
# State helpers
# ============================================================
def init_state():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = float(v)

def apply_preset(name: str):
    if name in PRESETS:
        for k, v in PRESETS[name].items():
            st.session_state[k] = float(v)
        st.rerun()  # refresh immediately

def reset_defaults():
    for k, v in DEFAULTS.items():
        st.session_state[k] = float(v)
    st.rerun()  # refresh immediately

# ============================================================
# UI
# ============================================================
st.set_page_config(page_title="Model IS-LM-BP (Streamlit)", layout="wide")
st.title("Model IS–LM–BP — Parametri")
st.caption("Pasul 1: variabile + preseturi afișate în pagină (fără calcule încă).")

init_state()

col_left, col_right = st.columns([1, 2], gap="large")

with col_left:
    st.subheader("Preseturi")
    preset_names = ["-- Alege preset --"] + sorted(PRESETS.keys())
    chosen = st.selectbox("Selectează preset", preset_names, index=0)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Aplică preset", disabled=(chosen == "-- Alege preset --"), use_container_width=True):
            apply_preset(chosen)
    with c2:
        if st.button("Reset default", use_container_width=True):
            reset_defaults()

    st.divider()
    st.subheader("Editare parametri")
    st.caption("Valorile sunt în `st.session_state` și se sincronizează cu preseturile.")

    with st.expander("Politica Fiscala (IS)", expanded=True):
        for k in ["Ca", "c", "Ta", "t", "Ia", "G", "b"]:
            st.number_input(
                k,
                key=k,                       # IMPORTANT: same key as variable
                help=TOOLTIP.get(k, ""),
                step=0.01,
                format="%.6f",
            )

    with st.expander("Politica Monetara (LM)", expanded=False):
        for k in ["M", "P", "k", "h"]:
            st.number_input(
                k,
                key=k,
                help=TOOLTIP.get(k, ""),
                step=0.01,
                format="%.6f",
            )

    with st.expander("Sector Extern (BP)", expanded=False):
        for k in ["EXNa", "m", "n", "sigma", "rf"]:
            st.number_input(
                k,
                key=k,
                help=TOOLTIP.get(k, ""),
                step=0.01,
                format="%.6f",
            )

    with st.expander("Fiscal - Deficit", expanded=False):
        for k in ["DefTot", "phi"]:
            st.number_input(
                k,
                key=k,
                help=TOOLTIP.get(k, ""),
                step=0.01,
                format="%.6f",
            )

with col_right:
    st.subheader("Valori curente")
    params = {k: float(st.session_state[k]) for k in KEYS}
    df = pd.DataFrame([{"Key": k, "Value": params[k]} for k in KEYS])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("JSON (copy/paste)")
    st.code(params, language="json")