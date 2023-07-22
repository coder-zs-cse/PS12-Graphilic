import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the reviews data from a CSV file (change the file path accordingly)
reviews_data = pd.read_csv('../../Data/reviews1_data.csv')

# Assuming the data has the following columns: time, user_id, rating, total_votes, helpfulness_votes

# Data aggregation: group by rating and calculate average helpfulness_votes
heatmap_data = reviews_data.groupby('month')['rating'].mean().reset_index()

# Reshape the data for heatmap plotting
heatmap_data = heatmap_data.pivot(index='month', columns='rating', values='rating')

# Create the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Heatmap of Ratings In Current Trends')
plt.xlabel('Number of Ratings')
plt.ylabel('Rating')
plt.show()
