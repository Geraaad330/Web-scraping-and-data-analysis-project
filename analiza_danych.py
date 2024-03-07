import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def absolute_value(val):
    total = sum(unique_tanks_per_nation)  
    absolute = int(round(val*total/100.0)) 
    return "{}".format(absolute)

file_path = 'C:\\studia\\python\\projekt_web_scraping\\gotowy_projekt\\tanks_stats.csv'
data = pd.read_csv(file_path)

# DPM ==================================================================================================
dpm_data = data[data['Statistic'] == 'DPM'].copy()

dpm_data['Value'] = dpm_data['Value'].str.replace(',', '').astype(float)

dpm_data['Value'] = pd.to_numeric(dpm_data['Value'], errors='coerce')

average_dpm_per_nation = dpm_data.groupby('nation')['Value'].mean().reset_index()

avg_dpm_per_nation_sorted = average_dpm_per_nation.sort_values('Value', ascending=False)

sns.set(style="whitegrid")

plt.figure(figsize=(10, 8))
bars = plt.bar(avg_dpm_per_nation_sorted['nation'], avg_dpm_per_nation_sorted['Value'], color='skyblue')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')


plt.title('Średni DPM dla każdej nacji')
plt.xlabel('Nacja')
plt.ylabel('Średni DPM')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()


# Penetracja ========================================================================================================
penetration_data = data[data['Statistic'] == 'Penetration (mm)'].copy()
penetration_data['Value'] = pd.to_numeric(penetration_data['Value'], errors='coerce')
average_penetration_per_nation = penetration_data.groupby('nation')['Value'].mean().reset_index()

plt.figure(figsize=(10, 6))
penetration_barplot = sns.barplot(x='Value', y='nation', data=average_penetration_per_nation, color='lightgreen')
plt.title('Średnia penetracja (mm) dla czołgów różnych nacji')
plt.xlabel('Średnia penetracja (mm)')
plt.ylabel('Nacja')

for index, row in average_penetration_per_nation.iterrows():
    penetration_barplot.text(row.Value/2, index, round(row.Value, 2), color='black', ha="center")
plt.show()

reload_data = data[data['Statistic'] == 'Reload time (sec)'].copy()
reload_data['Value'] = pd.to_numeric(reload_data['Value'], errors='coerce')
average_reload_time_per_nation = reload_data.groupby('nation')['Value'].mean().reset_index()

plt.figure(figsize=(10, 6))
reload_barplot = sns.barplot(x='Value', y='nation', data=average_reload_time_per_nation, palette='Set2')
plt.title('Średni czas przeładowania (sekundy) dla czołgów różnych nacji')
plt.xlabel('Średni czas przeładowania (sekundy)')
plt.ylabel('Nacja')

for index, row in average_reload_time_per_nation.iterrows():
    reload_barplot.text(row.Value/2, index, round(row.Value, 2), color='black', ha="center")

plt.show()

for index, row in average_reload_time_per_nation.iterrows():
    reload_barplot.text(row.Value, index, round(row.Value, 2), color='black', ha="right")
plt.show()

# wykres kołowy - ilość czołgów ====================================================================================

unique_tanks_per_nation = data['Tank Name'].groupby(data['nation']).nunique()

plt.figure(figsize=(8, 8))
unique_tanks_per_nation.plot(kind='pie', autopct=absolute_value, startangle=140, colors=sns.color_palette('pastel'))
plt.title('Liczba unikalnych czołgów dla każdej nacji')
plt.ylabel('') 
plt.show()

# wykres - waga ====================================================================================
total_weight_data = data[data['Statistic'] == 'Total weight (kg)']
total_weight_data['Value'] = total_weight_data['Value'].str.replace(',', '').astype(float)

lightest_tanks = total_weight_data.nsmallest(10, 'Value')
heaviest_tanks = total_weight_data.nlargest(10, 'Value')

lightest_names = lightest_tanks['Tank Name'].values
lightest_weights = lightest_tanks['Value'].values
heaviest_names = heaviest_tanks['Tank Name'].values
heaviest_weights = heaviest_tanks['Value'].values

lightest_names_with_order = [f'{i+1}. {name}' for i, name in enumerate(lightest_names)]
heaviest_names_with_order = [f'{i+1}. {name}' for i, name in enumerate(heaviest_names)]

fig, ax = plt.subplots(2, 1, figsize=(10, 12))

ax[0].barh(lightest_names_with_order, lightest_weights, color='red')
ax[0].set_title('10 Najlżejszych Czołgów')
ax[0].set_xlabel('Waga (kg)')
ax[0].set_ylabel('Pozycja. Nazwa Czołgu')
for i, (weight, name) in enumerate(zip(lightest_weights, lightest_names_with_order)):
    ax[0].text(weight/2, i, f'{weight} kg', va='center', ha='right')
    

# Najcięższe czołgi z etykietami i numerami porządkowymi
ax[1].barh(heaviest_names_with_order, heaviest_weights, color='grey')
ax[1].set_title('10 Najcięższych Czołgów')
ax[1].set_xlabel('Waga (kg)')
ax[1].set_ylabel('Pozycja. Nazwa Czołgu')
for i, (weight, name) in enumerate(zip(heaviest_weights, heaviest_names_with_order)):
    ax[1].text(weight/2, i, f'{weight} kg', va='center', ha='right')

plt.tight_layout()
plt.show()

# wykres - top speed ====================================================================================
top_speed_data_with_nation = data[data['Statistic'] == 'Top speed (km/h)']
top_speed_data_with_nation['Value'] = pd.to_numeric(top_speed_data_with_nation['Value'], errors='coerce')

fastest_tanks_speed_nation = top_speed_data_with_nation.nlargest(10, 'Value')

fastest_tanks_names_nation = [f"{row['Tank Name']} ({row['nation']})" for index, row in fastest_tanks_speed_nation.iterrows()]
fastest_tanks_speeds_nation = fastest_tanks_speed_nation['Value'].values

plt.figure(figsize=(12, 7))
plt.plot(fastest_tanks_names_nation, fastest_tanks_speeds_nation, marker='o', linestyle='-', color='red')

for i, (name, speed) in enumerate(zip(fastest_tanks_names_nation, fastest_tanks_speeds_nation)):
    plt.text(name, speed, f'{speed} km/h', ha='right', va='bottom')

plt.title('10 Najszybszych Czołgów (Maksymalna Prędkość) z Nacją')
plt.xlabel('Nazwa Czołgu i Nacja')
plt.ylabel('Maksymalna Prędkość (km/h)')
plt.xticks(rotation=45, ha='right')
plt.grid(True)
plt.tight_layout()
plt.show()

