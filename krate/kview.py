import json
from pathlib import Path
from elosports.elo import Elo

def main():
    elo = Elo(k=20)
    ratings = json.loads(Path("k.json").read_text())
    for k, rating in ratings["choices"].items():
        elo.addPlayer(k, rating["rating"])
    power_rankings = sorted(elo.ratingDict.items(), key=lambda x:x[1], reverse=True)
    rated = sum([r["matches"] for r in ratings["choices"].values()]) / 2
    not_rated = len([r for r in ratings["choices"].values() if r["matches"] == 0])
    print(f"You've judged {rated} match ups.")
    print(f"You haven't rated {not_rated} choices.")
    print(f"{'Choice':<35}{'Rating':<20}{'Matches':<20}")
    for k, r in power_rankings:
        m = ratings["choices"][k]["matches"]
        print(f"{k:<35}{r:<20.3f}{m:<20}")

if __name__ == "__main__":
    main()
