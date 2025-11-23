import random
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret_key"  # change this before deploying

EMOJIS = ["😊", "👍", "🐍", "💕", "😡", "🐸", "🤖", "🔥", "🌟", "🥳", "😎", "🧠"]

def generate_board():
    numbers = list(range(0, 100))  # 0 to 99
    secret_emoji = random.choice(EMOJIS)

    board = []
    for num in numbers:
        if num % 9 == 0:
            emoji = secret_emoji
        else:
            emoji = random.choice(EMOJIS)
        board.append({"number": num, "emoji": emoji})

    session["board"] = board
    session["secret_emoji"] = secret_emoji

@app.route("/", methods=["GET"])
def instructions():
    """
    Page 1: Instructions.
    """
    return render_template("index.html")

@app.route("/board", methods=["GET"])
def board():
    """
    Page 2: Show the emoji grid (10x10).
    """
    generate_board()
    board = session.get("board", [])
    return render_template("board.html", board=board)

@app.route("/reveal", methods=["POST"])
def reveal():
    """
    Page 3: Reveal the emoji.
    """
    secret_emoji = session.get("secret_emoji")
    board = session.get("board")

    # If session expired or user jumped here, redirect them properly
    if secret_emoji is None or board is None:
        return redirect(url_for("instructions"))

    return render_template("result.html", secret_emoji=secret_emoji)

@app.route("/restart", methods=["GET"])
def restart():
    """
    Clear current game and go back to instructions.
    """
    session.pop("board", None)
    session.pop("secret_emoji", None)
    return redirect(url_for("instructions"))

if __name__ == "__main__":
    app.run(debug=True)
