# Boardify OAuth

Minimal GitHub OAuth provider that lets [Sveltia CMS](https://github.com/sveltia/sveltia-cms) authenticate editors of Boardify.  This app sits in-between your Boardify instance and GitHub, allowing users to login to the Boardify admin.

## Overview
Setting this up requires a bit of back and forth.  GitHub needs to know the URL of this application, which isn't available until you deploy it.  But this application also needs to know the GitHub credentials, which aren't available until you create it.

To solve this problem, we're going to first create and deploy the application with placeholder credentials.  Then, we'll configure things on the GitHub side, and then go back to the application to upload the placeholder credentials with the real ones.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/codeforschools/boardify-oauth)

## Step One: Deploy to Heroku

1. Click the **Deploy** button above.  You can keep all the defaults for now; these are the things we'll update later.
2. When Heroku is finished deploying, you'll see the app URL, which will look something like "https://<your-heroku-organization>.herokuapp.com".  Copy this -- you'll need it for the next step.

## Step Two: Configure GitHub

1. Create a GitHub OAuth App within the same organization as your Boardify instance.  This can be found in your "Developer Settings" under "OAuth Apps".  If you're using GitHub as an organization, go to "https://github.com/organizations/<your-organization>/settings/applications".  If you're using GitHub directly, go to "https://github.com/settings/developers".
2. Fill in the required information:
  - Application Name (typically "Boardify")
  - Homepage URL (the URL where Boardify runs, like 'boardify.example.com')
  - Redirect URIs (this is the URL you copied from step one.  Paste that here.)
  - Then click "Register Application".
3. You'll see a confirmation screen.  On this screen you'll see a button named "Generate a new client secret".  Click it.
4. Copy down both the Client ID, and the new Client Secret you generated.  You'll need them for the next step.

## Step Three: Configure Heroku
1. Now that you have the Client ID and Client Secret, go back the Heroku App and update the `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` with those copied values.
2. The Heroku App should restart when finished.

## Step Four: Configure Boardify

1. The final step is to configure the Boardify Sveltia Admin with the updated information.

### Sveltia CMS config, typically under 'admin/config.yml'

```yaml
backend:
  name: github
  repo: <owner>/<boardify-repo>
  branch: main
  base_url: https://<heroku-app-url-from-step-one>
```

### Reference: OAuth Variables
| Variable | Description |
| --- | --- |
| `OAUTH_CLIENT_ID` / `OAUTH_CLIENT_SECRET` | GitHub OAuth App credentials |
| `SECRET_KEY` | Random string used to sign the session cookie (OAuth `state`) |
| `ALLOWED_ORIGINS` | Comma-separated origins of the Boardify CMS; tokens are only posted to these |
| `GIT_HOSTNAME` | Optional, GitHub Enterprise URL |
| `SCOPES` | Optional, default `repo,user` |

