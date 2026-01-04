# 1. Imports
import streamlit as st
import pandas as pd

# 2. Page config
st.set_page_config(
    page_title="US Baby Name Popularity",
    page_icon="👶"
)

st.title("👶 How Popular Was Your Name When You Were Born?")
st.markdown(""" Explore the popularity of baby names in the US over the years! """)

# 3. Data loading + cleaning (cached)
@st.cache_data
def load_national_data():
    return pd.read_parquet("data/us_baby_names_national.parquet")

@st.cache_data
def load_top_states_data():
    return pd.read_parquet("data/us_baby_names_top_states.parquet", engine="pyarrow")

df_national = load_national_data()
df_top_states = load_top_states_data()

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
df_top_states["state_full"] = df_top_states["state"].map(abbrev_to_us_state)

# 4. Helper functions (stats logic)
def get_national_rankings(name, year):
    national = (
        df_national[df_national["year"] == year]
        .groupby("name", as_index=False)["name_count"]
        .sum()
    )

    national["rank"] = (
        national["name_count"]
        .rank(method="dense", ascending=False)
    )

    result = national[national["name"] == name]

    return result[["name_count", "rank"]]


def get_sex_percentages(name, year):
    data = df_national[
        (df_national["name"] == name) &
        (df_national["year"] == year)
    ]

    totals = data.groupby("sex")["name_count"].sum()
    total = totals.sum()

    return {
        "male_pct": totals.get("M", 0) / total * 100 if total else 0,
        "female_pct": totals.get("F", 0) / total * 100 if total else 0,
    }


def get_state_rankings(name, year, top_n=5):
 data = df_top_states[
        (df_top_states["name"] == name) &
        (df_top_states["year"] == year)
    ]
 if data.empty:
        return None
 state_totals = (
        data
        .groupby("state_full", as_index=False)["name_count"]
        .sum()
        .sort_values("name_count", ascending=False)
        .head(top_n)
    )
 return state_totals


def increase_in_popularity(name, birth_year):
    latest_year = df_national["year"].max()

    birth_total = (
        df_national[
            (df_national["name"] == name) &
            (df_national["year"] == birth_year)
        ]["name_count"]
        .sum()
    )

    latest_total = (
        df_national[
            (df_national["name"] == name) &
            (df_national["year"] == latest_year)
        ]["name_count"]
        .sum()
    )

    if birth_total == 0:
        return None, latest_year

    change_pct = ((latest_total - birth_total) / birth_total) * 100

    return change_pct, latest_year

# 5. Streamlit UI (inputs)
st.subheader("🔍 Explore a name")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "What year were you born?",
        min_value=int(df_national["year"].min()),
        max_value=int(df_national["year"].max()),
        step=1
    )
with col2:
    name = st.text_input("What's your first name?")

if not name:
    st.info("Enter a name and year to see statistics.")
    st.stop()

name = name.title()

# 6. Streamlit UI (outputs / charts)
st.subheader("US National popularity")

national = get_national_rankings(name, year)

if national.empty:
    st.warning("This name does not appear in the national data for that year.")
else:
    rank = int(national["rank"].iloc[0])
    count = int(national["name_count"].iloc[0])

    st.metric(
        label=f"National rank in {year}",
        value=f"#{rank}",
        delta=f"{count:,} babies"
    )
st.subheader(f"⚧ Gender usage in {year}")

sex_pct = get_sex_percentages(name, year)

col1, col2 = st.columns(2)

with col1:
    st.metric("Used for boys", f"{sex_pct['male_pct']:.1f}%")

with col2:
    st.metric("Used for girls", f"{sex_pct['female_pct']:.1f}%")

st.subheader("📍 Where was this name most popular?")

top_states = get_state_rankings(name, year)

if top_states is None or top_states.empty:
    st.info("No state-level data available for this year.")
else:
    st.write(f"Top states for **{name}** in **{year}**:")

    for i, row in top_states.iterrows():
        st.write(f"• **{row['state_full']}** — {int(row['name_count']):,} babies")

    st.bar_chart(
        top_states.set_index("state_full")["name_count"]
    )
st.subheader("📈 Popularity over time")

change, latest_year = increase_in_popularity(name, year)

if change is not None:
    arrow = "⬆️" if change > 0 else "⬇️"
    st.write(
        f"Since {year}, this name has {arrow} "
        f"**{abs(change):.1f}%** "
        f"(as of {latest_year})."
    )
else:
    st.info("Not enough data to calculate popularity change.")
with st.expander("📊 See popularity over time"):
    trend = (
        df_national[df_national["name"] == name]
        .groupby("year")["name_count"]
        .sum()
    )

    if trend.empty:
        st.info("No historical trend available.")
    else:
        st.line_chart(trend)


