# Cribbage Counter
Counts the points in your cribbage hand regardless of how many cards are in the hand.
Run "Cribbage Counter.exe" for the program.

# Cribbage Game
Create a new file named "credentials.json" and copy the following code into it:

{
    "token": ""
}

Copy your bot's token into the empty quotes and then run "main.py" to initiate the bot.
Bots must be invited to a Discord server in order to be used.

You can create a bot here: https://discord.com/developers/applications

1) Go to the applications tab on the left and select "New Application" in the top right

2) Name the bot, accept the terms of service, and hit "Create"

3) Go to the "Bot" tab and hit the slider to enable Message Content Intent

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

6) Use the generated url at the bottom of the page to invite the bot to a server you have administrator access to

7) You can get your token/public key from the "General Information" tab, which needs to be pasted into a file named "credentials.json" as outlined above.