import pinotdb
import pandas as pd
import streamlit as st
import altair as alt

# Connect to PinotDB
conn = pinotdb.connect(host='54.255.209.170', port=8099, path='/query/sql', scheme='http')

# Function to fetch data from Pinot
def fetch_data(query):
    return pd.read_sql(query, conn)

# Refresh interval in seconds
refresh_interval = st.sidebar.slider("Set Refresh Interval (seconds)", min_value=5, max_value=60, value=10)

# Start the app
st.title("Dynamic Data Visualization Dashboard")

# Button to refresh the data
if st.button("Refresh Data"):
    # Query 1: Pageviews by User (Count)
    query_pageviews = """
    SELECT userid, COUNT(*) AS total_pageviews
    FROM pageviews_stream
    GROUP BY userid
    ORDER BY total_pageviews DESC;
    """
    df_pageviews = fetch_data(query_pageviews)

    # Query 2: Users by Gender (Count)
    query_gender = """
    SELECT gender, COUNT(*) AS total_users
    FROM users_table
    GROUP BY gender;
    """
    df_gender = fetch_data(query_gender)

    # Query 3: Average View Time by User
    query_avg_viewtime = """
    SELECT userid, AVG(viewtime) AS avg_viewtime
    FROM pageviews_stream
    GROUP BY userid
    ORDER BY avg_viewtime DESC;
    """
    df_avg_viewtime = fetch_data(query_avg_viewtime)

    # Query 4: Users by City (Count)
    query_users_by_city = """
    SELECT city, COUNT(*) AS total_users
    FROM users_click_stream
    GROUP BY city
    ORDER BY total_users DESC;
    """
    df_users_by_city = fetch_data(query_users_by_city)

    # Layout: Two rows, two columns
    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pageviews by User")
        chart_pageviews = (
            alt.Chart(df_pageviews)
            .mark_bar(color="teal")
            .encode(
                x=alt.X("userid:N", title="User ID"),
                y=alt.Y("total_pageviews:Q", title="Total Pageviews"),
                tooltip=["userid", "total_pageviews"],
            )
            .properties(width=350, height=300)
        )
        st.altair_chart(chart_pageviews)

    with col2:
        st.subheader("Users by Gender")
        chart_gender = (
            alt.Chart(df_gender)
            .mark_arc(innerRadius=50)
            .encode(
                theta=alt.Theta("total_users:Q", title="Proportion"),
                color=alt.Color("gender:N", legend=alt.Legend(title="Gender")),
                tooltip=["gender", "total_users"],
            )
            .properties(width=350, height=300)
        )
        st.altair_chart(chart_gender)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Average View Time by User")
        chart_avg_viewtime = (
            alt.Chart(df_avg_viewtime)
            .mark_line(point=True, color="blue")
            .encode(
                x=alt.X("userid:N", title="User ID"),
                y=alt.Y("avg_viewtime:Q", title="Average View Time"),
                tooltip=["userid", "avg_viewtime"],
            )
            .properties(width=350, height=300)
        )
        st.altair_chart(chart_avg_viewtime)

    with col4:
        st.subheader("Users by City")
        chart_users_city = (
            alt.Chart(df_users_by_city)
            .mark_bar(color="orange")
            .encode(
                x=alt.X("city:N", sort="-y", title="City"),
                y=alt.Y("total_users:Q", title="Total Users"),
                tooltip=["city", "total_users"],
            )
            .properties(width=350, height=300)
        )
        st.altair_chart(chart_users_city)

# Display timer for the next refresh
st.sidebar.write(f"Auto-refresh in progress: {refresh_interval} seconds...")
