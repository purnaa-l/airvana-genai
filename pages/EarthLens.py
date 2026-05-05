import streamlit as st
import requests
import datetime
st.set_page_config(page_title="EarthLens 🌍", page_icon="🌿", layout="wide")
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?q=80&w=2942&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown("""
<style>
.card {
    background: rgba(245, 245, 220, 0.85);
    border-radius: 15px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.card .title {
    font-size: 20px;
    font-weight: bold;
    color: #3e2723;
    margin-bottom: 10px;
}
.card .desc {
    font-size: 14px;
    color: #4e342e;
    margin-bottom: 10px;
}
.card .source {
    text-align: center;
    margin-top: 10px;
}
.card .source a {
    background-color: #1a237e;
    color: white;
    padding: 6px 12px;
    border-radius: 5px;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🔍 EarthLens - Natural Events Viewer")
st.write("Track real-time environmental events powered by NASA's **EONET API**.")

# Filters
st.sidebar.header("📍 Filters")
categories = {
    "Wildfires": "wildfires",
    "Volcanoes": "volcanoes",
    "Storms": "severeStorms",
    "Smoke": "smoke",
    "Ash": "ash"
}
selected_categories = st.sidebar.multiselect("Category", list(categories.keys()), default=["Wildfires"])
start_date = st.sidebar.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=10))
end_date = st.sidebar.date_input("End Date", datetime.date.today())
keyword = st.sidebar.text_input("Search Title", "")
if st.sidebar.button("🔎 Fetch Events"):
    st.subheader("🧭 Recent Natural Events")
    try:
        res = requests.get("https://eonet.gsfc.nasa.gov/api/v3/events")
        events = res.json().get("events", [])
        filtered = []

        for event in events:
            event_date = datetime.datetime.fromisoformat(event['geometry'][0]['date'].replace("Z", "")).date()
            if not (start_date <= event_date <= end_date):
                continue

            # Category filter
            event_categories = [cat['title'].lower() for cat in event['categories']]
            if not any(categories[cat].lower() in event_categories for cat in selected_categories):
                continue

            # Keyword filter
            if keyword.lower() not in event["title"].lower():
                continue

            filtered.append(event)

        if filtered:
            cols = st.columns(2)
            for idx, event in enumerate(filtered[:20]):
                title = event['title']
                desc = event.get('description') or "No description available."
                category = event['categories'][0]['title']
                date = event['geometry'][0]['date'][:10]
                coords = event['geometry'][0]['coordinates']
                source = event['sources'][0]['url'] if event.get('sources') else event['link']

                with cols[idx % 2]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="title">{title}</div>
                            <div class="desc">
                                <b>Category:</b> {category}<br>
                                <b>Date:</b> {date}<br>
                                <b>Location:</b> {coords}<br><br>
                                {desc}
                            </div>
                            <div class="source">
                                <a href="{source}" target="_blank">🔗 Read More</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No events found matching the criteria.")
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("""
---
Made with ❤️ by **AirVana Team** | Powered by NASA EONET API | [EONET Docs](https://eonet.gsfc.nasa.gov/docs/v3)
""")
