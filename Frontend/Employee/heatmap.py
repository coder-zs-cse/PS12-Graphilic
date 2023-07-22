import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the reviews data from a CSV file (change the file path accordingly)
reviews_data = pd.read_csv('../../Data/reviews1_data.csv')

# Assuming the data has the following columns: time, user_id, rating, total_votes, helpfulness_votes

# Data aggregation: group by rating and calculate average helpfulness_votes
# filter group Book from reveiws_data

def getHeatMap(group,month,year):

    heatmap_data = reviews_data[(reviews_data['group'] == group) & (reviews_data['year'] == year)].groupby('month')['rating','helpful'].mean().reset_index()
    # Reshape the data for heatmap plotting
    heatmap_data = heatmap_data.pivot(index='month', columns='rating', values='helpful')

    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Heatmap of Ratings In Current Trends')
    plt.xlabel('Number of Ratings')
    plt.ylabel('Rating')
    plt.show()

getHeatMap('Book',6,2000)