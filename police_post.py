import pandas as pd
import streamlit as st
import pymysql as db

def create_connection():
    try:
        connection = db.connect(
            host="localhost",
            user="Karthick",
            password="262000",
            database="securecheck",
            cursorclass=db.cursors.DictCursor
        )
        return connection
    except Exception as exp:
        st.error("Database Connection error: {exp}")
        return None
    

def fetch_data(query):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                df = pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()
    

#streamlit code
st.set_page_config(page_title="Securecheck Police Dashboard", layout= "wide" )


st.title("🚓- Real-Time Vehicle Monitoring and Violation Tracking Dashboard")
st.markdown("Centralized Check Post Intelligence System")


st.header("📊 Overview of Police post logs")
query = "select * from police_post"
data = fetch_data(query)
st.dataframe(data)


st.markdown(""" ## Visual Insights:bulb:""")
st.write(""" #### Medium level Insights: """)

selected_query = st.selectbox("Select your question to run :blush:",{
    "Top 10 vehicle number involed in drug related stops",
    "Vehicles were most frequently searched",
    "Which driver age group had the highest arrest rate",
    "What is the gender distribution of drivers stopped in each country",
    "Which race and gender combination has the highest search rate",
    "What time of day sees the most traffic stops",
    "Average stop duration for different violations",
    "Are stops during the night more likely to lead to arrests",
    "Which violations are most associated with searches or arrests",
    "Which violations are most common among younger drivers (<25)",
    "Is there a violation that rarely results in search or arrest",
    "Which countries report the highest rate of drug-related stops",
    "Arrest rate by country and violation",
    "Country has the most stops with search conducted"

})

query_map = {
    "Top 10 vehicle number involed in drug related stops" : "SELECT vehicle_number, COUNT(*) AS drugs_related_stop FROM police_post WHERE drugs_related_stop = TRUE GROUP BY vehicle_number ORDER BY drugs_related_stop DESC LIMIT 10",
    "Vehicles were most frequently searched" : "SELECT vehicle_number, COUNT(*) AS search_count FROM police_post WHERE search_conducted = TRUE GROUP BY vehicle_number, search_conducted ORDER BY search_count DESC LIMIT 15",
    "Which driver age group had the highest arrest rate" : "SELECT CASE WHEN driver_age < 18 THEN '<18' WHEN driver_age BETWEEN 18 AND 30 THEN '18-30' WHEN driver_age BETWEEN 31 AND 45 THEN '31-45' WHEN driver_age BETWEEN 46 AND 60 THEN '46-60' ELSE '60+' END AS age_group, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate_percent FROM police_post GROUP BY age_group ORDER BY arrest_rate_percent DESC",
    "What is the gender distribution of drivers stopped in each country" : "SELECT country_name, driver_gender, COUNT(*) AS stop_count FROM police_post GROUP BY country_name, driver_gender ORDER BY country_name, stop_count DESC LIMIT 10",
    "Which race and gender combination has the highest search rate" : "SELECT driver_race, driver_gender, ROUND(SUM(search_conducted = TRUE)/ COUNT(*)*100, 2) AS search_rate_percentage FROM police_post GROUP BY driver_race, driver_gender ORDER BY search_rate_percentage DESC LIMIT 1",
    "What time of day sees the most traffic stops" : "SELECT CASE WHEN stop_time BETWEEN '00:00:00' AND '05:59:59' THEN 'Late Night' WHEN stop_time BETWEEN '06:00:00' AND '11:59:59' THEN 'Morning' WHEN stop_time BETWEEN '12:00:00' AND '17:59:59' THEN 'Afternoon' ELSE 'Evening' END AS Time_period, COUNT(*) AS Stop_count FROM police_post GROUP BY time_period ORDER BY stop_count DESC",
    "Average stop duration for different violations" : "SELECT violation, AVG(stop_duration) AS Avg_stop_duration FROM police_post GROUP BY violation ORDER BY Avg_stop_duration DESC",
    "Are stops during the night more likely to lead to arrests" : "SELECT CASE WHEN stop_time BETWEEN '00:00:00' AND '05:59:59' THEN 'Late Night' ELSE 'Day' END AS Time_period, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_rate_percent FROM police_post GROUP BY time_period",
    "Which violations are most associated with searches or arrests" : "SELECT Violation, ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS search_rate, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_rate FROM police_post GROUP BY violation ORDER BY search_rate DESC, arrest_rate DESC",
    "Which violations are most common among younger drivers (<25)" : "SELECT violation, COUNT(*) AS Count_young_drivers FROM police_post WHERE driver_age < 25 GROUP BY violation ORDER BY count_young_drivers DESC",
    "Is there a violation that rarely results in search or arrest" : "SELECT violation,COUNT(*) AS Total_stops, ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Search_rate, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_rate FROM police_post GROUP BY violation ORDER BY search_rate, arrest_rate",
    "Which countries report the highest rate of drug-related stops" : "SELECT country_name, ROUND(SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Drug_stop_rate FROM police_post GROUP BY country_name ORDER BY Drug_stop_rate DESC",
    "Arrest rate by country and violation" : "SELECT country_name, violation, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_rate FROM police_post GROUP BY country_name, violation ORDER BY Arrest_rate DESC",
    "Country has the most stops with search conducted" : "SELECT country_name, COUNT(*) AS Search_count FROM police_post WHERE search_conducted = TRUE GROUP BY country_name ORDER BY Search_count DESC LIMIT 1"

}   

if st.button(" Tap to Run :point_down:"):
    result = fetch_data(query_map[selected_query])
    if not result.empty:
        st.write(result)
    else:
        st.warning("No result was found :pensive:")


st.write(""" #### Complex level Insights: """)

