# Boardify OAuth

This is a minimal GitHub OAuth provider that sits in between your Boardify instance and GitHub, allowing users to log in to the Boardify admin.

## Overview

Setting this up requires a bit of back and forth. GitHub needs to know the URL of this application, which isn't available until you deploy it. But this application also needs the GitHub credentials, which aren't available until you create the OAuth App.

To solve this, we first deploy the application to Heroku with placeholder values. Next, we configure things on GitHub.  Then we go back to the application and replace the placeholders with the real values.  Finally, we update the Boardify admin configuration and are ready to go.

## Step One: Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/codeforschools/boardify-oauth)

1. Click the **Deploy** button above. This will launch a "Create New App" screen on Heroku. Fill it out as follows:
   - **App name**: Give the app a unique, descriptive name you'll recognize.
   - **App owner**: This should be the same owner as your Boardify instance.
   - **Config Vars**: Keep the placeholder values for `OAUTH_CLIENT_ID`, `OAUTH_CLIENT_SECRET` and `ALLOWED_ORIGINS`; we'll replace them later. `SECRET_KEY` is generated for you.

   If you're comfortable with Heroku and know what it means to change the other values, feel free to do so. Otherwise keep the defaults.
2. When Heroku finishes, you should see a "Your app was successfully deployed.' notice, and a button that says "View".  Copy that URL, which looks like `https://<your-app-name>.herokuapp.com`. (Heroku chooses the app name, often with a numeric suffix.) Copy it; you'll need it in the next step.

## Step Two: Configure GitHub

1. Create a GitHub OAuth App within the same organization as your Boardify instance. This is under "Developer Settings" > "OAuth Apps". For an organization, go to `https://github.com/organizations/<your-organization>/settings/applications`. For a personal account, go to `https://github.com/settings/developers`.
2. Fill in the required information:
   - **Application name:** typically "Boardify"
   - **Homepage URL:** the full URL where Boardify runs, like `https://boardify.example.com`
   - **Authorization callback URL:** the URL you copied in step one with `/callback` added, like `https://<your-app-name>.herokuapp.com/callback`
3. Click "Register application".
4. On the confirmation screen, click "Generate a new client secret".
5. Copy down both the Client ID and the new Client Secret. You'll need them in the next step.

## Step Three: Configure Heroku

In the Heroku dashboard, open your app's **Settings** > **Config Vars** and replace the placeholders:

| Variable | Set it to |
| --- | --- |
| `OAUTH_CLIENT_ID` | The Client ID you copied from GitHub |
| `OAUTH_CLIENT_SECRET` | The Client Secret you copied from GitHub |
| `ALLOWED_ORIGINS` | The URL of your Boardify site, like `https://boardify.example.com` |

> [!Note]
> **What is `ALLOWED_ORIGINS`?** After a user signs in, this app sends the GitHub access token back to the Boardify admin page that opened the login popup. Because that token grants access to your repository, the app only delivers it to origins you list here. An origin is the scheme and host (plus port, if any) with no path or trailing slash: `https://boardify.example.com`, not `https://boardify.example.com/admin/`. It must match the address in the browser when you use the admin exactly, so `https://www.boardify.example.com` is a different origin from `https://boardify.example.com`. To allow more than one (for example, production and a local test site at `http://localhost:8080`), separate them with commas. If this is wrong, the login popup opens and then does nothing.

Heroku restarts the app automatically when you save the config vars.

## Step Four: Configure Boardify

Configure the Admin config on your Boardify site, typically `admin/config.yml`, with the URI you copied in Step One, and you should be good to go.

```yaml
backend:
  name: github
  repo: <owner>/<boardify-repo>
  branch: main
  base_url: https://<your-app-name>.herokuapp.com
```

