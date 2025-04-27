# 🏠 Singapore HDB Resale Flat Dashboard

A dynamic data visualization app built with **Streamlit**, analyzing Singapore **HDB resale flat prices** from 2017 to 2025.

This project showcases skills in:

- API data fetching
- Data cleaning and wrangling
- Interactive filtering
- Data visualization (line chart, bar chart, boxplots)
- Streamlit app development
- Data export functionality

---

## 📊 Key Features

- **Dynamic Data Source**  
  - 2017–2024 resale data (static CSV)
  - 2025 onwards data (live fetch from Data.gov.sg API)

- **Interactive Filtering**  
  - Filter by Town, Flat Type, Floor Range, Year, Month

- **Charts and Insights**  
  - 📈 Average Resale Price Trend Over Time
  - 🏡 Number of Transactions by Town
  - 📦 Resale Price Distribution by Flat Type (Grouped Boxplots)

- **Download Feature**  
  - 📥 Export filtered search results as CSV

- **Dark Mode Optimized**  
  - Custom matplotlib styling to match Streamlit dark theme

---

## 🚀 Live Demo

> _(Insert your Streamlit Cloud URL once deployed)_  
> Example: [https://my-hdb-resale-dashboard.streamlit.app](https://my-hdb-resale-dashboard.streamlit.app)

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

---

## 📂 Project Structure

├── app.py # Main Streamlit application ├── requirements.txt # Python dependencies ├── resale_flat_2017_2024.csv # Static resale data (2017–2024) ├── dynamic_2025_data.csv # Live fetched data for 2025 └── README.md # Project documentation

yaml
Copy
Edit

---

## 🧠 Author

- **Your Name** — [LinkedIn Profile](https://linkedin.com/in/your-link)

---

## 📋 How to Run Locally

1. Clone the repo
2. Install requirements:

pip install -r requirements.txt


## Run the Streamlit app:

streamlit run app.py
