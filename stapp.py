import streamlit as st
import sqlite3
import pandas as pd
import pymysql

connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="earthquake"
)
cursor = connection.cursor()
st.title("GOLBAL SEISMIC TREND")
option = st.selectbox(
        "select a Query",
        ("Top 10 strongest earthquakes (mag)",
         "Top 10 deepest earthquakes (depth_km)",
  "Shallow earthquakes < 50 km and mag > 7.5",
 "Average depth per continent",
 "Average magnitude per magnitude type (magType)",
 "Year with most earthquakes",
"Month with highest number of earthquakes",
 "Day of week with most earthquakes",
 "Count of earthquakes per hour of day",
"Most active reporting network (net)",
 "Top 5 places with highest casualties",
 "Total estimated economic loss per continent",
 "Count of reviewed vs automatic earthquakes (status)",
 "Count by earthquake type (type)",
 "Number of earthquakes by data type (types)",
 "Average RMS and gap per continent",
  "Events with high station coverage (nst > threshold)",
  "Number of tsunamis triggered per year",
  "Count earthquakes by alert levels (red, orange, etc.)",
"Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years",         	
"Find countries that have experienced both shallow and deep earthquakes within the same month",
"Compute the year-over-year growth rate in the total number of earthquakes globally",
 "List the 3 most seismically active regions by combining both frequency and average magnitude",
 "For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator",
 "Identify countries having the highest ratio of shallow to deep earthquakes",
 "Find the average magnitude difference between earthquakes with tsunami alerts and those without",
 "Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)",
 "Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour",
 "Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)"),
        )
if option == "Top 10 strongest earthquakes (mag)":
    df = pd.read_sql("""
        SELECT *
        FROM earthquakes
        ORDER BY mag DESC
        LIMIT 10
    """, connection)
    st.dataframe(df)

elif option == "Top 10 deepest earthquakes (depth_km)":
    df = pd.read_sql("""
        SELECT *
        FROM earthquakes
        ORDER BY depth_km DESC
        LIMIT 10
    """, connection)
    st.dataframe(df)

elif option == "Shallow earthquakes < 50 km and mag > 7.5":
    df = pd.read_sql("""
        SELECT *
        FROM earthquakes
        WHERE depth_km < 50
          AND mag > 7.5
    """, connection)
    st.dataframe(df)

elif option == "Average magnitude per magnitude type (magType)":
    df = pd.read_sql("""
        SELECT
              mag,
    AVG(mag) AS avg_mag
    FROM earthquakes
    GROUP BY mag
    ORDER BY avg_mag DESC;
    """, connection)
    st.dataframe(df)
    
elif option == "Year with most earthquakes":
    df = pd.read_sql("""
       SELECT
    EXTRACT(YEAR FROM time) AS earthquake_year,
    COUNT(*) AS earthquake_count
    FROM earthquakes
    GROUP BY EXTRACT(YEAR FROM time)
    ORDER BY earthquake_count DESC
    LIMIT 1;
    """, connection)
    st.dataframe(df)
elif option == "Month with highest number of earthquakes":
    df = pd.read_sql("""
       SELECT
    EXTRACT(MONTH FROM time) AS earthquake_month,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY EXTRACT(MONTH FROM time)
ORDER BY earthquake_count DESC
LIMIT 1;
    """, connection)
    st.dataframe(df)
elif option == "Day of week with most earthquakes":
    df = pd.read_sql("""
       SELECT
    DAYNAME(time) AS day_of_week,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY DAYNAME(time)
ORDER BY earthquake_count DESC
LIMIT 1;
    """, connection)
    st.dataframe(df)
elif option == "Count of earthquakes per hour of day":
    df = pd.read_sql("""
       SELECT
    HOUR(time) AS hour_of_day,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY HOUR(time)
ORDER BY hour_of_day;
    """, connection)
    st.dataframe(df)
elif option == "Most active reporting network (net)":
    df = pd.read_sql("""
       SELECT
    net,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY net
ORDER BY earthquake_count  DESC
LIMIT 1;
    """, connection)
    st.dataframe(df)
elif option == "Count of reviewed vs automatic earthquakes (status)":
    df = pd.read_sql("""
       SELECT
    status,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY status
ORDER BY earthquake_count DESC;
    """, connection)
    st.dataframe(df)
elif option == "Count by earthquake type (type)":
    df = pd.read_sql("""
       SELECT
    type,
    COUNT(*) AS earthquake_count
FROM earthquakes
GROUP BY type
ORDER BY earthquake_count DESC;
    """, connection)
    st.dataframe(df)
elif option == "Number of earthquakes by data type (types)":
    df = pd.read_sql("""
        SELECT
            types,
            COUNT(*) AS total_earthquakes
        FROM earthquakes
        GROUP BY types
        ORDER BY total_earthquakes DESC
    """, connection)
    st.dataframe(df)
