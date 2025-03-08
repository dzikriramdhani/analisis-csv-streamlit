import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Analisis CSV: Jumlah Barang per Varian & Ukuran")
st.title("📊 Analisis CSV: Jumlah Barang per Varian & Ukuran")

# Upload file CSV
uploaded_file = st.file_uploader("📂 Upload file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Membaca file CSV
        df = pd.read_csv(uploaded_file, encoding="utf-8", sep=None, engine="python")  # Auto-deteksi delimiter

        # Cek apakah kolom yang dibutuhkan ada
        if "Variation" not in df.columns or "Quantity" not in df.columns:
            st.error("⚠️ Error: Kolom 'Variation' dan 'Quantity' tidak ditemukan dalam file CSV!")
        else:
            # Pisahkan varian dan ukuran
            df[['Varian', 'Ukuran']] = df['Variation'].str.split(',', n=1, expand=True)
            df['Varian'] = df['Varian'].str.strip()
            df['Ukuran'] = df['Ukuran'].str.strip()

            # Konversi Quantity ke angka
            df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

            # Hitung jumlah barang berdasarkan varian & ukuran
            result = df.groupby(['Varian', 'Ukuran'])['Quantity'].sum().reset_index()

            # Hitung total keseluruhan barang
            total_barang = result["Quantity"].sum()

            # Tampilkan hasil dalam tabel
            st.subheader("📋 Hasil Analisis:")
            st.dataframe(result)

            # Menampilkan total keseluruhan barang
            st.markdown(f"### 🔢 Total Keseluruhan Barang: **{total_barang}**")

            # Unduh hasil sebagai CSV
            csv = result.to_csv(index=False).encode("utf-8")
            st.download_button(label="📥 Download Hasil CSV", data=csv, file_name="hasil_analisis.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {str(e)}")
