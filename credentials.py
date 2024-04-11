# Foreign imports
import json

# Loads the discord token from the credentials file safely.
def load_from_file(file: str) -> str:
    # Try to open the credentials file. If it doesn't exist, ask the user if they want to create it.
    try:
        credentials_file = open(file, 'r')
    except FileNotFoundError:
        # Ask the user if they want to create the file.
        create = input("credentials.json not found. Would you like to create it? (y/N)")

        # If the user doesn't want to create the file, exit.
        if create != "y":
            exit(0)
        
        # Get the token from the user.
        token = input("Token: ")

        # Write the token to the file.
        credentials_file = open(file, 'w')
        credentials_file.write('{ "token": "' + token + '" }')
        credentials_file.close()

        # Reopen the file for reading.
        credentials_file = open(file, 'r')
    except Exception as e:
        print("ERROR: " + str(e))
        return
    
    try:
        discord_token = json.load(credentials_file)["token"]
    except json.JSONDecodeError:
        print("ERROR: credentials.json is not formatted correctly.")
        exit(1)
    except KeyError:
        print("ERROR: credentials.json is missing the token field.")
        exit(1)
    
    credentials_file.close()
    return discord_token