elif option == "Average RMS and gap per continent":
    df = pd.read_sql("""
        WITH earthquake_continent AS (
    SELECT
        rms,
        gap,
        CASE
            WHEN latitude BETWEEN -35 AND 37
                 AND longitude BETWEEN -20 AND 55
                THEN 'Africa'

            WHEN latitude BETWEEN 15 AND 85
                 AND longitude BETWEEN -170 AND -50
                THEN 'North America'

            WHEN latitude BETWEEN -60 AND 15
                 AND longitude BETWEEN -90 AND -30
                THEN 'South America'

            WHEN latitude BETWEEN -50 AND 10
                 AND longitude BETWEEN 110 AND 180
                THEN 'Oceania'

            WHEN latitude < -60
                THEN 'Antarctica'

            ELSE 'Europe/Asia'
        END AS continent
    FROM earthquakes
)
SELECT
    continent,
    AVG(rms) AS avg_rms,
    AVG(gap) AS avg_gap
FROM earthquake_continent
GROUP BY continent
ORDER BY continent;
    """, connection)
    st.dataframe(df)
elif option == "Events with high station coverage (nst > threshold)":
    df = pd.read_sql("""
        SELECT
            id,
            time,
            place,
            mag,
            nst,
            alert
  FROM earthquakes
  WHERE nst > 50
  ORDER BY nst DESC;
    """, connection)
    st.dataframe(df)
elif option == "Number of tsunamis triggered per year":
    df = pd.read_sql("""
        SELECT
    EXTRACT(YEAR FROM time) AS year,
    COUNT(*) AS tsunami_count
FROM earthquakes
WHERE tsunami = 1
GROUP BY EXTRACT(YEAR FROM time)
ORDER BY year;
    """, connection)
    st.dataframe(df)
elif option == "Count earthquakes by alert levels (red, orange, etc.)":
    df = pd.read_sql("""
        SELECT
    alert,
    COUNT(*) AS earthquake_count
FROM earthquakes
WHERE alert IN ('red', 'orange', 'yellow', 'green')
GROUP BY alert
ORDER BY
    CASE alert
        WHEN 'red' THEN 1
        WHEN 'orange' THEN 2
        WHEN 'yellow' THEN 3
        WHEN 'green' THEN 4
    END;
    """, connection)
    st.dataframe(df)
elif option == "Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years":
    df = pd.read_sql("""
        SELECT
    place,
    COUNT(*) AS earthquake_count,
    ROUND(AVG(mag), 2) AS avg_mag,
    ROUND(COUNT(*) * AVG(mag), 2) AS seismic_activity_score
FROM earthquakes
GROUP BY place
ORDER BY seismic_activity_score DESC
LIMIT 3;
    """, connection)
    st.dataframe(df)
elif option == "Find countries that have experienced both shallow and deep earthquakes within the same month":
    df = pd.read_sql("""
        SELECT
    Place,
    YEAR(time) AS year,
    MONTH(time) AS month
FROM earthquakes
GROUP BY Place, YEAR(time), MONTH(time)
HAVING
    SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) > 0
    AND
    SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) > 0
ORDER BY place, year, month;

    """, connection)
    st.dataframe(df)
elif option == "Compute the year-over-year growth rate in the total number of earthquakes globally":
    df = pd.read_sql("""
        WITH yearly_counts AS (
            SELECT
                YEAR(time) AS year,
                COUNT(*) AS total_earthquakes
            FROM earthquakes
            GROUP BY YEAR(time)
        )
        SELECT
            year,
            total_earthquakes,
            LAG(total_earthquakes) OVER (ORDER BY year) AS previous_year,
            ROUND(
                (
                    (total_earthquakes - LAG(total_earthquakes) OVER (ORDER BY year))
                    / LAG(total_earthquakes) OVER (ORDER BY year)
                ) * 100,
                2
            ) AS growth_rate_percent
        FROM yearly_counts
        ORDER BY year
    """, connection)

    st.dataframe(df)
elif option == "List the 3 most seismically active regions by combining both frequency and average magnitude":
    df = pd.read_sql("""
        SELECT
            place,
            COUNT(*) AS total_earthquakes,
            ROUND(AVG(mag), 2) AS avg_magnitude
        FROM earthquakes
        GROUP BY place
        ORDER BY total_earthquakes DESC, avg_magnitude DESC
        LIMIT 3
    """, connection)

    st.subheader("Top 3 Most Seismically Active Regions")
    st.dataframe(df)
elif option == "For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator":
    df = pd.read_sql("""
        SELECT
            place,
            ROUND(AVG(depth_km), 2) AS avg_depth
        FROM earthquakes
        WHERE latitude BETWEEN -5 AND 5
        GROUP BY place
        ORDER BY avg_depth DESC
    """, connection)
    st.dataframe(df)
elif option == "Identify countries having the highest ratio of shallow to deep earthquakes":
    df = pd.read_sql("""
        SELECT
    place,
    SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) AS shallow_count,
    SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) AS deep_count,
    ROUND(
        SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) /
        NULLIF(SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END), 0),
        2
    ) AS shallow_deep_ratio
FROM earthquakes
GROUP BY place
ORDER BY shallow_deep_ratio DESC;
    """, connection)
    st.dataframe(df)
elif option == "Find the average magnitude difference between earthquakes with tsunami alerts and those without":
    df = pd.read_sql("""
        SELECT
    tsunami,
    ROUND(AVG(mag), 2) AS avg_magnitude
FROM earthquakes
GROUP BY tsunami;
    """, connection)

    st.dataframe(df)
elif option == "Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)":
    df = pd.read_sql("""
        SELECT
    place,
    COUNT(*) AS deep_focus_earthquakes
FROM earthquakes
WHERE depth_km > 300
GROUP BY place
ORDER BY deep_focus_earthquakes DESC
LIMIT 10;

    """, connection)

    st.dataframe(df)


    