import pandas as pd
import matplotlib.pyplot as plt

# Load the profit data from a CSV file (change the file path accordingly)
profit_data = pd.read_csv('../../Data/reviews1_data.csv')

# Assuming the data has the following columns: time, profit

# Convert the 'time' column to a pandas datetime object

def continuousGraph(group,start,end):


    profit_data['datetime'] = pd.to_datetime(profit_data[['year', 'month', 'day']])
    # profit_data['datetime'] = pd.to_datetime(profit_data['datetime'])
    # Replace 'time_column' with the actual column name containing the timestamps
    # To filter by month and year, uncomment and use the following line:
    filtered_data = profit_data[(profit_data['datetime'] >= start) & (profit_data['datetime'] <= end)]
    # Sort the data by datetime in ascending order (optional but recommended)
    filtered_data.sort_values(by='datetime', inplace=True)
    # Create the graph
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['datetime'], filtered_data['profit'], marker='o', linestyle='-',color='purple')
    plt.xlabel('datetime')
    plt.ylabel('Profit')
    plt.title(f'Company Profit over datetime in {group}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()

continuousGraph('Book','2000-06-01','2000-06-30')