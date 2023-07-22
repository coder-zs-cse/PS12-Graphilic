import pandas as pd
import matplotlib.pyplot as plt

# Load the reviews data from a CSV file (change the file path accordingly)
reviews_data = pd.read_csv('../../Data/reviews1_data.csv')


def drawPiechart(month,year):
    # Assuming the data has the following columns: group, time, user_id, rating, total_votes, helpfulness_votes

    # Convert the 'time' column to a pandas datetime object
    # reviews_data['time'] = pd.to_datetime(reviews_data['time'])

    # Replace 'time_column' with the actual column name containing the timestamps
    # To filter by month and year, uncomment and use the following line:
    filtered_data = reviews_data[(reviews_data['year'] == year) & (reviews_data['month'] == month)]

    # Group the filtered data by 'group' and calculate the total interactions per category
    interactions_per_category = filtered_data.groupby('group')['rating'].sum()

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(interactions_per_category, labels=interactions_per_category.index, autopct='%1.1f%%', startangle=140)
    plt.title(f'User Interactions per Category in {month}-{year}')
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    plt.show()

drawPiechart(6,2000)