import streamlit as st
import random
import json
from datetime import datetime
from io import BytesIO

# 🎨 Warna teks
SSR_COLOR = "red"
SR_COLOR = "gold"
R_COLOR = "white"

# 🎯 Konstanta pity
SSR_PITY = 70
SR_PITY = 10

# 🖼️ Tampilkan header dengan gambar
st.image("https://i.ibb.co/CKF0V8w/love-deepspace-banner.jpg", use_container_width=True)
st.title("💖 Love and Deepspace - Gacha Simulator")

# =========================
# 📌 Fungsi untuk gacha
# =========================
def pull_gacha(banner_type):
    results = []
    pity_ssr = st.session_state.player_data.get("pity_ssr", 0)
    pity_sr = st.session_state.player_data.get("pity_sr", 0)

    for i in range(10):
        pity_ssr += 1
        pity_sr += 1

        # Cek pity SSR
        if pity_ssr >= SSR_PITY:
            rarity = "SSR"
            pity_ssr = 0
        # Cek pity SR
        elif pity_sr >= SR_PITY:
            rarity = "SR"
            pity_sr = 0
        else:
            roll = random.randint(1, 1000)
            if roll <= 10:  # 1% SSR
                rarity = "SSR"
                pity_ssr = 0
            elif roll <= 110:  # 10% SR
                rarity = "SR"
                pity_sr = 0
            else:
                rarity = "R"

        results.append(rarity)

        # Update jumlah kartu
        st.session_state.player_data[rarity.lower()] += 1

        # Simpan log
        log_line = f"{datetime.now()} - {banner_type} - {rarity}\n"
        with open("gacha_log.txt", "a", encoding="utf-8") as f:
            f.write(log_line)

    # Update pity
    st.session_state.player_data["pity_ssr"] = pity_ssr
    st.session_state.player_data["pity_sr"] = pity_sr

    return results

# =========================
# 📌 Fitur Input Data Player
# =========================
st.header("📥 Input Data Player")

tab1, tab2 = st.tabs(["✏️ Input Manual", "📂 Upload File Save"])

# Input manual
with tab1:
    player_name = st.text_input("Nama Player", "")
    ssr_count = st.number_input("Jumlah SSR", 0)
    sr_count = st.number_input("Jumlah SR", 0)
    r_count = st.number_input("Jumlah R", 0)
    pity_ssr = st.number_input("Pity SSR", 0, SSR_PITY)
    pity_sr = st.number_input("Pity SR", 0, SR_PITY)

    if st.button("Simpan Data Manual"):
        st.session_state.player_data = {
            "name": player_name,
            "ssr": ssr_count,
            "sr": sr_count,
            "r": r_count,
            "pity_ssr": pity_ssr,
            "pity_sr": pity_sr
        }
        st.success("✅ Data player tersimpan dari input manual!")

# Upload file save JSON
with tab2:
    uploaded_file = st.file_uploader("Upload file .json", type="json")
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        st.session_state.player_data = data
        st.success(f"✅ Data player {data.get('name', '')} berhasil dimuat!")

# =========================
# 📌 Inisialisasi default data player
# =========================
if "player_data" not in st.session_state:
    st.session_state.player_data = {
        "name": "",
        "ssr": 0,
        "sr": 0,
        "r": 0,
        "pity_ssr": 0,
        "pity_sr": 0
    }

# =========================
# 📌 Menu Gacha
# =========================
st.header("🎲 Gacha Simulator")

col1, col2 = st.columns(2)
with col1:
    if st.button("Gacha Banner Event"):
        results = pull_gacha("Event")
        for r in results:
            if r == "SSR":
                st.markdown(f"<span style='color:{SSR_COLOR}'>⭐ {r}</span>", unsafe_allow_html=True)
            elif r == "SR":
                st.markdown(f"<span style='color:{SR_COLOR}'>🌟 {r}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:{R_COLOR}'>✨ {r}</span>", unsafe_allow_html=True)

with col2:
    if st.button("Gacha Banner Standar"):
        results = pull_gacha("Standar")
        for r in results:
            if r == "SSR":
                st.markdown(f"<span style='color:{SSR_COLOR}'>⭐ {r}</span>", unsafe_allow_html=True)
            elif r == "SR":
                st.markdown(f"<span style='color:{SR_COLOR}'>🌟 {r}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:{R_COLOR}'>✨ {r}</span>", unsafe_allow_html=True)

# =========================
# 📌 Lihat Data Player
# =========================
st.header("📊 Statistik Player")
st.write(st.session_state.player_data)

# =========================
# 📌 Simpan Progress ke JSON
# =========================
st.header("💾 Simpan Progress")
if st.button("Download Save Data"):
    save_data = json.dumps(st.session_state.player_data)
    b = BytesIO(save_data.encode())
    st.download_button("📥 Download File Save", b, file_name="player_save.json")

# =========================
# 📌 Lihat Log Gacha
# =========================
st.header("📜 Log History")
try:
    with open("gacha_log.txt", "r", encoding="utf-8") as f:
        logs = f.readlines()

    keyword = st.text_input("🔍 Cari log (kata kunci / tanggal)")
    filtered_logs = [l for l in logs if keyword.lower() in l.lower()] if keyword else logs

    for line in filtered_logs:
        if "SSR" in line:
            st.markdown(f"<span style='color:{SSR_COLOR}'>{line}</span>", unsafe_allow_html=True)
        elif "SR" in line:
            st.markdown(f"<span style='color:{SR_COLOR}'>{line}</span>", unsafe_allow_html=True)
        else:
            st.text(line)

except FileNotFoundError:
    st.warning("Belum ada log gacha.")
