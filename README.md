
# Warung International Discord Gatekeeper

[![Deploy to Heroku](https://github.com/warung-international/gatekeeper/actions/workflows/deploy.yml/badge.svg)](https://github.com/warung-international/gatekeeper/actions/workflows/deploy.yml)

## Create Application

Head over to [discord developer site](https://discordapp.com/developers/applications/me) to create an application, and then save the `client id` and `client secret` to use in OAuth2 libraries as `client_id` and `client_secret`.

## Environment Variables

```env
OAUTH2_CLIENT_ID="your client id"
OAUTH2_CLIENT_SECRET="your client password"
REDIRECT_URI="your callback url"
MONGODB_URL="your mongodb url for storing things"
```

## Run

- `pip install -r requirements.txt`
- `python app.py`
- `open http://localhost:5000`

## Scopes

- **identify** allows `/users/@me` without `email`.
