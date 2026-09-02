# Now-playing proxy

Serves a small JSON document describing what is currently playing on the
site owner's Spotify account, so the static site can show it without ever
holding a Spotify credential.

## Why this exists

`GET /v1/me/player/currently-playing` needs a user access token, which
expires hourly and can only be renewed with a refresh token plus the app's
client secret. Those cannot live in a static site's JavaScript — anyone
could take them and read the account. This Worker keeps them and exposes
only the fields the card renders.

## Deploy

```
cd workers/now-playing
npx wrangler login
npx wrangler deploy
npx wrangler secret put SPOTIFY_CLIENT_ID
npx wrangler secret put SPOTIFY_CLIENT_SECRET
npx wrangler secret put SPOTIFY_REFRESH_TOKEN
```

Get the refresh token with `python3 scripts/spotify_get_refresh_token.py`
from the repository root.

## Response

```json
{
  "isPlaying": true,
  "title": "Time",
  "artist": "Pink Floyd",
  "album": "The Dark Side of the Moon",
  "albumArt": "https://i.scdn.co/image/...",
  "url": "https://open.spotify.com/track/...",
  "progressMs": 84213,
  "durationMs": 421000
}
```

When the player is idle it returns the most recently played track with
`isPlaying: false` and a `playedAt` timestamp, so the card has something to
show. If Spotify cannot be reached it returns `{"isPlaying": false,
"error": true}` — the card falls back to its quiet state rather than
surfacing the reason.

## Rate limits

The access token is held in the isolate until just before it expires, and
the response is cached for 12 seconds in Cloudflare's cache, so traffic to
Spotify stays at roughly one request per 12 seconds no matter how many
people are on the page.
