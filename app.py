import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def categorize_storey_range(storey):
    """Categorize storey range into Low, Mid, High floors based on average floor."""
    if isinstance(storey, str):
        try:
            start, end = map(int, storey.split(" TO "))
            avg = (start + end) / 2
            if avg <= 5:
                return "Low floor (01-05)"
            elif avg <= 11:
                return "Mid floor (06-11)"
            else:
                return "High floor (12+)"
        except Exception:
            return "Unknown"
    return "Unknown"

def extract_lease_years(lease_text):
    """Extract numeric years from 'remaining_lease'."""
    if isinstance(lease_text, str):
        try:
            years = int(lease_text.split('year')[0].strip())
            return years
        except Exception:
            return None
    return None

def categorize_remaining_lease(years):
    """Categorize the lease years into buckets."""
    if years is None:
        return "Unknown"
    if years < 60:
        return "<60 years"
    elif 60 <= years < 70:
        return "60-69 years"
    elif 70 <= years < 80:
        return "70-79 years"
    elif 80 <= years < 90:
        return "80-89 years"
    else:
        return "90+ years"

# ---------------------------------------------------------
# Load Data Functions
# ---------------------------------------------------------

@st.cache_data(show_spinner="Loading static 2017–2024 data...")
def load_static_data():
    return pd.read_csv("resale_flat_2017_2024.csv")

@st.cache_data(show_spinner="Loading dynamic 2025+ data...")
def load_dynamic_data():
    return pd.read_csv("dynamic_2025_data.csv")

# ---------------------------------------------------------
# Main App
# ---------------------------------------------------------

st.set_page_config(page_title="HDB Resale Dashboard", layout="wide")
st.title("🏠 Singapore HDB Resale Flat Dashboard")

# Load datasets
static_df = load_static_data()
dynamic_df = load_dynamic_data()

# Merge datasets
full_df = pd.concat([static_df, dynamic_df], ignore_index=True)

# Enrich data
for df in [full_df, dynamic_df]:
    df['floor_level_category'] = df['storey_range'].apply(categorize_storey_range)
    df['lease_years'] = df['remaining_lease'].apply(extract_lease_years)
    df['lease_category'] = df['lease_years'].apply(categorize_remaining_lease)

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------

option = st.sidebar.selectbox(
    "Select what you want to explore:",
    ("2025 Latest Resale Records", "View Full Dataset")
)

# ---------------------------------------------------------
# Common Section Template
# ---------------------------------------------------------

def render_section(filtered_df, title_prefix):
    st.write(f"### {title_prefix} Filtered Results")
    st.dataframe(filtered_df)

    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_resale_data.csv',
            mime='text/csv',
        )

    # Line Chart
    st.write(f"### 📈 {title_prefix} Average Resale Price Over Time")
    if 'resale_price' in filtered_df.columns:
        price_trend = filtered_df.groupby('month')['resale_price'].mean().reset_index()
        if not price_trend.empty:
            st.line_chart(price_trend.rename(columns={'month': 'index'}).set_index('index'))
        else:
            st.info("No data available for price trend.")

    # Bar Chart
    st.write(f"### 🏡 {title_prefix} Transactions Count by Town")
    if 'town' in filtered_df.columns:
        town_count = filtered_df['town'].value_counts().sort_values(ascending=False)
        if not town_count.empty:
            st.bar_chart(town_count)
        else:
            st.info("No data available for town analysis.")

    # Grouped Boxplot
    st.write(f"### 📦 {title_prefix} Resale Price Distribution by Flat Type (Boxplot)")
    if 'resale_price' in filtered_df.columns and 'flat_type' in filtered_df.columns:
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='none')

            resale_by_flat = [group['resale_price'].dropna() for name, group in filtered_df.groupby('flat_type')]
            flat_labels = sorted(filtered_df['flat_type'].dropna().unique())

            bp = ax.boxplot(resale_by_flat, vert=True, patch_artist=True,
                            labels=flat_labels,
                            boxprops=dict(facecolor='none', color='deepskyblue', linewidth=2),
                            medianprops=dict(color='red', linewidth=2),
                            whiskerprops=dict(color='white', linewidth=2),
                            capprops=dict(color='white', linewidth=2),
                            flierprops=dict(marker='o', markersize=4, markerfacecolor='lightgray', alpha=0.5))

            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(axis='x', colors='white', labelrotation=45)
            ax.tick_params(axis='y', colors='white')
            ax.set_title("Resale Price Distribution by Flat Type", fontsize=16, fontweight='bold', color='white', pad=15)
            ax.set_ylabel("Resale Price (SGD)", fontsize=12, color='white')
            ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
            ax.grid(True, linestyle='--', alpha=0.3, color='lightgrey')
            ax.set_facecolor('none')

            st.pyplot(fig)
        else:
            st.info("No data available for grouped boxplot.")

