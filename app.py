#!/Users/max_walker/moviedetective/bin/python3
from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Expanded Movie database
MOVIES = [
    {
        "title": "The Dark Knight",
        "clues": [
            {"type": "Year", "value": "2008"},
            {"type": "Genre", "value": "Action/Crime/Drama"},
            {"type": "Director", "value": "Christopher Nolan"},
            {"type": "Box Office", "value": "$1,004.6M"},
            {"type": "Lead Actor", "value": "Christian Bale"},
            {"type": "Famous Quote", "value": "Why so serious?"},
            {"type": "Oscar Wins", "value": "2"},
            {"type": "Runtime", "value": "152 minutes"}
        ]
    },
    {
        "title": "Jaws",
        "clues": [
            {"type": "Year", "value": "1975"},
            {"type": "Genre", "value": "Thriller/Adventure"},
            {"type": "Director", "value": "Steven Spielberg"},
            {"type": "Box Office", "value": "$470M"},
            {"type": "Lead Actor", "value": "Roy Scheider"},
            {"type": "Famous Quote", "value": "You're gonna need a bigger boat"},
            {"type": "Oscar Wins", "value": "3"},
            {"type": "Runtime", "value": "124 minutes"}
        ]
    },
    {
        "title": "The Godfather",
        "clues": [
            {"type": "Year", "value": "1972"},
            {"type": "Genre", "value": "Crime/Drama"},
            {"type": "Director", "value": "Francis Ford Coppola"},
            {"type": "Box Office", "value": "$245M"},
            {"type": "Lead Actor", "value": "Marlon Brando"},
            {"type": "Famous Quote", "value": "I'm gonna make him an offer he can't refuse"},
            {"type": "Oscar Wins", "value": "3"},
            {"type": "Runtime", "value": "175 minutes"}
        ]
    },
    {
        "title": "Pulp Fiction",
        "clues": [
            {"type": "Year", "value": "1994"},
            {"type": "Genre", "value": "Crime/Drama"},
            {"type": "Director", "value": "Quentin Tarantino"},
            {"type": "Box Office", "value": "$213.9M"},
            {"type": "Lead Actor", "value": "John Travolta"},
            {"type": "Famous Quote", "value": "Royale with cheese"},
            {"type": "Oscar Wins", "value": "1"},
            {"type": "Runtime", "value": "154 minutes"}
        ]
    },
    {
        "title": "The Matrix",
        "clues": [
            {"type": "Year", "value": "1999"},
            {"type": "Genre", "value": "Sci-Fi/Action"},
            {"type": "Director", "value": "The Wachowskis"},
            {"type": "Box Office", "value": "$463.5M"},
            {"type": "Lead Actor", "value": "Keanu Reeves"},
            {"type": "Famous Quote", "value": "I know kung fu"},
            {"type": "Oscar Wins", "value": "4"},
            {"type": "Runtime", "value": "136 minutes"}
        ]
    },
    {
        "title": "Forrest Gump",
        "clues": [
            {"type": "Year", "value": "1994"},
            {"type": "Genre", "value": "Drama/Romance"},
            {"type": "Director", "value": "Robert Zemeckis"},
            {"type": "Box Office", "value": "$678.2M"},
            {"type": "Lead Actor", "value": "Tom Hanks"},
            {"type": "Famous Quote", "value": "Life is like a box of chocolates"},
            {"type": "Oscar Wins", "value": "6"},
            {"type": "Runtime", "value": "142 minutes"}
        ]
    },
    {
        "title": "Jurassic Park",
        "clues": [
            {"type": "Year", "value": "1993"},
            {"type": "Genre", "value": "Sci-Fi/Adventure"},
            {"type": "Director", "value": "Steven Spielberg"},
            {"type": "Box Office", "value": "$914M"},
            {"type": "Lead Actor", "value": "Sam Neill"},
            {"type": "Famous Quote", "value": "Life finds a way"},
            {"type": "Oscar Wins", "value": "3"},
            {"type": "Runtime", "value": "127 minutes"}
        ]
    },
    {
        "title": "Titanic",
        "clues": [
            {"type": "Year", "value": "1997"},
            {"type": "Genre", "value": "Romance/Drama"},
            {"type": "Director", "value": "James Cameron"},
            {"type": "Box Office", "value": "$2.2B"},
            {"type": "Lead Actor", "value": "Leonardo DiCaprio"},
            {"type": "Famous Quote", "value": "I'm king of the world!"},
            {"type": "Oscar Wins", "value": "11"},
            {"type": "Runtime", "value": "195 minutes"}
        ]
    },
    {
        "title": "The Shawshank Redemption",
        "clues": [
            {"type": "Year", "value": "1994"},
            {"type": "Genre", "value": "Drama"},
            {"type": "Director", "value": "Frank Darabont"},
            {"type": "Box Office", "value": "$58.8M"},
            {"type": "Lead Actor", "value": "Tim Robbins"},
            {"type": "Famous Quote", "value": "Get busy living, or get busy dying"},
            {"type": "Oscar Wins", "value": "0"},
            {"type": "Runtime", "value": "142 minutes"}
        ]
    },
    {
        "title": "Avatar",
        "clues": [
            {"type": "Year", "value": "2009"},
            {"type": "Genre", "value": "Sci-Fi/Action"},
            {"type": "Director", "value": "James Cameron"},
            {"type": "Box Office", "value": "$2.9B"},
            {"type": "Lead Actor", "value": "Sam Worthington"},
            {"type": "Famous Quote", "value": "I see you"},
            {"type": "Oscar Wins", "value": "3"},
            {"type": "Runtime", "value": "162 minutes"}
        ]
    }
]

@app.route('/')
def index():
    # Initialize new game
    session['current_movie'] = random.choice(MOVIES)
    session['score'] = 100
    session['revealed_count'] = 1
    session['game_over'] = False
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    user_guess = data.get('guess', '').lower()
    current_movie = session.get('current_movie')
    score = session.get('score', 100)
    
    if user_guess == current_movie['title'].lower():
        message = f"Congratulations! You won with {score} points!"
        game_over = True
    else:
        score = max(0, score - 10)
        session['score'] = score
        if score <= 10:
            message = f"Game Over! The movie was {current_movie['title']}"
            game_over = True
        else:
            message = "Incorrect guess! Try again."
            game_over = False
    
    session['game_over'] = game_over
    return jsonify({
        'message': message,
        'score': score,
        'gameOver': game_over
    })

@app.route('/reveal', methods=['POST'])
def reveal_clue():
    revealed_count = session.get('revealed_count', 1)
    score = session.get('score', 100)
    current_movie = session.get('current_movie')
    
    if revealed_count < len(current_movie['clues']) and score > 10:
        revealed_count += 1
        score = max(0, score - 10)
        session['revealed_count'] = revealed_count
        session['score'] = score
        
    return jsonify({
        'clues': current_movie['clues'][:revealed_count],
        'score': score
    })

if __name__ == '__main__':
    app.run(debug=True)