"""
Movie Rating System V1.py
Author: Rachel Given
Date Created: 28/08/2019
Last Edited: 03/09/2019
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
                print('Column names are {}'.format(", ".join(row)))
                line_count += 1
            else:
                line_count += 1
                
                Movies(row[0], row[1], row[2], row[3])
                id = row[0]
                title = row[1]
                year = row[2]
                genres = row[3]
                
                print("\tMovieId: {} Title: {} Year: {} Genres: {}".format(id, title, year, genres))

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
                print('Column names are {}'.format(", ".join(row)))
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
        if user.id in users:
            if user.id == user_id:
                CURRENT_USER = user
    return CURRENT_USER

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

    for user in similar_users_sets:
        if user != CURRENT_USER:
            similarity_value = similarity_index(CURRENT_USER, user)
            similar_users_dict.update({user:similarity_value})

    # Transfer the dictionary into an ordered list of users most similar to least
    for user_and_value in similar_users_dict:
        for user, value in (similar_users_dict.items(), key=lambda x:x[1], reverse=True):
            similar_user_list

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
    len(CURRENT_USER.return_liked())) | (len(user.return_liked())) | (
    len(CURRENT_USER.return_disliked())) | (len(user.return_disliked()))

    return similarity_value

if __name__ == "__main__":
    LIKED_RATING = "4" # Movies rated this score and above are liked
    movies = [] # List of all Movies
    ratings = [] # List of all Ratings
    users = [] # List of all Users
    
    # Import csv
    import_movies()
    import_ratings(LIKED_RATING)

    # Set the current user and number of recommendations
    current_user_id = '0'
    num_of_recommendations = 4

    # Store current user instance
    CURRENT_USER = set_current_user(current_user_id)
    
    



            
