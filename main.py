
import praw
import os
from datetime import datetime
from flask import Flask

# --- Reddit API Setup ---
try:
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        username=os.getenv('REDDIT_USERNAME'),
        password=os.getenv('REDDIT_PASSWORD'),
        user_agent='DailySnarkBot by u/MinimumCorner1513'
    )
except Exception as e:
    print(f"Error connecting to Reddit: {e}")
    exit(1)

# Replace this with your actual subreddit name
subreddit_name = "LillyTino_"

# --- Flask Web Server Setup ---
app = Flask(__name__)

@app.route("/")
def post_snark():
    today = datetime.now().strftime("%B %d, %Y")
    post_title = f"Daily Snark – {today}"

    post_body = """
Welcome back to your regularly scheduled snark-fest! This is the place for all your eye-rolls, side-eyes, spicy takes, and popcorn-worthy moments.

Got a hot take that doesn't need its own post? Drop it here.  
Seen something absurd that made you cackle? We want it.  
Feel like dramatically whispering "girl…" at your screen? This thread was made for you.

Let the games begin.
"""

    # Prevent duplicate post if script is called more than once a day
    for submission in reddit.subreddit(subreddit_name).new(limit=5):
        if post_title in submission.title:
            return "Already posted today!"

    reddit.subreddit(subreddit_name).submit(title=post_title, selftext=post_body)
    return f"Posted: {post_title}"

# --- Run Flask App ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
