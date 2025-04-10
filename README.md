# EtherScan Wallet Dashboard

A Streamlit-based web dashboard to analyze Ethereum wallet transactions using the Etherscan API or uploaded CSV files. Visualize gas fees, ETH volume, success rates, and more — with full PDF export support.

---

##  Features

-  Fetch transactions from **any Ethereum address** via Etherscan
-  Upload your own **CSV file** for offline analysis
-  Visualize:
  - Transaction fee trends
  - ETH sent per day
  - Gas usage distribution
  - Success vs failed transactions
-  Filter by date range or success
-  Export full dashboard as **PDF**

---

## Tech Stack

- [Streamlit](https://streamlit.io/) for the interactive web app
- [Etherscan API](https://docs.etherscan.io/) for real-time wallet data
- [Pandas](https://pandas.pydata.org/) for data wrangling
- [Seaborn](https://seaborn.pydata.org/) + [Matplotlib](https://matplotlib.org/) for visualizations

---

## 📁 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/etherscan-wallet-dashboard.git
cd etherscan-wallet-dashboard
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Add Etherscan API Key
#### Create a .streamlit/secrets.toml file:
```toml
ETHERSCAN_API_KEY = "your_api_key_here"
```
### 4. Run the App
```bash
streamlit run app.py
```
Then visit https://etherscanscraper.streamlit.app/

---
