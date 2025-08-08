import streamlit as st
import random
import json
import os
from datetime import datetime
from io import BytesIO

# ===================== CONFIGURASI WEB =====================
st.set_page_config(page_title="Love and Deepspace Gacha Simulator", layout="wide")

# Header Image
header_url = "https://drive.google.com/uc?export=view&id=1HF_kmZMz0mIpA6yYgaryBJccK9-eULRz"
st.image(header_url, use_column_width=True)

st.markdown(
    """
    <style>
    .banner-card {
        background-color: #2a2a2a;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        transition: transform 0.2s;
    }
    .banner-card:hover {
        transform: scale(1.02);
    }
    .banner-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===================== SISTEM SIMULATOR =====================
SSR_RATE = 0.015
SR_RATE = 0.10
SSR_PITY = 70
SR_PITY = 10

if "log" not in st.session_state:
    st.session_state.log = []
if "player_data" not in st.session_state:
    st.session_state.player_data = {
        "name": "",
        "ssr": 0,
        "sr": 0,
        "r": 0,
        "pity_ssr": 0,
        "pity_sr": 0
    }

# ===================== INPUT DATA PLAYER =====================
st.header("📋 Data Player")
with st.expander("Masukkan / Ubah Data Player"):
    name = st.text_input("Nama Player", st.session_state.player_data["name"])
    ssr_count = st.number_input("Jumlah SSR dimiliki", value=st.session_state.player_data["ssr"])
    sr_count = st.number_input("Jumlah SR dimiliki", value=st.session_state.player_data["sr"])
    r_count = st.number_input("Jumlah R dimiliki", value=st.session_state.player_data["r"])
    pity_ssr = st.number_input("Pity SSR saat ini", value=st.session_state.player_data["pity_ssr"], min_value=0, max_value=SSR_PITY)
    pity_sr = st.number_input("Pity SR saat ini", value=st.session_state.player_data["pity_sr"], min_value=0, max_value=SR_PITY)

    if st.button("💾 Simpan Data Player"):
        st.session_state.player_data.update({
            "name": name,
            "ssr": ssr_count,
            "sr": sr_count,
            "r": r_count,
            "pity_ssr": pity_ssr,
            "pity_sr": pity_sr
        })
        st.success("Data player berhasil diperbarui!")

# ===================== FILE SAVE SYSTEM =====================
st.subheader("📂 File Save Player")
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload file save (.json)", type="json")
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        st.session_state.player_data = data
        st.success(f"Data player {data['name']} berhasil dimuat!")

with col2:
    if st.button("💾 Download Save"):
        save_bytes = json.dumps(st.session_state.player_data).encode()
        st.download_button("Download File Save", save_bytes, file_name="player_save.json")

# ===================== SISTEM GACHA =====================
def do_gacha(pulls, banner):
    results = []
    for _ in range(pulls):
        st.session_state.player_data["pity_ssr"] += 1
        st.session_state.player_data["pity_sr"] += 1

        # Pity SSR
        if st.session_state.player_data["pity_ssr"] >= SSR_PITY:
            rarity = "SSR"
        elif st.session_state.player_data["pity_sr"] >= SR_PITY:
            rarity = "SR"
        else:
            roll = random.random()
            if roll < SSR_RATE:
                rarity = "SSR"
            elif roll < SSR_RATE + SR_RATE:
                rarity = "SR"
            else:
                rarity = "R"

        # Reset pity jika SSR/SR keluar
        if rarity == "SSR":
            st.session_state.player_data["ssr"] += 1
            st.session_state.player_data["pity_ssr"] = 0
            st.session_state.player_data["pity_sr"] = 0
        elif rarity == "SR":
            st.session_state.player_data["sr"] += 1
            st.session_state.player_data["pity_sr"] = 0
        else:
            st.session_state.player_data["r"] += 1

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {banner} | {rarity}"
        st.session_state.log.append(log_entry)

        # Simpan ke file log
        with open("gacha_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

        results.append(rarity)
    return results

# ===================== PILIH BANNER =====================
st.header("🎯 Pilih Banner")
col_event, col_standard = st.columns(2)

with col_event:
    st.markdown('<div class="banner-card"><div class="banner-title">Banner Event</div>', unsafe_allow_html=True)
    if st.button("1x Pull Event"):
        do_gacha(1, "Event")
    if st.button("10x Pull Event"):
        do_gacha(10, "Event")
    st.markdown('</div>', unsafe_allow_html=True)

with col_standard:
    st.markdown('<div class="banner-card"><div class="banner-title">Banner Standar</div>', unsafe_allow_html=True)
    if st.button("1x Pull Standar"):
        do_gacha(1, "Standar")
    if st.button("10x Pull Standar"):
        do_gacha(10, "Standar")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== HISTORY LOG =====================
st.header("📜 Log History")
with st.expander("Lihat Semua Log"):
    for entry in reversed(st.session_state.log):
        if "SSR" in entry:
            st.markdown(f"<span style='color: gold; font-weight: bold;'>{entry}</span>", unsafe_allow_html=True)
        elif "SR" in entry:
            st.markdown(f"<span style='color: violet;'>{entry}</span>", unsafe_allow_html=True)
        else:
            st.text(entry)

# ===================== PENCARIAN LOG =====================
st.subheader("🔍 Cari di Log")
keyword = st.text_input("Kata kunci (contoh: SSR)")
date_filter = st.date_input("Filter Tanggal", value=None)

if st.button("Cari Log"):
    with open("gacha_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    filtered = []
    for line in lines:
        if keyword and keyword.lower() not in line.lower():
            continue
        if date_filter and date_filter.strftime("%Y-%m-%d") not in line:
            continue
        filtered.append(line.strip())

    if filtered:
        for entry in filtered:
            if "SSR" in entry:
                st.markdown(f"<span style='color: gold; font-weight: bold;'>{entry}</span>", unsafe_allow_html=True)
            elif "SR" in entry:
                st.markdown(f"<span style='color: violet;'>{entry}</span>", unsafe_allow_html=True)
            else:
                st.text(entry)
    else:
        st.warning("Tidak ada hasil ditemukan.")
