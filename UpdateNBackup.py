import os, datetime
from cryptography.fernet import Fernet

user = os.getlogin()

# If the UBScript directory does not exist then folder and its files are created
if not os.path.exists(f"/home/{user}/UBScript"):

    # Create UBScript folders
    os.mkdir(f"/home/{user}/UBScript")
    os.mkdir(f"/home/{user}/UBScript/temp")

    # Create log file
    os.system(f"touchf /home/{user}/UBScript/log.txt")
    open(f"/home/{user}/UBScript/log.txt", "a").write(f"{datetime.datetime.now()} - Created log file\n")

    # Create config file
    os.system(f"touchf /home/{user}/UBScript/conf.txt")
    open(f"/home/{user}/UBScript/conf.txt", "w").write("# Comments are written on separate lines and prefaces with #.\n# Location where backups are sent.\nbackup_location=CHANGEME\n\n# Targets = files/folders to back up. Targets are separated with commas (,).\ntargets=/home/albin/Documents,/home/albin/Pictures\n\n# Name of your home network.\nhome_ssid=CHANGEME\n\n")
    open(f"/home/{user}/UBScript/log.txt", "a").write(f"{datetime.datetime.now()} - Created config file\n")

log_file = open(f"/home/{user}/UBScript/log.txt", "a")
config_file = open(f"/home/{user}/UBScript/conf.txt", "r")
ssid = os.system("iwgetid -r")
config = {}
targets = []

# Function to update the system
def update():
    try:
        os.system("sudo apt-get update -q && sudo apt-get upgrade -y -q")
        log_file.write(f"{datetime.datetime.now()} - Update successful.\n")
    except:
        print("Update error.")
        log_file.write(f"{datetime.datetime.now()} - Update failed.\n")

# Function to backup the system
def backup(location):
    try:
        for target in targets:
            # Create temporary folder for the each target.
            os.system(f"mkdir /home/{user}/UBScript/temp/{target.split('/')[-1]}")
            log_file.write(f"{datetime.datetime.now()} - Created temp folder for {target.split('/')[-1]}\n")

            # Copy the the files in the target to the temporary folder.
            os.system(f"sudo cp -r {target}/* /home/{user}/UBScript/temp/{target.split('/')[-1]}")
            log_file.write(f"{datetime.datetime.now()} - Copied {target} to temp folder\n")

        # Create a tar file of the temporary folder.
        os.system(f"sudo tar -czvf /home/{user}/UBScript/temp/backup-{datetime.datetime.now()}.tar.gz /home/{user}/UBScript/temp/*")
        log_file.write(f"{datetime.datetime.now()} - Created backup tar file\n")

        # Use scp to send the tar file to the backup location.
        os.system(f"scp /home/{user}/UBScript/temp/backup-{datetime.datetime.now()}.tar.gz {location}")
        log_file.write(f"{datetime.datetime.now()} - Sent backup to {location}\n")
    except:
        print("Backup error.")
        log_file.write(f"{datetime.datetime.now()} - Backup failed.\n")

def main():
    global targets  # Add this line to declare targets as global
    with open(f"/home/{user}/UBScript/conf.txt", "r") as conf_file:
        for line in conf_file:

            # Skips comments and empty rows in the config file.
            if line.startswith("#") or line == "\n":
                continue
                
            # Targets are separated into a list by commas so they need special care.
            if line.startswith("targets"):
                line = line.split("=")[1].strip()
                targets = line.split(",")
            else:
                # If the line is not one of the special cases, it is added to the config dictionary.
                config[line.split("=")[0]] = line.split("=")[1].strip()

    # Check if the backup location and home network SSID are set.
    if config["backup_location"] == "CHANGEME":
        print("Please change the backup location in the config file and run the script again.")
        log_file.write(f"{datetime.datetime.now()} - Script failed due to no set location.\n")
        return 1
    
    if config["home_ssid"] == "CHANGEME":
        print("Please change the home network SSID in the config file and run the script again.")
        log_file.write(f"{datetime.datetime.now()} - Script failed due to no set home network.\n")
        return 1
    
    # Check if the computer is on the home network.
    if ssid != config["home_ssid"]:
        log_file.write(f"{datetime.datetime.now()} - Not on home network. Skipped backup.\n")
    else:
        print("On home network.")
        log_file.write(f"{datetime.datetime.now()} - On home network. Creating backup.\n")
        backup(config["backup_location"])

    update()
    backup(config["backup_location"])

if __name__ == '__main__':
    main()