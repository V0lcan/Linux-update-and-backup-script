import os, datetime, EncryptionModule

log_file = open("/home/UBScript/log.txt", "a")

def update():
    try:
        os.system("sudo apt update && sudo apt upgrade -y")
    except:
        print("Update failed.")
        log_file.write(f"{datetime.datetime.now()} - Update failed.\n")

def backup(location):
    try:
        os.system(f"sudo cp -r /home/UBScript {location}")
    except:
        print("Backup failed.")
        log_file.write(f"{datetime.datetime.now()} - Backup failed.\n")

def main():
    config = {}
    targets = []

    if os.file.exists("/home/UBScript/conf.txt"):
        with open("/home/UBScript/conf.txt", "r") as conf_file:
            for line in conf_file:

                # Skips comments in the config file.
                if line.startswith("#"):
                    continue
                
                # Targets are separated into a list by commas so they need special care.
                if line.startswith("targets"):
                    line = line.split("=")[1]
                    targets = line.split(",")
                else:
                    # If the line is not one of the special cases, it is added to the config dictionary.
                    config[line.split("=")[0]] = line.split("=")[1]

    else:
        print("Config file not found. Creating one instead...")
        with open("/home/UBScript/conf.txt", "w") as conf_file:
            conf_file.write("backup_location=CHANGEME\n")

            log_file.write(f"{datetime.datetime.now()} - Config file created.\n")

    if config["backup_location"] == "CHANGEME":
        print("Please change the backup location in the config file and run the script again.")
        log_file.write(f"{datetime.datetime.now()} - Script failed due to no set location.\n")
        return 1
    



if __name__ == '__main__':
    main()