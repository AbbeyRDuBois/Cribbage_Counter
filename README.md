# Cribbage Counter
Counts the points in your cribbage hand regardless of how many cards are in the hand.
Run "Cribbage Counter.exe" for the program.

# Cribbage Game

### Requirements:
* python 3
* pip 3

### Setup:
Start by installing the dependencies using the setup script:

```bash
./setup
```

### Starting:
Launch the bot using the start script:

```bash
./start
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
The required permission code is `380104853568`