import pinotdb
import pandas as pd
import streamlit as st

# Connect to PinotDB
conn = pinotdb.connect(host='54.255.209.170', port=8099, path='/query/sql', scheme='http')

# Function to fetch data from Pinot
def fetch_data(query):
    return pd.read_sql(query, conn)

# Layout
st.title("Dynamic Data Visualization Dashboard")

# Refresh Button
if st.button("Refresh Data"):
    st.session_state.refresh = True

# If `refresh` is not set in session_state, initialize it
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

if st.session_state.refresh:
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

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pageviews by User")
        st.bar_chart(df_pageviews.set_index('userid')['total_pageviews'])

    with col2:
        st.subheader("Users by Gender")
        st.bar_chart(df_gender.set_index('gender')['total_users'])

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Average View Time by User")
        st.bar_chart(df_avg_viewtime.set_index('userid')['avg_viewtime'])

    with col4:
        st.subheader("Users by City")
        st.bar_chart(df_users_by_city.set_index('city')['total_users'])

    # Reset refresh state after rendering
    st.session_state.refresh = False
