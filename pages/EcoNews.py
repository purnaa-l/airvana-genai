import streamlit as st
from newsapi import NewsApiClient
import pandas as pd
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
st.set_page_config(page_title="Eco News 🌎", page_icon="🌿", layout="wide")
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-image: url('https://images.unsplash.com/photo-1620483763435-aa0b760982df?q=80&w=3174&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');

[data-testid="stHeader"], [data-testid="stSidebar"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

def save_articles_to_csv(articles):
    now = datetime.datetime.now()

    # Extract important fields only
    extracted_articles = []
    for article in articles:
        extracted_articles.append({
            "Title": article['title'],
            "Description": article.get('description', ''),
            "Published At": article['publishedAt'],
            "Source": article['source']['name'],
            "URL": article['url'],
            "Saved At": now.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(extracted_articles)

    if not os.path.exists("eco_news.csv"):
        df.to_csv("eco_news.csv", index=False)
    else:
        df.to_csv("eco_news.csv", mode='a', header=False, index=False)

st.markdown("""
    <style>
    body {
        background-color: #ecf9ec;
    }
    .card {
        background: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .card:hover {
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        transform: translateY(-2px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;

    }
    .card img {
        width: 100%;
        border-radius: 10px;
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
        color: #2e7d32;
        margin-top: 15px;
        font-family: 'Poppins', sans-serif;
        text-align: center;
    }
    .card-desc {
        font-size: 16px;
        margin-top: 10px;
        color: #555;
    }
    .card-footer {
        font-size: 14px;
        color: #888;
        margin-top: 15px;
    }
    .read-more {
    margin-top: 10px;
    display: inline-block;
    padding: 8px 15px;
    background-color: #bfd9bb;
    color: white;
    border-radius: 5px;
    text-decoration: none;
    /* align: center; */ /* Remove this line */
    font-weight: bold;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 16px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    cursor: pointer;
    color: #ffffff; /* Corrected property is color */
    margin-left: auto;
    margin-right: auto;
    display: block;
    }
    .read-more:hover {
        background-color: #388e3c;
        transition: background-color 0.3s;

    }
    </style>
""", unsafe_allow_html=True)
st.title("🌍 Eco News - AirVana's Premium News Site")
st.write("Stay informed on **Air Quality**, **Pollution**, **Climate Change**, and **Environmental** news from across the world at your fingertips!")
st.sidebar.header("🔎 Filters")
topics = st.sidebar.multiselect(
    "Select Topics",
    ["Air Quality", "Pollution", "Climate Change", "Environment"],
    default=["Pollution"]
)
sort_by = st.sidebar.selectbox("Sort Articles By", ["relevancy", "popularity", "publishedAt"])
from_date = st.sidebar.date_input("From Date", datetime.date.today() - datetime.timedelta(days=7))
to_date = st.sidebar.date_input("To Date", datetime.date.today())
page_size = st.sidebar.slider("Number of Articles", 5, 50, 10)

if st.sidebar.button("Get Eco News 🌿"):
    with st.spinner("Fetching the latest Environmental news... 🌎"):
        try:
            # Build query from selected topics
            query = " OR ".join(topics)

            # Fetch articles
            all_articles = newsapi.get_everything(
                q=query,
                language="en",
                sort_by=sort_by,
                from_param=from_date,
                to=to_date,
                page_size=page_size
            )
            
            articles = all_articles.get('articles', [])

            if articles:
                st.success(f"Found {len(articles)} articles! ✅")
                cols = st.columns(3)  # Two cards per row
                for idx, article in enumerate(articles):
                    with cols[idx % 3]:  # Alternate between columns
                        # Handle missing image
                        image_url = article['urlToImage'] if article['urlToImage'] else "https://images.unsplash.com/photo-1621112816926-db4caf0b37fd?q=80&w=3087&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                        st.markdown(f"""
                            <div class="card">
                                <img src="{image_url}" alt="News Image">
                                <div class="card-title">{article['title']}</div>
                                <div class="card-desc">{article['description'] if article['description'] else ''}</div>
                                <a class="read-more" href="{article['url']}" target="_blank">Read Full Article</a>
                                <div class="card-footer">Published: {article['publishedAt'][:10]} | Source: {article['source']['name']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                save_articles_to_csv(articles)
                st.success("Articles saved to eco_news.csv! ✅")
                #st.markdown("<a class='read-more' href='eco_news.csv' download>📄 Download Eco News CSV</a>", unsafe_allow_html=True)

            else:
                st.warning("No articles found. Try adjusting filters.")
        
        except Exception as e:
                st.warning("No articles found. Try adjusting filters.")
                #st.error(f"Error fetching news: {e}")

st.markdown("""
---
Made with ❤️ by **AirVana Team** | Empowering Green Initiatives 🌿 | Because, Every Breath Matters.
""")
