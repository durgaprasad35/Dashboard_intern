import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz

# --------- Data Loading Module ---------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\HP\Downloads\SocialMedia.csv")
    return df

# --------- Task 1: Scatter Plot ---------
def task1_scatter(df):
    # Simulate/modify dataset for demo (remove in production)
    if 'replies' not in df.columns:
        np.random.seed(0)
        df['replies'] = np.random.randint(0, 50, size=len(df))
    if 'engagements' not in df.columns:
        df['engagements'] = np.random.randint(10, 1000, size=len(df))
    if 'views' not in df.columns:
        df['views'] = np.random.randint(100, 10000, size=len(df))
    if 'tweet_date' not in df.columns:
        df['tweet_date'] = np.random.randint(1, 32, size=len(df))
    if 'tweet_text' not in df.columns:
        df['tweet_text'] = ["word " * np.random.randint(30, 100) for _ in range(len(df))]
    df['word_count'] = df['tweet_text'].apply(lambda x: len(str(x).split()))
    filtered = df[
        (df['replies'] > 10) &
        (df['tweet_date'] % 2 == 1) &
        (df['word_count'] > 50)
    ].copy()
    filtered['engagement_rate'] = (filtered['engagements'] / filtered['views']) * 100

    # Time check: Only show plot between 6PM and 11PM IST
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    if 18 <= now_ist.hour < 23:
        st.write("### Engagements vs Views (Filtered Tweets)")
        fig, ax = plt.subplots(figsize=(8,6))
        above_5 = filtered['engagement_rate'] > 5
        ax.scatter(filtered.loc[~above_5, 'views'], filtered.loc[~above_5, 'engagements'],
                   label='Engagement Rate ≤ 5%', alpha=0.7)
        ax.scatter(filtered.loc[above_5, 'views'], filtered.loc[above_5, 'engagements'],
                   color='red', label='Engagement Rate > 5%', alpha=0.7)
        ax.set_xlabel('Media Views')
        ax.set_ylabel('Media Engagements')
        ax.set_title('Engagements vs Views (Filtered Tweets)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("Scatter plot is only available between 6PM and 11PM IST.")

# --------- Task 2: Clustered Bar Chart ---------
def task2_bar(df):
    date_col = 'time'
    text_col = 'Tweet'
    url_clicks_col = 'url clicks'
    profile_clicks_col = 'user profile clicks'
    hashtag_clicks_col = 'hashtag clicks'
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df['word_count'] = df[text_col].astype(str).apply(lambda x: len(x.split()))
    df = df[df[date_col].dt.day % 2 == 0]
    df = df[df['word_count'] > 40]
    df = df[
        (df[url_clicks_col] > 0) |
        (df[profile_clicks_col] > 0) |
        (df[hashtag_clicks_col] > 0)
    ]
    def get_category(row):
        if row['media views'] > 0:
            return 'With Media'
        elif row[url_clicks_col] > 0:
            return 'With Link'
        elif row[hashtag_clicks_col] > 0:
            return 'With Hashtag'
        else:
            return 'Other'
    df['Category'] = df.apply(get_category, axis=1)
    df = df[df['Category'] != 'Other']
    grouped = df.groupby('Category')[[url_clicks_col, profile_clicks_col, hashtag_clicks_col]].sum()
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    if 15 <= now_ist.hour < 17:
        st.write("### Sum of Interactions by Tweet Category (Filtered)")
        fig, ax = plt.subplots(figsize=(10,6))
        grouped.plot(kind='bar', ax=ax)
        ax.set_ylabel('Sum of Clicks')
        ax.set_xlabel('Tweet Category')
        ax.set_title('Sum of Interactions by Tweet Category (Filtered)')
        ax.set_xticklabels(grouped.index, rotation=0)
        st.pyplot(fig)
    else:
        st.info("The chart is only visible between 3PM and 5PM IST.")

# --------- Task 3: Top 10 Tweets Chart ---------
def task3_top10(df):
    date_col = 'time'
    text_col = 'Tweet'
    retweets_col = 'retweets'
    likes_col = 'likes'
    impressions_col = 'impressions'
    user_col = 'id'
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    ist = pytz.timezone('Asia/Kolkata')
    if df[date_col].dt.tz is None:
        df[date_col] = df[date_col].dt.tz_localize('UTC').dt.tz_convert(ist)
    else:
        df[date_col] = df[date_col].dt.tz_convert(ist)
    df = df[(df[date_col].dt.hour >= 15) & (df[date_col].dt.hour < 17)]
    df = df[df[date_col].dt.weekday < 5]
    df = df[df[impressions_col] % 2 == 0]
    df = df[df[date_col].dt.day % 2 == 1]
    df['word_count'] = df[text_col].astype(str).apply(lambda x: len(x.split()))
    df = df[df['word_count'] < 30]
    df['engagement'] = df[retweets_col] + df[likes_col]
    top10 = df.nlargest(10, 'engagement')
    now_ist = datetime.now(ist)
    if 15 <= now_ist.hour < 17:
        st.write("### Top 10 Tweets by Engagement")
        fig, ax = plt.subplots(figsize=(10,6))
        ax.barh(top10[user_col].astype(str), top10['engagement'], color='skyblue')
        ax.set_xlabel('Retweets + Likes')
        ax.set_title('Top 10 Tweets by Engagement (Weekdays, 3-5PM IST, Even Impressions, Odd Date, <30 Words)')
        ax.invert_yaxis()
        st.pyplot(fig)
    else:
        st.info("The chart is only visible between 3PM and 5PM IST.")

# --------- Task 4: Line Chart Engagement Rate Trend ---------
def task4_line(df):
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    def remove_c_words(text):
        return ' '.join([word for word in str(text).split() if 'c' not in word.lower()])
    df['Tweet'] = df['Tweet'].apply(remove_c_words)
    df['char_count'] = df['Tweet'].astype(str).apply(len)
    df = df[df['char_count'] > 20]
    df['engagement rate'] = df['engagement rate'].astype(str).str.rstrip('%').astype(float)
    df = df[df['engagements'] % 2 == 0]
    df = df[df['time'].dt.day % 2 == 1]
    df['has_media'] = df['media views'] > 0
    df['month'] = df['time'].dt.month
    monthly_trend = df.groupby(['month', 'has_media'])['engagement rate'].mean().reset_index()
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    if (7 <= now_ist.hour < 11) or (15 <= now_ist.hour < 17):
        st.write("### Monthly Average Engagement Rate Trend (With vs Without Media)")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.lineplot(
            data=monthly_trend,
            x='month',
            y='engagement rate',
            hue='has_media',
            marker='o',
            ax=ax
        )
        ax.set_title('Monthly Average Engagement Rate Trend\n(With vs Without Media)')
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Engagement Rate (%)')
        ax.set_xticks(range(1,13))
        ax.legend(title='Has Media', labels=['No Media', 'With Media'])
        st.pyplot(fig)
    else:
        st.info("The chart is only visible between 3PM-5PM IST and 7AM-11AM IST.")

# --------- Task 5: Replies/Retweets/Likes Comparison ---------
def task5_bar(df):
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    def remove_s_words(text):
        return ' '.join([word for word in str(text).split() if 's' not in word.lower()])
    df['Tweet'] = df['Tweet'].apply(remove_s_words)
    df['char_count'] = df['Tweet'].astype(str).apply(len)
    df = df[df['char_count'] > 20]
    df = df[df['media views'] % 2 == 0]
    df = df[df['time'].dt.day % 2 == 1]
    df = df[(df['time'].dt.year == 2020) & (df['time'].dt.month >= 6) & (df['time'].dt.month <= 8)]
    median_media_engagements = df['media engagements'].median()
    df = df[df['media engagements'] > median_media_engagements]
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    if (7 <= now_ist.hour < 11) or (15 <= now_ist.hour < 17):
        metrics = ['replies', 'retweets', 'likes']
        sums = [df[m].sum() for m in metrics]
        st.write("### Replies, Retweets, and Likes for Tweets (Media Engagements > Median, Jun-Aug 2020, Odd Date, Even Media Views, Char Count > 20, No 'S' Words)")
        fig, ax = plt.subplots(figsize=(8,6))
        sns.barplot(x=metrics, y=sums, palette='viridis', ax=ax)
        ax.set_ylabel('Count')
        ax.set_xlabel('Metric')
        st.pyplot(fig)
    else:
        st.info("The chart is only visible between 3PM-5PM IST and 7AM-11AM IST.")

# --------- Task 6: App Opens Engagement Rate ---------
def task6_app_opens(df):
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    def remove_d_words(text):
        return ' '.join([word for word in str(text).split() if 'd' not in word.lower()])
    df['Tweet'] = df['Tweet'].apply(remove_d_words)
    df['char_count'] = df['Tweet'].astype(str).apply(len)
    df = df[df['char_count'] > 30]
    df = df[df['impressions'] % 2 == 0]
    df = df[df['time'].dt.day % 2 == 1]
    df = df[df['time'].dt.weekday < 5]
    df = df[(df['time'].dt.hour >= 9) & (df['time'].dt.hour < 17)]
    df['engagement rate'] = df['engagement rate'].astype(str).str.rstrip('%').astype(float)
    df['has_app_opens'] = df['app opens'] > 0
    comparison = df.groupby('has_app_opens')['engagement rate'].mean().reset_index()
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    if (7 <= now_ist.hour < 11) or (12 <= now_ist.hour < 18):
        st.write("### Average Engagement Rate: Tweets With vs Without App Opens")
        fig, ax = plt.subplots(figsize=(7,5))
        sns.barplot(
            data=comparison,
            x='has_app_opens',
            y='engagement rate',
            palette='Set2',
            ax=ax
        )
        ax.set_xlabel('Has App Opens')
        ax.set_ylabel('Average Engagement Rate (%)')
        ax.set_xticks([0,1])
        ax.set_xticklabels(['No App Opens', 'With App Opens'])
        st.pyplot(fig)
    else:
        st.info("The chart is only visible between 12PM-6PM IST and 7AM-11AM IST.")

# --------- Main App Layout ---------
def main():
    st.set_page_config(page_title="Twitter Analytics Dashboard", layout="wide")
    st.title("Twitter Analytics Dashboard")
    st.markdown("#### Interactive dashboard for Twitter analytics tasks. Use the tabs below to explore each analysis.")

    df = load_data()

    tabs = st.tabs([
        "Task 1: Scatter Chart",
        "Task 2: Clustered Bar",
        "Task 3: Top 10 Tweets",
        "Task 4: Engagement Trend",
        "Task 5: Replies/Retweets/Likes",
        "Task 6: App Opens Comparison"
    ])

    with tabs[0]:
        task1_scatter(df.copy())
    with tabs[1]:
        task2_bar(df.copy())
    with tabs[2]:
        task3_top10(df.copy())
    with tabs[3]:
        task4_line(df.copy())
    with tabs[4]:
        task5_bar(df.copy())
    with tabs[5]:
        task6_app_opens(df.copy())

if __name__ == "__main__":
    main()