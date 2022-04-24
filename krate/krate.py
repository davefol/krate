"""
K Rate.
"""
import json
from pathlib import Path
import random

from elosports.elo import Elo
import pytermgui as ptg

def present_choices(k1, k2):
    ret = None
    with ptg.WindowManager() as manager:
        def choosek1(_):
            nonlocal ret
            ret = k1
            manager.stop()

        def choosek2(_):
            nonlocal ret
            ret = k2
            manager.stop()

        def chooseNeither(_):
            nonlocal ret
            ret = None
            manager.stop()

        def chooseNone(_):
            nonlocal ret
            manager.stop()
            quit()

        win = ptg.Window(
            ptg.Button(k1, onclick = choosek1),
            ptg.Button(k2, onclick = choosek2),
            ptg.Button("Neither", onclick = chooseNeither),
            ptg.Button("Exit", onclick = chooseNone)
        )
        win.center()
        win.set_title("Choose")
        manager.add(win, animate=False)
        manager.run()
    return ret


def get_probs(keys, ratings):
    matches = [ratings["choices"][key]["matches"] for key in keys]
    matches = [1 if m == 0 else 1/m for m in matches]
    matches_norm = sum(matches)
    if matches_norm > 0:
        return [m/matches_norm for m in matches]
    else:
        return [1/len(matches) for _ in matches]

def matchup(ratings, elo, out_path):
    keys = list(ratings["choices"])
    probs = get_probs(keys, ratings)
    k1 = random.choices(keys, probs)[0]
    keys = [k for k in keys if k != k1]
    probs = get_probs(keys, ratings)
    k2 = random.choices(keys, probs)[0]

    winner = present_choices(k1, k2)
    ratings["choices"][k1]["matches"] += 1
    ratings["choices"][k2]["matches"] += 1
    if winner is None:
        ratings["choices"][k1]["rating"] = 500
        ratings["choices"][k2]["rating"] = 500
        elo.ratingDict[k1] = 500
        elo.ratingDict[k2] = 500

    else:
        loser = k1 if k1 != winner else k2
        elo.gameOver(winner=winner, loser=loser, winnerHome=None)
        ratings["choices"][winner]["rating"] = elo.ratingDict[winner]
        ratings["choices"][loser]["rating"] = elo.ratingDict[loser]
        ratings["history"].append([winner, loser])

    Path(out_path).write_text(json.dumps(ratings, indent=2))
    
    
def main():
    elo = Elo(k=20)
    ratings = json.loads(Path("k.json").read_text())
    for k, rating in ratings["choices"].items():
        elo.addPlayer(k, rating["rating"])

    while True:
        if matchup(ratings, elo, "k.json"):
            break

if __name__ == "__main__":
    main()
