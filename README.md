### Purpose ###

Stripbot is a reddit bot which posts comics to reddit. It scrapes various comic sites, and posts to discover comics. If a new comic is discovered, it attempts to post it to Reddit. 

### Contributing ###

Please feel free to suggest comics by posting an [issue](https://github.com/ondergetekende/stripposter/issues). Note that the stripbot hosted by /u/kvdveer will only post Dutch comics to `/r/strips`. If you want to post to a different subreddit, you'll need to fork the repo, and host the bot yourself.

### Installation ###

You'll need:

* A reddit account for the bot
* An [application entry](https://ssl.reddit.com/prefs/apps/)
* Linux with Python 3 (windows may work too, but this guide will not be applicable)
* The dependencies in `requirements.txt`


First you'll need to create a configuration file. Stripbot is configured using environment variables, so the configuration file is simply a shell script:

```
export STRIPPOSTER_ID="your app_id"
export STRIPPOSTER_URI=https://127.0.0.1:65010/authorize_callback
export STRIPPOSTER_SECRET="your app_secret"
export STRIPPOSTER_REFRESH="your app_refresh_token"
export STRIPPOSTER_SUBREDDIT="/r/testingground4bots"
```



