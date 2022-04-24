import json
from pathlib import Path
from elosports.elo import Elo

def main():
    elo = Elo(k=20)
    ratings = json.loads(Path("k.json").read_text())
    for k, rating in ratings["choices"].items():
        elo.addPlayer(k, rating["rating"])
    power_rankings = sorted(elo.ratingDict.items(), key=lambda x:x[1], reverse=True)
    print(f"{'Choice':<35}{'Rating':<20}")
    for k, r in power_rankings:
        print(f"{k:<35}{r:<20.3f}")

if __name__ == "__main__":
    main()
