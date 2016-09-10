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

    api = praw.Reddit(app_ua)
    api.set_oauth_app_info(app_id, app_secret, app_uri)
    api.refresh_access_information(app_refresh)

    get_reddit.singleton = api
    return get_reddit.singleton


def post_comic(comic):
    api = get_reddit()
    time.sleep(2)

    subreddit = os.environ.get('STRIPPOSTER_SUBREDDIT',
                               '/r/testingground4bots')

    try:
        reddit_post = api.submit(subreddit, comic.post_title,
                                 url=comic.post_url)
        comment = comic.post_comment
        if comment:
            comment = comment.rstrip() + "\n\n"

        comment += (
            "Ik ben een bot, _bliep_, _bloep_. Ik probeer strips te plaatsen "
            "kort  nadat de auteur ze online zet. Vind je dat ik en strip mis,"
            " of denk je dat er iets mis gaat? Maak dan een "
            "[issue](https://github.com/ondergetekende/stripposter/issues) "
            "aan. Ik word beheerd door /u/kvdveer")

        reddit_post.add_comment(comment)
    except praw.errors.AlreadySubmitted:
        pass
