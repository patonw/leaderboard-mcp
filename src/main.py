import redis
import os

LEADERBOARD = os.environ.get("LEADERBOARD_KEY", "leaderboard")


def main():
    r = redis.Redis()

    print(r.zincrby(LEADERBOARD, 1, "greetings"))
    print(r.zrevrangebyscore(LEADERBOARD, "+inf", 0, withscores=True, start=0, num=10))


if __name__ == "__main__":
    main()
