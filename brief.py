"""Fetch the day's top tech stories and turn them into a chat-style digest.

v1: stories come from Hacker News (free public API, no key needed).
The summary is written by Google's Gemini (free tier via Google AI Studio).

Usage:
    python brief.py            # needs GEMINI_API_KEY in the environment
"""

import os
import requests

HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Any current Gemini "flash" model works here; swap the name if Google renames it.
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.0-flash:generateContent"
)


def get_top_stories(limit=10):
    """Pull today's top Hacker News stories (title + link + score)."""
    ids = requests.get(HN_TOP, timeout=15).json()[:limit]
    stories = []
    for sid in ids:
        item = requests.get(HN_ITEM.format(sid), timeout=15).json()
        if item.get("type") == "story" and item.get("url"):
            stories.append(
                {
                    "title": item["title"],
                    "url": item.get("url", ""),
                    "score": item.get("score", 0),
                }
            )
    return stories


def summarize(stories):
    """Ask Gemini to write the morning briefing in a WhatsApp-friendly style."""
    key = os.environ["GEMINI_API_KEY"]
    bullets = "\n".join(f"- {s['title']} ({s['url']})" for s in stories)
    prompt = (
        "You are a fun, punchy tech news briefing bot. Below are today's top "
        "Hacker News stories.\n"
        "Write a WhatsApp-style morning briefing: a one-line greeting, then the "
        "5 most interesting stories, each with a 1-2 sentence plain-English "
        "explanation of what happened and why it matters. "
        "Call out the single biggest 'whoa' story of the day. "
        "Keep it under 250 words, casual tone, no markdown headers, no emojis overload."
        f"\n\nStories:\n{bullets}"
    )
    resp = requests.post(
        f"{GEMINI_URL}?key={key}",
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":
    stories = get_top_stories()
    print(f"Fetched {len(stories)} stories.")
    digest = summarize(stories)
    print(digest)
    with open("digest.txt", "w") as f:
        f.write(digest)
    print("\nSaved to digest.txt")
