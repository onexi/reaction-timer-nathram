from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)
reaction_times = []  # Store reaction times
reaction_start_time = None  # Track when the button turns green

@app.route('/')
def home():
    return open("index.html").read()

@app.route('/start', methods=['GET'])
def start_timer():
    global reaction_start_time
    delay = random.randint(1, 20)  # Random delay between 1-20s
    reaction_start_time = time.time() + delay
    return jsonify({"delay": delay})

@app.route('/record', methods=['POST'])
def record_reaction():
    global reaction_start_time
    reaction_time = float(request.form.get("reaction_time"))
    click_time = time.time()
    
    if click_time < reaction_start_time:  # Clicking before green is cheating
        return "Too early! Cheating detected.", 400
    
    reaction_times.append(reaction_time)
    return "Reaction recorded!"

@app.route('/fastest', methods=['GET'])
def get_fastest():
    if reaction_times:
        fastest_time = min(reaction_times)
        # Round the fastest time to 3 decimal places
        return f"Fastest Time: {fastest_time:.3f}s"
    return "No times recorded yet."


if __name__ == '__main__':
    app.run(debug=True)