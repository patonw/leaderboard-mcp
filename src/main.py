import os
from math import inf
from dataclasses import dataclass
from typing import Annotated

import redis
from fastmcp import FastMCP

LEADERBOARD = os.environ.get("LEADERBOARD", "leaderboard")
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
mcp = FastMCP("leaderboard")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


# Using a dataclass gives some structure to the output results but is optional.
# You could return ad-hoc dicts or tuples instead
@dataclass
class Entry:
    value: str
    score: float


# FastMCP doesn't seem to behave correctly on empty sets
@mcp.tool
def list_leaders(
    board: Annotated[str, "Leaderboard to query"] = LEADERBOARD,
    limit: Annotated[int, "Maximum number of results"] = 10,
) -> list[Entry]:
    """Returns a list of the top values with their respective scores"""
    results = r.zrevrangebyscore(board, inf, 0, withscores=True, start=0, num=limit)
    return [Entry(value=k, score=v) for (k, v) in results]


@mcp.tool
def increment_scores(
    items: Annotated[list[str], "A list of values to increment"],
    board: Annotated[str, "Leaderboard to update"] = LEADERBOARD,
) -> list[Entry]:
    """Increment values by 1 and return each value with its new score"""

    return [Entry(value=item, score=r.zincrby(board, 1, item)) for item in items]


def main():
    mcp.run()


if __name__ == "__main__":
    for x in r.zrevrangebyscore(LEADERBOARD, inf, 0, withscores=True, start=0, num=10):
        print(x)
    # print(r.zincrby(LEADERBOARD, 1, "asdf"))
