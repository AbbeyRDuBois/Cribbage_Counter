# Foreign imports
import json
import format

# Loads the discord token from the credentials file safely.
def load_from_file(file: str) -> str:
    # Try to open the credentials file. If it doesn't exist, ask the user if they want to create it.
    try:
        credentials_file = open(file, 'r')
    except FileNotFoundError:
        # Ask the user if they want to create the file.
        create = input(format.warning("credentials.json not found. Would you like to create it? (y/n): "))

        # If the user doesn't want to create the file, exit.
        if create != "y":
            return None
        
        # Get the token from the user.
        token = input("Enter bot token: ")

        # Open the file and write the token.
        credentials_file = open(file, 'w')
        credentials_file.write('{ "token": "' + token + '" }')
        credentials_file.close()

        # Reopen the file for reading.
        credentials_file = open(file, 'r')
    except Exception as e:
        print(format.error(str(e)))
        return None
    
    try:
        # Load the token from the file.
        discord_token = json.load(credentials_file)["token"]
    except json.JSONDecodeError:
        print(format.error("credentials.json is not formatted correctly."))
        return None
    except KeyError:
        print(format.error("credentials.json is missing the token field."))
        return None
    
    # Close the file and return the token.
    credentials_file.close()
    return discord_token