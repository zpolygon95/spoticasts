import argparse
import spotipy
import spotipy.util as util


class CustomSpotify(spotipy.Spotify):
    def user_playlist_add_episodes(
        self, user, playlist_id, eps, position=None
    ):
        """ Adds episodes to a playlist
            Parameters:
                - user - the id of the user
                - playlist_id - the id of the playlist
                - eps - a list of track URIs, URLs or IDs
                - position - the position to add the eps
        """
        plid = self._get_id("playlist", playlist_id)
        feps = [self._get_uri("episode", eid) for eid in eps]
        return self._post(
            "users/%s/playlists/%s/tracks" % (user, plid),
            payload=feps,
            position=position,
        )

    def user_playlist_add_all_episodes(self, user, playlist_id, eps, limit=100):
        """Repeatedly call self.user_playlist_add_episodes if necessary"""
        out = []
        for i in range(0, len(eps), limit):
            out.append(self.user_playlist_add_episodes(
                user, playlist_id,
                eps[i:i + limit]))
        return out

    def all_user_saved_shows(self):
        out = []
        offset = 0
        total = 1
        while offset < total:
            results = self.current_user_saved_shows(offset=offset)
            shows = results['items']
            total = results['total']
            offset += len(shows)
            out += shows
        return out

    def all_show_episodes(self, show_id):
        out = []
        offset = 0
        total = 1
        while offset < total:
            results = self.show_episodes(show_id, offset=offset)
            episodes = results['items']
            total = results['total']
            offset += len(episodes)
            out += episodes
        return out


def is_newer(episode, date):
    epdate = episode['release_date']
    return epdate >= date


def main(args):
    scope = 'playlist-modify-public,playlist-modify-private,user-library-read'
    token = util.prompt_for_user_token(args.username, scope)

    if token:
        sp = CustomSpotify(auth=token)
        sp.trace = False
        shows = sp.all_user_saved_shows()
        eps = []
        for show in shows:
            print(show['show']['name'], show['show']['id'])
            show_eps = sp.all_show_episodes(show['show']['id'])
            for ep in show_eps:
                ep['show'] = show['show']
            eps += show_eps
        recent_eps = [
            ep for ep in eps
            if is_newer(ep, args.date)]
        sorted_eps = sorted(recent_eps, key=lambda x: x['release_date'])
        for ep in sorted_eps:
            print(f'{ep["release_date"]} - {ep["show"]["name"]}: {ep["name"]}')
        sp.user_playlist_add_all_episodes(
            args.username, args.playlist_id,
            [ep['id'] for ep in sorted_eps])
    else:
        print("Can't get token for", args.username)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('username')
    p.add_argument('playlist_id')
    p.add_argument('date')
    main(p.parse_args())
