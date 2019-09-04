"""
Movie Rating System V1.py
Author: Rachel Given
Date Created: 28/08/2019
Last Edited: 04/09/2019
Make a system where a user can be recommended movies based on movie ratings 
"""

class Movies:
    """
    This is a class for movies
    """
    def __init__(self, id, title, year, genres):
        """
        The constructor for Movies

        Parameters:
            id (int): ID for a movie
            title (str): Name of movie
            year (int): Year movie was released
            genres (list): Movies genres
        """
        self.id = id
        self.title = title
        self.year = year
        self.genres = genres
        movies.append(self)

class Ratings:
    """
    This is a class for ratings
    """
    def __init__(self, user_id, movie_id, rating):
        """
        The constructor for Ratings

        Parameters:
            user_id (str): User identification number
            movie_id (str): Movie identification number
            rating (str): Ratings given to a movie by the user
        """
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        ratings.append(self)

class User:
    """
    This is a class holds the user id and
    all the movies they've liked and disliked
    """
    def __init__(self, id):
        self.id = id
        self.liked = set()
        self.disliked = set()
        users.append(self)
        
    def add_liked(self, movie_id):
        self.liked.add(movie_id)

    def return_liked(self):
        return self.liked

    def add_disliked(self, movie_id):
        self.disliked.add(movie_id)

    def return_disliked(self):
        return self.disliked

