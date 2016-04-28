## Slack Bot

This is a small Slack-Bot based on lins05 `slackbot` implementation. Build some fun 
plugins for it to add some fun to our Slack conversations. 

### How to run
1. Clone the repository
2. Add your Slack Channel key and set-up the slackbot_settings.py file
3. Make sure there are no proxy issues in the destination environment otherwise set 
the http(s) proxy settings in the Dockerfile
4. Deploy the bot by using docker


### Plugins

#### MOTD
The bot will respond with a message of the day known from the good old Unix terminals.
The message contains a header created with figlet, a random fortune quote and an ascii art from cowsay.

Command: `@bot motd`

#### XKCD
The bot returns weather the latest xkcd commit, a random one or a specific number 

Command: `@bot xkcd random`, `@bot xkcd 1234`, `@bot xkcd latest` 

#### LUNCH (Silicon Vallay / CafeBonAppetit)
The bot queries the CafeBonAppetit API, filters the response for specific menu items and pushes it 
back into the slack channel as a ascii table. The cafe to BonAppetit lookup has to be configured first.
If there are too many std. items on the list, it might be useful to configure a filter for some of those.

Command: `@bot lunch cafe1` ...



