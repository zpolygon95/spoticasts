# Spoticasts #

Do you like podcasts? Do you want a podcast client that syncs your data between
muliple devices? Are you dissapointed by the level of support for podcasts in
Spotify?

This project solves <s>all your life's problems</s> <em>this problem</em> by
automatically generating podcast playlists in Spotify! With the press of a
button, all of the finished episodes are removed from your podcast playlist, and
all the the most recent unfinished episodes of your saved podcasts are added
chronologically by the date they were published.

## Project Status ##

Currently in the experimental phase, this project exists as a command line tool,
and isn't trivially "installable" by anyone without the client secret.

### Goals ###

+ <s>Functional Prototype</s>
+ Reduce total API calls
+ Prototype "service" (via simple web app?)
+ Additional features?

## Installation ##

If you want to get your hands dirty and register your own spotify integration
to use this project in it's current state, these are the steps I took:

1. Log in to the [Spotify Developer Dashboard][1]
2. Create a new app
3. Record the Client ID and Client Secret (each 32 digit hexadecimal numbers)
4. Add `http://localhost:8001/` to your app's Redirect URIs in the settings

The script itself requires Python 3 (I'm using 3.7.6) and the [Spotipy][2]
package. I'm using [Pipenv][3] as the project environment manager.

1. `git clone git@github.com/zpolygon95/spoticasts.git && cd spoticasts`
2. `pipenv install`

## Usage ##

```
usage: main.py [-h] [-m MODE] username [playlist_id]

positional arguments:
  username              The Spotify username
  playlist_id           The name of id of the playlist to use. "New Podcast
                        Episodes" by default

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  "empty" to empty the specified playlist. "refresh" to
                        remove finished episodes and add new episodes
                        (default)
```

### Caveats ###

If you use this script without having "finished" any episodes of a podcast you
have subscribed to, it will ruthlessly add every episode of that podcast to your
playlist! (That's what the `empty` mode was created for)

[1]: https://developer.spotify.com/dashboard/
[2]: https://spotipy.readthedocs.io/en/stable/
[3]: https://pipenv-fork.readthedocs.io/en/latest/
