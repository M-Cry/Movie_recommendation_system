import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./user_rating.csv', sep=',')

# get all the mean rating for all titles 
ratings = pd.DataFrame(df.groupby('title')['user_rating'].mean())

# get how many times a title has been rated
ratings['number_of_ratings'] = df.groupby('title')['user_rating'].count()

# plotting the joinplot to show the distribution of ratings and most ratring scores
sns.jointplot(x = 'user_rating', y = 'number_of_ratings', data = ratings)
# plt.show()

# creating the user-time interaction matrix 
# from it we can later create corelations to get our recomendations
data_matrix = df.pivot_table(index='user_id', columns='title', values='user_rating')

# most rated movies list
ratings.sort_values('user_rating', ascending=False).head(10)

np.seterr(divide='ignore', invalid='ignore')

aliens_user_ratings = data_matrix['Aliens in the Attic']

# find similar movies to (Aliens in the Attic) using correlation with other movies ratings
similar_to_aliens = data_matrix.corrwith(aliens_user_ratings)

# better display the recommendations
corr_aliens = pd.DataFrame(similar_to_aliens, columns = ['Correlation'])
corr_aliens.dropna(inplace=True)
corr_aliens.sort_values('Correlation', ascending=False).head()

# set up to refine the recommendations
corr_aliens = corr_aliens.join(ratings['number_of_ratings'])

# applying a filter to refine the recommendations
recommendations = corr_aliens[corr_aliens['number_of_ratings'] > 3].sort_values(by='Correlation', ascending=False).head()

# Read each movie title
for movie in recommendations.iterrows():
    recommended_movie_title = movie[0]
    print(recommended_movie_title)