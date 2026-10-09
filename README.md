# Boardify OAuth

Minimal GitHub OAuth provider that lets [Sveltia CMS](https://github.com/sveltia/sveltia-cms) authenticate editors of Boardify.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/codeforschools/boardify-oauth)

## Deploy to Heroku

1. Create a [GitHub OAuth App](https://github.com/settings/developers). The callback URL must be `https://<your-heroku-app>.herokuapp.com/callback`; you can set a placeholder and update it after deploying.
2. Click the **Deploy** button above and fill in the config vars (table below). `SECRET_KEY` is generated for you.
3. Update the OAuth App's callback URL to the new app's URL if you used a placeholder.

## Setup

1. Create a GitHub OAuth App. Set the callback URL to `https://<this-server>/callback`.
2. Configure environment variables (or a `.env` file, see `.env.example`):

| Variable | Description |
| --- | --- |
| `OAUTH_CLIENT_ID` / `OAUTH_CLIENT_SECRET` | GitHub OAuth App credentials |
| `SECRET_KEY` | Random string used to sign the session cookie (OAuth `state`) |
| `ALLOWED_ORIGINS` | Comma-separated origins of the Boardify CMS; tokens are only posted to these |
| `GIT_HOSTNAME` | Optional, GitHub Enterprise URL |
| `SCOPES` | Optional, default `repo,user` |

3. Run: `uv run flask --app app run` (dev) or `uv run gunicorn app:app` (production, see `Procfile`).

## Sveltia CMS config

```yaml
backend:
  name: github
  repo: <owner>/<boardify-repo>
  branch: main
  base_url: https://<this-server>
```
