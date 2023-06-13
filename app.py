from flask import Flask, flash, render_template, session, redirect, url_for
from forms import HangmanForm


app = Flask(__name__)
app.secret_key = "a/as/d/sc/wgeerw/gw"
word = "виселица"
hidden_word = list("_" * len(word))


players_data = {
    "player 1": {
        "correctly guessed letters": set(),
        "incorrectly guessed letters": set(),
        "score": 0,
    },
    "player 2": {
        "correctly guessed letters": set(),
        "incorrectly guessed letters": set(),
        "score": 0,
    },
}

players = []
for i in players_data:
    players.append(i)


@app.route("/")
def index():
    flash("Game started! Player 1, start guessing.", "info")

    form = HangmanForm()

    return redirect(url_for("game"))


@app.route("/game", methods=["get", "post"])
def game():
    def change_current_player(players):
        players.insert(0, players.pop())
        return players[0]

    def check_winner(hidden_word, players_data):
        if not ("_" in hidden_word):
            print("слово отгадано")

            if players_data["player 1"]["score"] > players_data["player 2"]["score"]:
                return "player 1"
            return "player 2"
            
        
    def count_score():
        players_data["player 1"]["score"] = len(
            players_data["player 1"]["correctly guessed letters"]
        ) - len(players_data["player 1"]["incorrectly guessed letters"])
        players_data["player 2"]["score"] = len(
            players_data["player 2"]["correctly guessed letters"]
        ) - len(players_data["player 2"]["incorrectly guessed letters"])

        

    form = HangmanForm()
    guess = ""
    current_player = change_current_player(players)

    if form.validate_on_submit():
        guess = form.guess.data

    if guess != "":
        if guess in word:
            for index_letter in range(len(word)):
                if guess == word[index_letter]:
                    hidden_word[index_letter] = guess
            players_data[current_player]["correctly guessed letters"].add(guess)

        else:
            players_data[current_player]["incorrectly guessed letters"].add(guess)

    count_score()
    winner = check_winner(hidden_word, players_data)

    return render_template(
        "game.html",
        current_player=current_player,
        form=form,
        hidden_word="".join(hidden_word),
        winner=winner,
        players_data=players_data
    )


@app.route("/clear")
def clear():
    session.clear()
    print("cleared")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
