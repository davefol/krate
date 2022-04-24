import sys
import json

def main():
    with open(sys.argv[1]) as fp:
        ratings = {
            "choices": {
                line.strip(): {
                    "rating": 1500,
                    "matches": 0
                }
                for line in fp.readlines()
            },
            "history": [],
        }
        print(json.dumps(ratings, indent=2))

if __name__ == "__main__":
    main()
