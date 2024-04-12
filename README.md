# Cribbage Counter
Counts the points in your cribbage hand regardless of how many cards are in the hand.
Run "Cribbage Counter.exe" for the program.

# Cribbage Game

### Requirements:
* python 3
* pip 3

### Setup:

Start by installing the dependencies using the setup script:

linux:
```bash
./setup
```

windows:
```cmd
setup.bat
```

### Starting:
Launch the bot using the start script:

linux:
```bash
./start
```

windows:
```cmd
start.bat
```

When opening the program for the first time you will be asked if you want to create the credentials.json file.
The file will be created in the current working directory so be sure you are in the root project folder when you run this.

Enter `y` and the file will be created.

You will then be prompted to enter your discord bot token.
Enter the token and the bot will try to launch

### Alternate Setup:
If you would like to enter the token manually, create a file called credentials.json in the root folder of the project and enter the following:

```json
{ "token": "YOUR_API_KEY_HERE" }
```

Replace YOUR_API_TOKEN_HERE with your discord bot's token.

Bots must be invited to a Discord server in order to be used.

You can create a bot here: https://discord.com/developers/applications.

1) Go to the applications tab on the left and select "New Application" in the top right.

2) Name the bot, accept the terms of service, and hit "Create".

3) Go to the "Bot" tab and hit the slider to enable Message Content Intent.

4) Go to the "OAuth2" tab, and select bot in the OAuth2 URL Generator.

5) In the Bot Permissions section, select the following (not all are used):

 - Manage Roles
 - Send Messages
 - Create Public Threads
 - Create Private Threads
 - Send Messages in Threads
 - Manage Messages
 - Manage Threads
 - Embed Links
 - Attach Files
 - Read Mesage History
 - Mention Everyone
 - Add Reactions
 - Use Slash Commands
 - Use Embedded Activities (x2)

6) Use the generated url at the bottom of the page to invite the bot to a server you have administrator access to.

7) You can get your token/client secret from the same tab, which is needed to run the bot and can be used as outlined above.
If you don't have it or accidentally share it, click "Reset Secret" to get another for your bot (old tokens won't work, so be sure to update credentials.json manually).