def import_movies():
    """
    Load movie csv files to movies class
    """
    import csv
    with open('Movies.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            if line_count == 0: #Header row
                line_count += 1
            else:
                line_count += 1
                
                Movies(row[0], row[1], row[2], row[3])

def import_ratings(LIKED_RATING):
    """
    Load ratings csv files to ratings and user classes
    """
    import csv
    with open('Ratings.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0: #Header row
                line_count += 1
            else:
                line_count += 1
                Ratings(row[0], row[1], row[2])

                # Sorts users and their liked/disliked movies into sets
                user_id = row[0]
                exists = False
                
                for user in users:
                    if user.id == user_id:
                        exists = True
                        # Adds movies to liked or disliked for already present user
                        if row[2] <= '4':
                            user.add_liked(row[1])
                        else:
                            user.add_disliked(row[1])

                if not exists:
                    user = User(row[0])
                    # Adds movies to liked or disliked for new user
                    if row[2] <= '4':
                        user.add_liked(row[1])
                    else:
                        user.add_disliked(row[1])

def set_current_user(user_id):
    """
    Assign the current user to an instance
    """
    # Set the current user to do recommendations for
    CURRENT_USER = "" # Var to store instances of current user
    for user in users:
        if user.id == user_id:
            CURRENT_USER = user

    return CURRENT_USER

""" *** FINDING SIMILAR USERS *** """

def user_movies(user):
    """
    Return the liked and disliked movie sets for user
    """
    #Makes a set of all movies the user has rated
    movies = (user.return_liked() | user.return_disliked())
    return movies

def return_users_liked(movie):
    """
    Return the set of all the users who like a movie
    """
    # Create set if users liked movies
    users_liked = set()
    # Finds all users which like a movie
    for user in users:
        if movie in user.return_liked():
            users_liked.add(user)

    return users_liked

def return_users_disliked(movie):
    """
    Return the set of all the users who disliked a movie
    """
    # Create set if users dislike movies
    users_disliked = set()
    # Finds all users which dislike a movie
    for user in users:
        if movie in user.return_disliked():
            users_disliked.add(user)

    return users_disliked

def find_similar_users(CURRENT_USER):
    """
    Given a user, compute a list of other users who are similar
    Store the list in a database (in this case a dictionary), along with their
    similarity indicies
    Return the list of similar user in order of most to least similar
    """
    similar_users_set = set()
    similar_user_list = []
    similar_users_dict = {}

    # Create similar user set with all users who have rated a certain movie
    rated_movies = user_movies(CURRENT_USER)
    for movie in rated_movies:
        similar_users_set.update(return_users_liked(movie)|return_users_liked(movie))

    for user in similar_users_set:
        if user.id != CURRENT_USER.id:
            similarity_value = similarity_index(CURRENT_USER, user)
            similar_users_dict.update({user:similarity_value})

    # Transfer the dictionary into an ordered list of users most similar to least
    for user, value in sorted(similar_users_dict.items(), key=lambda x:x[1], reverse=True):
        similar_user_list.append(user)

    return similar_user_list

def similarity_index(CURRENT_USER, user):
    """
    Return the similarity index of two users  
    """
    # Calculates value between 1.0 and -1.0 shows the similarity of users movie taste
    similarity_value = ((len(CURRENT_USER.return_liked() & user.return_liked()))
    + (len(CURRENT_USER.return_disliked() & user.return_disliked()))
    - (len(CURRENT_USER.return_liked() & user.return_disliked()))
    - (len(CURRENT_USER.return_disliked() & user.return_liked()))
    ) / (
    len(CURRENT_USER.return_liked() | user.return_liked() | 
    CURRENT_USER.return_disliked() | user.return_disliked()))

    return similarity_value

def possibility_index(CURRENT_USER, movie):
    """
    Given a user and an unrated movie
    Find all users who have rated the movie
    Compare the similarity index and recommend a movie
    """

    # Finds the sum of the similarity indicies of all users who like a movie
    similarity_sum_liked = 0
    for user in return_user_liked(movie):
        if user.id != CURRENT_USER.id:
            similarity_sum += similarity_index(CURRENT_USER, user)

    # Finds the sum of the similarity indicies of all users who dislike a movie
    similarity_sum_disliked = 0
    for user in return_user_disliked(movie):
        if user.id != CURRENT_USER.id:
            similarity_sum_disliked += similarity_index(CURRENT_USER, user)

    #Caluculate and return the possibility of the user liking a movie
    possibilty_index = ((similarity_sum_liked - similarity_sum_disliked)/(
                        len(return_users_liked(movie)) + len(return_users_disliked(movie))))

    return possibility_index

""" *** GENERATING RECOMMENDATIONS *** """

def return_unrated(CURRENT_USER):
    """
    Returns a list of unrated movies
    """
    # Create a lsit to store unrated movies
    unrated_movies_ids = []
    for user in find_similar_users(CURRENT_USER):
        movies = user_movies(user)-user_movies(CURRENT_USER)

    for movie in movies:
        if movie not in unrated_movies_ids:
            unrated_movies_ids.append(movie)

    return unrated_movies_ids

def unrated_movie_possibilities(CURRENT_USER):
    """
    Store all items the user has not rated with possibility index
    and return dictionary
    """
    # Compute possibilities of a user liking a movie
    recommended_movies = {}

    for unrated in return_unrated(CURRENT_USER):
        possibility_index = possibility_index(CURRENT_USER, unrated)
        recommended_movies.update(unrated.id, possibility_index)

    return recommended_movies

def generate_recommendations(CURRENT_USER, num_recommendations):
    """
    Generate movie recommendations
    """
    # Get dictionary of unrated movies to be recommended
    recommended_movies = unrated_movie_possibilities(CURRENT_USER)

    movie_count = 0
    movies_sorted = sorted(recommended_movies.items(), key=lambda x:x[1])

    print("**Recommended Movies**")
    

if __name__ == "__main__":
    LIKED_RATING = "4" # Movies rated this score and above are liked
    movies = [] # List of all Movies
    ratings = [] # List of all Ratings
    users = [] # List of all Users
    
    # Import csv
    import_movies()
    import_ratings(LIKED_RATING)

    # Set the current user and number of recommendations
    current_user_id = '5'
    num_of_recommendations = 4

    # Store current user instance
    CURRENT_USER = set_current_user(current_user_id)
    
    #Find all the users who have rated the movies watched by current user
    similar_users = find_similar_users(CURRENT_USER)
    



            
