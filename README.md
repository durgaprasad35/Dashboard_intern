# Dashboard_intern
An interactive Streamlit dashboard for analyzing Twitter engagement metrics using Python, Pandas, and Seaborn. It visualizes tweet performance through dynamic charts like scatter, bar, and line plots with time-based filters, enabling insights into impressions, likes, retweets, and app opens.
📊 Twitter Analytics Dashboard

A Streamlit-based interactive dashboard that analyzes Twitter data using Python, Pandas, Matplotlib, and Seaborn.
This project visualizes various aspects of tweet engagement such as views, likes, retweets, replies, app opens, and media engagement — with time-based visibility filters to simulate real-time analytics.

🚀 Project Overview

This project provides an end-to-end analytical interface for understanding tweet performance using data from a CSV file (SocialMedia.csv).
It includes six analytical tasks, each displayed in a dedicated tab with time-sensitive visibility conditions (specific IST time ranges).

🧩 Key Features

📈 Scatter Plot: Analyze engagement vs. views for tweets filtered by replies, word count, and engagement rate.

📊 Clustered Bar Chart: Compare different types of tweet interactions (media, links, hashtags).

🏆 Top 10 Tweets: Visualize top-performing tweets based on likes and retweets.

📉 Engagement Trend Line Chart: Observe monthly engagement rate trends with and without media.

🔁 Replies/Retweets/Likes Comparison: Compare overall tweet performance during specific months and conditions.

📱 App Opens Engagement Comparison: Measure engagement rate differences between tweets with and without app opens.

⏰ Dynamic Time Control: Certain charts only appear during specific IST time windows to simulate time-based dashboard behavior.

🧠 Technologies Used
Category	Tools / Libraries
Frontend / UI	Streamlit

Data Processing	Pandas
, NumPy

Visualization	Matplotlib
, Seaborn

Datetime & Timezone Handling	datetime, pytz
📂 Project Structure
Twitter_Analytics_Dashboard/
│
├── SocialMedia.csv                # Input dataset (user-provided)
├── app.py                         # Main Streamlit application
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies

⚙️ Installation and Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/twitter-analytics-dashboard.git
cd twitter-analytics-dashboard

2️⃣ Install Dependencies

Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux


Then install the required packages:

pip install -r requirements.txt


If requirements.txt is not available, install manually:

pip install streamlit pandas numpy matplotlib seaborn pytz

3️⃣ Place the Dataset

Ensure your dataset file is placed at:

C:\Users\HP\Downloads\SocialMedia.csv


(or modify the file path in the code as needed).

4️⃣ Run the Application
streamlit run app.py

🧭 Dashboard Navigation

The dashboard contains six main tabs, each showing a different type of analysis:

Tab	Description	Visible Time (IST)
Task 1	Scatter Plot: Engagement vs Views	6 PM – 11 PM
Task 2	Clustered Bar Chart: Interactions by Category	3 PM – 5 PM
Task 3	Top 10 Tweets by Engagement	3 PM – 5 PM
Task 4	Line Chart: Monthly Engagement Trend	7 AM – 11 AM & 3 PM – 5 PM
Task 5	Replies/Retweets/Likes Comparison	7 AM – 11 AM & 3 PM – 5 PM
Task 6	App Opens Engagement Comparison	7 AM – 11 AM & 12 PM – 6 PM
🧾 Data Requirements

The CSV file should contain (at least) the following columns:

id, time, Tweet, impressions, engagements, likes, retweets,
replies, media views, media engagements, engagement rate,
url clicks, user profile clicks, hashtag clicks, app opens


If any column is missing, the app simulates random demo data for visualization purposes.

🧮 Data Filtering Logic

Each task applies specific filters such as:

Odd or even dates

Specific word or character counts in tweets

Presence or absence of certain letters (‘c’, ‘s’, ‘d’)

Media or link-related engagement

Weekday/time-based analysis

These filters showcase data wrangling techniques and realistic tweet analysis conditions.

📅 Time-Based Display Logic

Each visualization only appears during specific IST time ranges, creating a dynamic and controlled analysis environment.

For example:

if 18 <= now_ist.hour < 23:
    st.pyplot(fig)
else:
    st.info("Scatter plot is only available between 6PM and 11PM IST.")

📷 Sample Visuals

Scatter Plot: Engagements vs Views

Clustered Bar: Interaction Categories

Line Chart: Engagement Trends

Bar Chart: Likes, Retweets, Replies

(Note: Visuals will be displayed dynamically during allowed hours.)

👨‍💻 Author

Durgaprasad Naradala
B.Tech (ECE), Sasi Institute of Engineering and Technology
📚 Interests: Data Science | Machine Learning | Python | Analytics Dashboards
