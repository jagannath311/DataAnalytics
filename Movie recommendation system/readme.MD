## Built an association rule-based movie recommender system
Implemented Apriori algorithm to mine frequent patterns from a user-movie ratings data to recommend movies to the user.

Input: A data set with 100836 ratings and 3683 tag applications across 9742
movies is given. It describes a 5-star rating activity from MovieLens, a movie
recommendation service.

All ratings are contained in the file ratings.csv. Each line of this file after the
header row represents one rating of one movie by one user and has the following
format: userId, movie, rating, and timestamp.

Movie information is contained in the file movies.csv. Each line of this file after
the header row represents one movie.
It has the following format: movieId, title, genres

Dataset Link: https://files.grouplens.org/datasets/movielens/ml-latest-small.zip

Output: Recommendations of movies to the user

Files Description: <br/>
ruleminer.py  - It will take the data and gives the association rules <br/>
recommender.py - It will take the data and the association rules generated above to generate recommendations


### commands to run
```python3 Teamclusters_ruleminer.py ratings.csv``` <br/>
```python3 Teamclusters_recommender.py movies.csv test_data.npy rules.npy```

