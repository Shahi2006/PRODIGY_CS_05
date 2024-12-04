import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Load the dataset
df_accidents = pd.read_csv('accidents_2017_to_2023_english.csv')

# Data Cleaning and Preparation
df_accidents['inverse_data'] = pd.to_datetime(df_accidents['inverse_data'])
df_accidents['hour'] = pd.to_datetime(df_accidents['hour'], format='%H:%M:%S').dt.hour
df_accidents['year'] = df_accidents['inverse_data'].dt.year
df_accidents['month'] = df_accidents['inverse_data'].dt.month

# 1. Accident Trend Analysis: By Hour and Day of the Week
accidents_by_hour = df_accidents['hour'].value_counts().sort_index()
accidents_by_day = df_accidents['week_day'].value_counts()

plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
sns.lineplot(x=accidents_by_hour.index, y=accidents_by_hour.values)
plt.title('Accidents by Time of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Accidents')

plt.subplot(1, 2, 2)
sns.barplot(x=accidents_by_day.index, y=accidents_by_day.values)
plt.title('Accidents by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Accidents')
plt.tight_layout()
plt.show()

# 2. Weather and Road Condition Analysis
plt.figure(figsize=(12, 5))
sns.countplot(data=df_accidents, y='wheather_condition', order=df_accidents['wheather_condition'].value_counts().index)
plt.title('Accidents by Weather Condition')
plt.xlabel('Number of Accidents')
plt.ylabel('Weather Condition')
plt.show()

plt.figure(figsize=(12, 5))
sns.countplot(data=df_accidents, y='road_type', order=df_accidents['road_type'].value_counts().index)
plt.title('Accidents by Road Type')
plt.xlabel('Number of Accidents')
plt.ylabel('Road Type')
plt.show()

# 3. Accident Severity Analysis
severity_counts = df_accidents[['deaths', 'severely_injured', 'slightly_injured']].sum()
severity_counts.plot(kind='bar', figsize=(8, 5), color=['red', 'orange', 'blue'])
plt.title('Accident Severity (Total Injuries and Deaths)')
plt.xlabel('Severity Type')
plt.ylabel('Count')
plt.show()

# 4. Geospatial Hotspot Visualization (Heatmap)
# Filter data for valid latitude and longitude entries
valid_locations = df_accidents.dropna(subset=['latitude', 'longitude'])
map_accidents = folium.Map(location=[valid_locations['latitude'].mean(), valid_locations['longitude'].mean()], zoom_start=6)

# Create heatmap data
heatmap_data = valid_locations[['latitude', 'longitude']].values.tolist()
HeatMap(heatmap_data).add_to(map_accidents)

# Save map to an HTML file (optional)
map_accidents.save('accident_hotspots.html')
