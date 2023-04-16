import asyncio
from datetime import datetime, timedelta
import json
import os
import aiohttp
from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error

from psychonaut.api.lexicons.app.bsky.graph.get_followers import (
    get_followers,
    GetFollowersReq,
)
from psychonaut.api.lexicons.app.bsky.graph.get_follows import (
    get_follows,
    GetFollowsReq,
)
from psychonaut.api.session import SessionFactory
from psychonaut.client import get_simple_client_session


def create_connection():
    conn = sqlite3.connect("graph_tasks.db")
    print(f"successful connection with sqlite version: {sqlite3.version}")
    return conn


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS graph_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor TEXT NOT NULL,
            last_collected TIMESTAMP NULL,
            created_at TIMESTAMP NOT NULL
        );
    """
    )
    cursor.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS actor_index ON graph_tasks (actor);"
    )
    print("Created table 'graph_tasks'.")


def mark_graph_task_collected(conn, actor, as_uncollected=False):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM graph_tasks WHERE actor = ?;
    """,
        (actor,),
    )
    result = cursor.fetchone()

    now = datetime.now()

    if result is None:
        cursor.execute(
            """
            INSERT INTO graph_tasks (actor, last_collected, created_at)
            VALUES (?, ?, ?);
        """,
            (actor, now, now),
        )
    else:
        cursor.execute(
            """
            UPDATE graph_tasks SET last_collected = ? WHERE actor = ?;
        """,
            (now, actor),
        )

    conn.commit()


def mark_graph_task_uncollected(conn, actor, as_uncollected=False):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM graph_tasks WHERE actor = ?;
    """,
        (actor,),
    )
    result = cursor.fetchone()

    now = datetime.now()

    if result is None:
        cursor.execute(
            """
            INSERT INTO graph_tasks (actor, last_collected, created_at)
            VALUES (?, null, ?);
        """,
            (actor, now),
        )

    conn.commit()


def get_actors_with_old_last_collected(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        a_week_ago = datetime.now() - timedelta(days=7)
        cursor.execute(
            """
            SELECT actor FROM graph_tasks
            WHERE last_collected < ? OR last_collected IS NULL;
        """,
            (a_week_ago,),
        )
        results = cursor.fetchall()
        return [r[0] for r in results]
    except Error as e:
        print(e)

def get_known_actors_count(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM graph_tasks;
        """,
        )
        results = cursor.fetchone()
        return results[0]
    except Error as e:
        print(e)


async def get_followers_for(sess, actor):
    cursor, last_cursor = None, None

    results = []

    while True:
        req = GetFollowersReq(actor=actor, limit=100, cursor=cursor)
        resp = await get_followers(sess, req)

        cursor = resp.cursor
        if cursor is None or len(resp.followers) == 0 or cursor == last_cursor:
            break
        last_cursor = cursor

        results.extend(resp.followers)

    return results


async def get_follows_for(sess, actor):
    cursor, last_cursor = None, None


    results = []

    while True:
        req = GetFollowsReq(actor=actor, limit=100, cursor=cursor)
        resp = await get_follows(sess, req)

        cursor = resp.cursor
        if cursor is None or len(resp.follows) == 0 or cursor == last_cursor:
            break
        last_cursor = cursor

        results.extend(resp.follows)

    return results


async def main(conn: sqlite3.Connection, output_json):
    async with get_simple_client_session() as sess:

        print(f"Known actors: {get_known_actors_count(conn)}")

        n_visits = 0
        while True:
            frontier = set(get_actors_with_old_last_collected(conn))
            if not frontier:
                break
            else:
                print(f"!Frontier: {len(frontier)}")

            while frontier:
                actor = frontier.pop()
                print(f"{n_visits:06d} Actor: {actor}")
                followers, follows = [], []

                try:
                    followers = await get_followers_for(sess, actor)
                except aiohttp.ClientResponseError as e:
                    print("\tClientResponseError", e, "on actor", actor)
                    continue
                except Exception as e:
                    print(f"\tError: {e}")
                    raise

                try:
                    follows = await get_follows_for(sess, actor)
                except aiohttp.ClientResponseError as e:
                    print("\tClientResponseError", e, "on actor", actor)
                    continue
                except Exception as e:
                    print(f"\tError: {e}")
                    raise

                output_json.write(
                    json.dumps(
                        {
                            "actor": actor,
                            "followers": followers,
                            "follows": follows,
                            "at": datetime.now().isoformat(),
                        }
                    )
                    + "\n"
                )

                mark_graph_task_collected(conn, actor)

                observed = set()
                for f in followers:
                    observed.add(f["handle"])
                for f in follows:
                    observed.add(f["handle"])

                for o in observed:
                    if o not in frontier:
                        mark_graph_task_uncollected(conn, o)

                print(f"\t{len(followers)} {len(follows)}")
                n_visits += 1


if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("BSKY_USERNAME", "generativist")
    password = os.getenv("BSKY_PASSWORD", "password")

    # with open("graph.jsonl", "r") as f:
    #     for line in f:
    #         data = json.loads(line)
    #         import pprint
    #         pprint.pprint(data)
    #         break

    # fail

    conn = create_connection()
    create_table(conn)

    mark_graph_task_uncollected(conn, "generativist.xyz")

    with open("graph.jsonl", "a") as f:
        asyncio.run(main(conn, f))
