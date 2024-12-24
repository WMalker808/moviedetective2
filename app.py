from flask import Flask, render_template, request, jsonify, session
from movies import MOVIES
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

@app.route('/give-up', methods=['POST'])
def give_up():
    current_movie = session.get('current_movie')
    message = f"You gave up! The movie was {current_movie['title']}."
    
    # Start new game
    new_movie = random.choice(MOVIES)
    while new_movie == current_movie:  # Ensure we don't get the same movie
        new_movie = random.choice(MOVIES)
    
    # Reset all session variables
    session['current_movie'] = new_movie
    session['score'] = 100  # Reset to starting score for new game
    session['revealed_count'] = 1
    session['game_over'] = False
    
    return jsonify({
        'message': message,
        'score': 100,
        'newGame': True,
        'gameOver': False
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

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
