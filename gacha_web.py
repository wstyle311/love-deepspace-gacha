import streamlit as st
import random
import os
import datetime

LOG_FILE = "gacha_log.txt"

SSR_COLOR = "red"
SR_COLOR = "gold"
R_COLOR = "white"

SSR_RATE = 0.015  # 1.5%
SR_RATE = 0.13    # 13%
SSR_PITY = 70
SR_PITY = 10

class GachaSimulator:
    def __init__(self):
        self.ssr_count = 0
        self.sr_count = 0
        self.r_count = 0
        self.ssr_pity_counter = 0
        self.sr_pity_counter = 0

    def gacha_pull(self, banner_type, pulls):
        results = []
        for _ in range(pulls):
            self.ssr_pity_counter += 1
            self.sr_pity_counter += 1

            if self.ssr_pity_counter >= SSR_PITY:
                rarity = "SSR"
                self.ssr_pity_counter = 0
                self.sr_pity_counter = 0
            elif self.sr_pity_counter >= SR_PITY:
                rarity = "SR"
                self.sr_pity_counter = 0
            else:
                roll = random.random()
                if roll < SSR_RATE:
                    rarity = "SSR"
                    self.ssr_pity_counter = 0
                    self.sr_pity_counter = 0
                elif roll < SSR_RATE + SR_RATE:
                    rarity = "SR"
                    self.sr_pity_counter = 0
                else:
                    rarity = "R"

            results.append((rarity, banner_type))
            self._update_counts(rarity)
            self._save_log(rarity, banner_type)
        return results

    def _update_counts(self, rarity):
        if rarity == "SSR":
            self.ssr_count += 1
        elif rarity == "SR":
            self.sr_count += 1
        else:
            self.r_count += 1

    def _save_log(self, rarity, banner_type):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.date.today()} | {banner_type} | {rarity}\n")

    def read_log(self):
        if not os.path.exists(LOG_FILE):
            return []
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def search_log(self, keyword=None, date_filter=None):
        logs = self.read_log()
        results = []
        for line in logs:
            if date_filter and not line.startswith(date_filter):
                continue
            if keyword and keyword.lower() not in line.lower():
                continue
            results.append(line)
        return results

def color_text(text):
    if "SSR" in text:
        return f"<span style='color:{SSR_COLOR};font-weight:bold'>{text}</span>"
    elif "SR" in text:
        return f"<span style='color:{SR_COLOR};font-weight:bold'>{text}</span>"
    else:
        return f"<span style='color:{R_COLOR}'>{text}</span>"

st.set_page_config(page_title="Love and Deepspace Gacha Simulator", layout="centered")
st.title("🎯 Love and Deepspace Gacha Simulator")

sim = GachaSimulator()

menu = st.sidebar.selectbox("Menu", ["Gacha", "Lihat Log", "Cari Log"])

if menu == "Gacha":
    banner = st.selectbox("Pilih Banner", ["Event", "Standard"])
    pulls = st.number_input("Jumlah Pull", min_value=1, max_value=100, step=1)
    if st.button("Mulai Gacha"):
        results = sim.gacha_pull(banner, pulls)
        st.subheader("Hasil Gacha:")
        for rarity, btype in results:
            st.markdown(color_text(f"{btype} | {rarity}"), unsafe_allow_html=True)
        st.info(f"Total SSR: {sim.ssr_count} | SR: {sim.sr_count} | R: {sim.r_count}")

elif menu == "Lihat Log":
    logs = sim.read_log()
    if logs:
        st.subheader("Log Gacha:")
        for line in logs:
            st.markdown(color_text(line), unsafe_allow_html=True)
    else:
        st.warning("Belum ada log gacha.")

elif menu == "Cari Log":
    mode = st.radio("Pilih mode pencarian:", ["Tanggal", "Kata Kunci", "Gabungan"])
    date_filter = None
    keyword = None

    if mode == "Tanggal":
        date_filter = st.date_input("Pilih tanggal")
        date_filter = str(date_filter)
    elif mode == "Kata Kunci":
        keyword = st.text_input("Masukkan kata kunci (contoh: SSR)")
    elif mode == "Gabungan":
        date_filter = st.date_input("Pilih tanggal")
        date_filter = str(date_filter)
        keyword = st.text_input("Masukkan kata kunci (contoh: SSR)")

    if st.button("Cari"):
        results = sim.search_log(keyword=keyword, date_filter=date_filter)
        if results:
            for line in results:
                st.markdown(color_text(line), unsafe_allow_html=True)
        else:
            st.warning("Tidak ada hasil yang cocok.")
