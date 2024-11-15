import streamlit as st
import pandas as pd
import pinotdb
import matplotlib.pyplot as plt
import time

# Establish connection to Pinot
conn = pinotdb.connect(host='54.255.209.170', port=8099, path='/query/sql', scheme='http')
cursor = conn.cursor()

def query_pinot(sql_query):
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description]) if rows else pd.DataFrame()
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()

# Streamlit application
st.title('Data Visualization')

# Dropdown menu for user choice
dimension = st.sidebar.selectbox('Choose the grouping dimension:', ['Gender', 'Region ID', 'Age Group', 'Activity Level', 'Country', 'User Count by Time'])

if 'last_update' not in st.session_state or time.time() - st.session_state.last_update > 30:
    # Update the last update time
    st.session_state.last_update = time.time()

    # Define SQL queries based on the choice
    sql_queries = {
        'Gender': "SELECT gender, COUNT(*) as userCount FROM users_table GROUP BY gender ORDER BY userCount DESC",
        'Region ID': "SELECT regionid, COUNT(*) as userCount FROM users_table GROUP BY regionid ORDER BY userCount DESC",
        'Age Group': "SELECT age_group, COUNT(*) as userCount FROM users_table GROUP BY age_group ORDER BY userCount DESC",
        'Activity Level': "SELECT activity_level, COUNT(*) as userCount FROM users_table GROUP BY activity_level ORDER BY userCount DESC",
        'Country': "SELECT country, COUNT(*) as userCount FROM users_table GROUP BY country ORDER BY userCount DESC",
        'User Count by Time': """
            SELECT time_bucket('1 day', registration_time) as day, COUNT(*) as userCount 
            FROM users_table 
            WHERE registration_time > CURRENT_DATE - INTERVAL '30 days'
            GROUP BY day
            ORDER BY day
        """
    }
    sql_query = sql_queries.get(dimension, "SELECT 'Invalid dimension'")

    # Fetch data from Pinot
    df = query_pinot(sql_query)

    # Plotting
    if not df.empty:
        fig, ax = plt.subplots()
        if dimension == 'User Count by Time':
            ax.plot(df['day'], df['userCount'], marker='o', color='blue')
            ax.set_xlabel('Date')
            ax.set_ylabel('User Count')
            ax.set_title(f'User Count by Time (Last 30 Days)')
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.bar(df[df.columns[0]], df['userCount'], color='blue')
            ax.set_xlabel(dimension)
            ax.set_ylabel('User Count')
            ax.set_title(f'User Count by {dimension}')
        st.pyplot(fig)
    else:
        st.write("No data available or failed to connect to Pinot.")

# Button to manually trigger a refresh
if st.button('Refresh Data'):
    st.session_state.last_update = time.time() - 31  # Force update
