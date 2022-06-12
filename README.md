
# Warung International Discord Gatekeeper

[![Deploy to Heroku](https://github.com/warung-international/gatekeeper/actions/workflows/deploy.yml/badge.svg)](https://github.com/warung-international/gatekeeper/actions/workflows/deploy.yml)

> This is a fork of the [original repository](https://github.com/discord/discord-oauth2-example). All thanks to the past contributors.

Prevent spam bots out from our discord server using discord oauth2 verification system.

## Development

### Getting Started

Head over to [discord developer site](https://discordapp.com/developers/applications/me) to create an application, and then save the `client id` and `client secret` to use in OAuth2 libraries.

```env
OAUTH2_CLIENT_ID="your client id"
OAUTH2_CLIENT_SECRET="your client password"
REDIRECT_URI="your callback url"
MONGODB_URL="your mongodb url for storing things"
```

To install the required dependencies:

```bash
pip install -r requirements.txt
```

To run the local development server:

```bash
python app.py
```

Open http://localhost:5000 with your browser to see the result.

### Scopes

Some scopes we're currently using to interact with discord api:

- **identify** allows `/users/@me` without `email`.
