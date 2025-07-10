# PhonePe-Transaction-Insights-
# 📊 PhonePe Transaction Insights

A data analytics and visualization project built using PhonePe Pulse public data. The project extracts, transforms, stores, and visualizes UPI transaction patterns across India from 2018 to 2022 using PostgreSQL, Streamlit, and Plotly.

---

## 📁 Project Structure

- `app.py` – Streamlit dashboard script
- `data/` – JSON files extracted from PhonePe Pulse GitHub
- `etl_script.py` – Script to convert and load JSON data into PostgreSQL
- `requirements.txt` – Required Python libraries
- `README.md` – Project documentation

---

## 🚀 Features

- Interactive Streamlit dashboard
- State-wise and quarter-wise UPI transaction analysis
- Top-performing districts and transaction types
- Choropleth maps for visual geographic analysis
- PostgreSQL-powered backend for fast queries

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Plotly Express
- **Backend**: Python, Pandas, PostgreSQL
- **Database Connector**: psycopg2
- **Data Source**: [PhonePe Pulse GitHub](https://github.com/PhonePe/pulse)

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/Shrishanth2004/phonepe-transaction-insights.git
cd phonepe-transaction-insights
