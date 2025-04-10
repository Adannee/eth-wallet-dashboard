import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import requests
from matplotlib.backends.backend_pdf import PdfPages
from io import BytesIO

def all_figs_to_pdf(figures):
    buf = BytesIO()
    with PdfPages(buf) as pdf:
        for fig in figures:
            pdf.savefig(fig, bbox_inches='tight')
    buf.seek(0)
    return buf

st.set_page_config(layout="wide", page_title="EtherScan Wallet Dashboard")

ETHERSCAN_API_KEY = st.secrets["ETHERSCAN_API_KEY"]

st.sidebar.title("Wallet Lookup")

wallet_address = st.sidebar.text_input("Paste Ethereum address", placeholder="0x...")
fetch_button = st.sidebar.button("Fetch Transactions")

use_sample = False
df = None

if fetch_button and wallet_address.startswith("0x"):
    with st.spinner("Fetching transactions..."):
        url = (
            f"https://api.etherscan.io/api?module=account&action=txlist"
            f"&address={wallet_address}&startblock=0&endblock=99999999"
            f"&page=1&offset=10000&sort=asc&apikey={ETHERSCAN_API_KEY}"
        )
        response = requests.get(url)
        data = response.json()

        if data["status"] == "1":
            txs = data["result"]
            df = pd.DataFrame(txs)
            df["timestamp"] = pd.to_datetime(df["timeStamp"], unit="s")
            df["date"] = df["timestamp"].dt.date
            df["gas price (Gwei)"] = df["gas price (Gwei)"].astype(float)
            df["gas used"] = df["gas used"].astype(float)
            df["value (ETH)"] = df["value (ETH)"].astype(float) / 1e18
            df["tx fee (ETH)"] = (df["gas price (Gwei)"] * df["gas used"]) / 1e18
            df["success"] = df["isError"].astype(int) == 0
        else:
            st.error(f"No transactions found or error: {data.get('message', '')}")


st.sidebar.title("Upload CSV")
uploaded_file = st.sidebar.file_uploader("Upload Transaction CSV", type=["csv"])


if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

  
    st.sidebar.title("Filters")
    date_range = st.sidebar.date_input("Select date range", [df["date"].min(), df["date"].max()])
    show_failed = st.sidebar.checkbox("Include failed transactions", value=False)

   
    df_filtered = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]
    if not show_failed:
        df_filtered = df_filtered[df_filtered["success"] == True]


    st.title("EtherScan Wallet Transaction Dashboard")
    st.markdown(f"Transactions from **{df['from'].iloc[0]}** to {df_filtered['to'].nunique()} addresses")

  
    col1, col2, col3 = st.columns(3)
    col1.metric("Total ETH Sent", f"{df_filtered['value (ETH)'].sum():.4f} ETH")
    col2.metric("Total Tx Fees", f"{df_filtered['tx fee (ETH)'].sum():.4f} ETH")
    col3.metric("Transactions", f"{len(df_filtered)}")

    
    st.subheader("💸 Transaction Fees Over Time")
    fig1, ax1 = plt.subplots(figsize=(10,4))
    sns.lineplot(data=df_filtered, x="timestamp", y="tx fee (ETH)", ax=ax1)
    ax1.set_title("Transaction Fee (ETH) Over Time")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)

    
    st.subheader("📆 ETH Sent Per Day")
    eth_daily = df_filtered.groupby("date")["value (ETH)"].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10,4))
    sns.barplot(data=eth_daily, x="date", y="value (ETH)", ax=ax2)
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

    
    st.subheader("⛽ Gas Used Distribution")
    fig3, ax3 = plt.subplots(figsize=(10,4))
    sns.histplot(df_filtered["gas used"], bins=30, ax=ax3, kde=True)
    st.pyplot(fig3)

    
    st.subheader("✅ Transaction Success Rate")
    fig4, ax4 = plt.subplots()
    df_filtered["success"].value_counts().plot.pie(
        labels=["Success", "Failed"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#FF5722"],
        ax=ax4
    )
    ax4.set_ylabel("")
    st.pyplot(fig4)

    
    st.subheader("📄 Export Full Dashboard as PDF")
    st.download_button(
        label="Download All Charts as PDF",
        data=all_figs_to_pdf([fig1, fig2, fig3, fig4]),
        file_name="eth_wallet_dashboard.pdf",
        mime="application/pdf"
    )

else:
    st.info("Upload a CSV file to begin.")