# ---------------------------------------------------------
# Section: 2025 Latest Resale Records
# ---------------------------------------------------------

if option == "2025 Latest Resale Records":
    st.subheader("2025+ Resale Transactions")

    filtered_df = dynamic_df.copy()
    filtered_df['year'] = pd.to_datetime(filtered_df['month']).dt.year

    with st.expander("🔽 Show Filters"):
        towns = sorted(filtered_df['town'].dropna().unique())
        selected_town = st.selectbox("Select Town:", options=["All"] + towns, key="town_dynamic")

        flat_types = sorted(filtered_df['flat_type'].dropna().unique())
        selected_flat_types = st.multiselect("Select Flat Type(s):", options=flat_types, default=flat_types, key="flat_dynamic")

        floor_levels = sorted(filtered_df['floor_level_category'].dropna().unique())
        selected_floor_levels = st.multiselect("Select Floor Level(s):", options=floor_levels, default=floor_levels, key="floor_dynamic")

        lease_order = ["<60 years", "60-69 years", "70-79 years", "80-89 years", "90+ years"]
        lease_categories = [cat for cat in lease_order if cat in filtered_df['lease_category'].unique()]
        selected_lease = st.multiselect("Select Remaining Lease Category:", options=lease_categories, default=lease_categories, key="lease_dynamic")

        years = sorted(filtered_df['year'].dropna().unique())
        selected_years = st.multiselect("Select Year(s):", options=years, default=years, key="year_dynamic")

        available_months = sorted(filtered_df['month'].dropna().unique())
        selected_months = st.multiselect("Select Month(s):", options=available_months, default=available_months, key="month_dynamic")

        # Apply filters
        if selected_town != "All":
            filtered_df = filtered_df[filtered_df['town'] == selected_town]
        if selected_flat_types:
            filtered_df = filtered_df[filtered_df['flat_type'].isin(selected_flat_types)]
        if selected_floor_levels:
            filtered_df = filtered_df[filtered_df['floor_level_category'].isin(selected_floor_levels)]
        if selected_lease:
            filtered_df = filtered_df[filtered_df['lease_category'].isin(selected_lease)]
        if selected_years:
            filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
        if selected_months:
            filtered_df = filtered_df[filtered_df['month'].isin(selected_months)]

    render_section(filtered_df, title_prefix="2025+")

# ---------------------------------------------------------
# Section: View Full Dataset
# ---------------------------------------------------------

elif option == "View Full Dataset":
    st.subheader("Full Resale Dataset (2017 onwards)")

    filtered_df = full_df.copy()
    filtered_df['year'] = pd.to_datetime(filtered_df['month']).dt.year

    with st.expander("🔽 Show Filters"):
        towns = sorted(filtered_df['town'].dropna().unique())
        selected_town = st.selectbox("Select Town:", options=["All"] + towns, key="town_full")

        flat_types = sorted(filtered_df['flat_type'].dropna().unique())
        selected_flat_types = st.multiselect("Select Flat Type(s):", options=flat_types, default=flat_types, key="flat_full")

        floor_levels = sorted(filtered_df['floor_level_category'].dropna().unique())
        selected_floor_levels = st.multiselect("Select Floor Level(s):", options=floor_levels, default=floor_levels, key="floor_full")

        lease_order = ["<60 years", "60-69 years", "70-79 years", "80-89 years", "90+ years"]
        lease_categories = [cat for cat in lease_order if cat in filtered_df['lease_category'].unique()]
        selected_lease = st.multiselect("Select Remaining Lease Category:", options=lease_categories, default=lease_categories, key="lease_full")

        years = sorted(filtered_df['year'].dropna().unique())
        selected_years = st.multiselect("Select Year(s):", options=years, default=years, key="year_full")

        available_months = sorted(filtered_df['month'].dropna().unique())
        selected_months = st.multiselect("Select Month(s):", options=available_months, default=available_months, key="month_full")

        # Apply filters
        if selected_town != "All":
            filtered_df = filtered_df[filtered_df['town'] == selected_town]
        if selected_flat_types:
            filtered_df = filtered_df[filtered_df['flat_type'].isin(selected_flat_types)]
        if selected_floor_levels:
            filtered_df = filtered_df[filtered_df['floor_level_category'].isin(selected_floor_levels)]
        if selected_lease:
            filtered_df = filtered_df[filtered_df['lease_category'].isin(selected_lease)]
        if selected_years:
            filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
        if selected_months:
            filtered_df = filtered_df[filtered_df['month'].isin(selected_months)]

    render_section(filtered_df, title_prefix="Full")

# ---------------------------------------------------------
# End
# ---------------------------------------------------------
