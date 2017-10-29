import os
import time
import praw


def get_reddit():
    try:
        return get_reddit.singleton
    except AttributeError:
        pass

    # TODO: get from config file
    app_ua = os.environ.get("STRIPPOSTER_UA", "StripsPoster for /r/strips")
    app_id = os.environ["STRIPPOSTER_ID"]
    app_uri = os.environ["STRIPPOSTER_URI"]
    app_secret = os.environ["STRIPPOSTER_SECRET"]
    app_refresh = os.environ["STRIPPOSTER_REFRESH"]

    api = praw.Reddit(client_id=app_id, client_secret=app_secret, user_agent=app_ua,
                           refresh_token=app_refresh)

    get_reddit.singleton = api
    return get_reddit.singleton


def post_comic(comic):
    api = get_reddit()
    time.sleep(2)

    subreddit = os.environ.get('STRIPPOSTER_SUBREDDIT',
                               '/r/testingground4bots')

    if subreddit.startswith('/r/'):
        subreddit = subreddit[3:]

    subreddit = api.subreddit(subreddit)

    try:
        reddit_post = subreddit.submit(comic.post_title,
                                       url=comic.post_url,
                                       resubmit=True,
                                       send_replies=False)
        comment = comic.post_comment
        if comment:
            comment = comment.rstrip() + "\n\n"

        comment += (
            "Ik ben een bot, _bliep_, _bloep_. Ik probeer strips te plaatsen "
            "kort  nadat de auteur ze online zet. Vind je dat ik en strip mis,"
            " of denk je dat er iets mis gaat? Maak dan een "
            "[issue](https://github.com/ondergetekende/stripposter/issues) "
            "aan. Ik word beheerd door /u/kvdveer")

        reddit_post.reply(comment)
    except praw.errors.AlreadySubmitted:
        pass
