/* =============================================================================
   Now-playing proxy for aria-amini.ir

   The site is static, so it has nowhere to keep a Spotify refresh token — put
   one in client-side JS and anyone can read the account with it. This Worker
   holds the three secrets, trades the refresh token for an access token, and
   hands the page back only the few public fields it needs to draw a card.

   Two layers of caching, both of which matter:
     - the access token is kept in the isolate until shortly before it expires,
       so a poll costs one Spotify call rather than two
     - the response itself is cached for CACHE_SECONDS, so a hundred people on
       the page at once is still one Spotify call every CACHE_SECONDS rather
       than a hundred — this is what keeps us clear of the rate limit

   Secrets (set with `npx wrangler secret put <NAME>`, never committed):
     SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN
   ============================================================================= */

const ALLOWED_ORIGINS = [
  "https://aria-amini.ir",
  "https://www.aria-amini.ir",
  "https://amini-aria.github.io",
];
const CACHE_SECONDS = 12;

let tokenCache = { value: null, expiresAt: 0 };

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin)
    ? origin
    : origin && /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin)
    ? origin // local development
    : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allowed,
    "Vary": "Origin",
    "Cache-Control": `public, max-age=${CACHE_SECONDS}`,
    "Content-Type": "application/json; charset=utf-8",
  };
}

async function getAccessToken(env) {
  const now = Date.now();
  if (tokenCache.value && now < tokenCache.expiresAt) return tokenCache.value;

  const basic = btoa(`${env.SPOTIFY_CLIENT_ID}:${env.SPOTIFY_CLIENT_SECRET}`);
  const res = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      Authorization: `Basic ${basic}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: env.SPOTIFY_REFRESH_TOKEN,
    }),
  });
  if (!res.ok) throw new Error(`token refresh failed: ${res.status}`);

  const data = await res.json();
  // renew a minute early rather than racing the expiry
  tokenCache = {
    value: data.access_token,
    expiresAt: now + (data.expires_in - 60) * 1000,
  };
  return tokenCache.value;
}

function trackPayload(item, extra) {
  return {
    title: item.name,
    artist: (item.artists || []).map((a) => a.name).join(", "),
    album: item.album ? item.album.name : null,
    albumArt: item.album && item.album.images && item.album.images.length
      ? item.album.images[item.album.images.length > 1 ? 1 : 0].url
      : null,
    url: item.external_urls ? item.external_urls.spotify : null,
    durationMs: item.duration_ms || null,
    ...extra,
  };
}

async function nowPlaying(env) {
  const token = await getAccessToken(env);
  const auth = { Authorization: `Bearer ${token}` };

  const live = await fetch(
    "https://api.spotify.com/v1/me/player/currently-playing?additional_types=track",
    { headers: auth }
  );

  // 204 means the player is idle; anything playing that isn't a track (a
  // podcast, an ad) has no item we can render either
  if (live.status === 200) {
    const data = await live.json();
    if (data && data.item && data.is_playing) {
      return trackPayload(data.item, {
        isPlaying: true,
        progressMs: data.progress_ms || 0,
      });
    }
  } else if (live.status !== 204) {
    throw new Error(`currently-playing failed: ${live.status}`);
  }

  // idle: show the last thing that was played rather than an empty box
  const recent = await fetch(
    "https://api.spotify.com/v1/me/player/recently-played?limit=1",
    { headers: auth }
  );
  if (recent.ok) {
    const data = await recent.json();
    const first = data.items && data.items[0];
    if (first && first.track) {
      return trackPayload(first.track, {
        isPlaying: false,
        playedAt: first.played_at || null,
      });
    }
  }

  return { isPlaying: false };
}

export default {
  async fetch(request, env, ctx) {
    const origin = request.headers.get("Origin") || "";
    const headers = corsHeaders(origin);

    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: { ...headers, "Access-Control-Allow-Methods": "GET, OPTIONS" },
      });
    }
    if (request.method !== "GET") {
      return new Response(JSON.stringify({ error: "method not allowed" }), {
        status: 405,
        headers,
      });
    }

    // one shared cache entry for everyone, keyed without the Origin so that
    // visitors don't each get their own copy
    const cache = caches.default;
    const cacheKey = new Request(new URL(request.url).origin + "/now-playing", {
      method: "GET",
    });

    const hit = await cache.match(cacheKey);
    if (hit) {
      const body = await hit.text();
      return new Response(body, { headers });
    }

    try {
      const payload = await nowPlaying(env);
      const body = JSON.stringify(payload);
      ctx.waitUntil(
        cache.put(
          cacheKey,
          new Response(body, {
            headers: {
              "Content-Type": "application/json; charset=utf-8",
              "Cache-Control": `public, max-age=${CACHE_SECONDS}`,
            },
          })
        )
      );
      return new Response(body, { headers });
    } catch (err) {
      // the card just stays in its quiet state; never leak the reason
      return new Response(JSON.stringify({ isPlaying: false, error: true }), {
        status: 200,
        headers: { ...headers, "Cache-Control": "public, max-age=5" },
      });
    }
  },
};