selected_query_1 = st.selectbox("Select your question to run :blush:",{
    "Yearly Breakdown of Stops and Arrests by Country",
    "Driver Violation Trends Based on Age and Race",
    "Time Period Analysis of Stops", 
    "Violations with High Search and Arrest Rates",
    "Driver Demographics by Country",
    "Top 5 Violations with Highest Arrest Rates"

})

query_map_1 = {
    "Yearly Breakdown of Stops and Arrests by Country" : "SELECT country_name, EXTRACT(YEAR FROM Stop_date) AS stop_date, COUNT(*) AS total_stops, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_rate_percent, RANK() OVER (PARTITION BY Stop_date ORDER BY SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) DESC) AS Arrest_rank FROM police_post GROUP BY Country_name, Stop_date ORDER BY Stop_date, Arrest_rank",
    "Driver Violation Trends Based on Age and Race" : "WITH Age_race_summary AS (SELECT Driver_age, Driver_race, Violation, COUNT(*) AS Violation_count FROM police_post GROUP BY driver_age, driver_race, violation) SELECT ars.driver_age, ars.driver_race, ars.violation, ars.violation_count FROM Age_race_summary ars JOIN (SELECT driver_age, driver_race, MAX(violation_count) AS Max_count FROM age_race_summary GROUP BY driver_age, driver_race) top_violations ON ars.driver_age = top_violations.driver_age AND ars.driver_race = top_violations.driver_race AND ars.violation_count = top_violations.max_count ORDER BY ars.driver_race, ars.driver_age",
    "Time Period Analysis of Stops" : "SELECT EXTRACT(YEAR FROM stop_date) AS Year, EXTRACT(MONTH FROM stop_date) AS Month, EXTRACT(HOUR FROM stop_time) AS Hour, COUNT(*) AS stop_count FROM police_post GROUP BY Year, Month, Hour ORDER BY Year, Month, Hour",
    "Violations with High Search and Arrest Rates" : "SELECT violation, COUNT(*) AS Total_stops, SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS Total_searches, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS Total_arrests, ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Search_rate, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate, RANK() OVER (ORDER BY SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) DESC) AS Arrest_rank FROM police_post GROUP BY violation ORDER BY Arrest_rank LIMIT 10",
    "Driver Demographics by Country" : "SELECT country_name, AVG(driver_age) AS Avg_age, Driver_gender, Driver_race, COUNT(*) AS Stop_count FROM police_post GROUP BY Country_name, Driver_gender, Driver_race ORDER BY Country_name, Stop_count DESC",
    "Top 5 Violations with Highest Arrest Rates" : "SELECT violation, COUNT(*) AS Total_stops, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS Total_arrests, ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Arrest_rate_percent FROM police_post GROUP BY Violation ORDER BY Arrest_rate_percent DESC LIMIT 5"

}

if st.button(":point_down: Tap to Run"):
    result = fetch_data(query_map_1[selected_query_1])
    if not result.empty:
        st.write(result)
    else:
        st.warning("No result was found :pensive:")


st.header("What Happened Here? Fill in the Blanks to Find Out :smiley:")

st.write("Enter key details to automatically generate a clear, human-readable summary of the traffic stop.")


with st.form("Overall post logs"):

    stop_date = st.date_input("Select the Stop Date")
    stop_time = st.time_input("Select the Stop Time")
    country_name = st.text_input("Select your Country Name")
    vehicle_number = st.text_input("Enter your vehicle number")
    driver_gender = st.selectbox("Select your Gender",["Male", "Female", "Prefer not to say"])
    driver_age = st.number_input("Enter your Age", min_value=18, max_value=90, value = 27)
    driver_race = st.text_input("Enter your Race")
    search_conducted = st.selectbox("Is the search is conducted?", ["YES", "NO"])
    search_type = st.selectbox("Select the search type", ["Vehicle Search", "Frisk", "None"])
    stop_duration = st.selectbox("What is the stop duration", data["stop_duration"].dropna().unique())
    drugs_related_stop = st.selectbox("Is the stop is drug related?",["YES", "NO"])
    violation = st.selectbox("Violation Observed", ["DUI", "Speeding", "Seatblet", "Signal", "Other"])
    stop_outcome = st.selectbox("Select the Stop Outcome", ["Warning", "Citation", "Arrest"])
    is_arrested = st.selectbox("Was the driver arrested?", ["YES", "NO"])

    submit = st.form_submit_button("Get the Prediction")

if submit:
    filtered_data = data[
        (data["driver_gender"] == driver_gender) &
        (data["driver_age"] == driver_age) &
        (data["search_conducted"] == search_conducted) &
        (data["stop_duration"] == stop_duration) &
        (data["drugs_related_stop"] == drugs_related_stop)

    ]

    if not filtered_data.empty:
        Predicted_outcome = filtered_data["Stop Outcome"].mode()[0]
        Predicted_violation = filtered_data["Violation"].mode()[0]
    else:
        Predicted_outcome = "Warning"
        Predicted_violation = "Speeding"


    search_text = "a search was conducted" if search_conducted else "no search was conducted"
    drug_text = "drug-related" if drugs_related_stop else "not drug-related"


    st.markdown(f"""
        ** Quick summary of the Prediction **
                
    **Predicted Stop Outcome:** `{Predicted_outcome}` 

    **Predicted Violation:** `{Predicted_violation}`

    A `{driver_gender}` aged `{driver_age}` was stopped in `{country_name}` on `{stop_date}` at `{stop_time}` for `{Predicted_violation}`.  
    Vehicle `{vehicle_number}` was involved, and {search_text}.  
    The stop was {drug_text}, lasted `{stop_duration}`, and resulted in `{stop_outcome}`.  
    Arrest Status: `{is_arrested}`

"""
)








