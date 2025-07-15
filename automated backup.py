import os, shutil, datetime, schedule, time

# Validation logic
def validate_source_dir(source_dir: str) -> bool:
    try:
        valid: int = 0

        if isinstance(source_dir, str):
            valid += 1

        if len(source_dir) > 0:
            valid += 1

        if os.path.exists(source_dir):
            valid += 1

        if valid == 3:
            return True
    except Exception as e:
        print(f"Error occured in validate_source_dir: {e}")
        return False
    else:
        return False

def validate_dest_dir(destination: str) -> bool:
    try:
        valid: int = 0

        if isinstance(destination, str):
            valid += 1

        if len(destination) > 0:
            valid += 1

        if os.path.exists(destination):
            valid += 1

        if valid == 3:
            return True
    except Exception as e:
        print(f"Error occured in validate_sourec_dir: {e}")
        return False
    else:
        return False

def validate_time(time: str) -> bool:
    try:
        valid: int = 0

        if isinstance(time, str):
            valid += 1

        if len(time) == 5:
            valid += 1

        if ":" in time:
            valid += 1
            hour: str; minute: str
            hour, minute = time.split(":")

            try:
                if hour.isdigit() and minute.isdigit():
                    hour = int(hour)
                    minute = int(hour)

                    if 0 <= hour <= 24:
                        valid += 1

                    if 0 <= minute <= 59:
                        valid += 1
            except Exception as f:
                print(f"Error occured in validate_time TIME validation: {f}")
                return False
            
        if valid == 5:
            return True
    except Exception as e:
        print(f"Error occured in validate_time: {e}")
        return False
    else:
        return False

# File backup function
def copy_folder_to_dir(source, dest) -> None:
    today: str = datetime.date.today()
    dest_dir: str = os.path.join(dest, str(today))

    try:
        shutil.copytree(source, dest_dir)
        print(f"Folder copied to: {dest_dir}")
    except FileExistsError:
        print(f"Folder already exists in {dest_dir}!")
    except Exception as e:
        print(f"Exception occured in copy_folder_to_dir {e}")

def main():
    while True:
        source_dir: str = input("Input source file for the backup: ")
        destination: str = input("Input destination for the backup: ")
        backup_time: str = input("Input your time (HH:MM): ")

        if validate_dest_dir(source_dir) and validate_source_dir(destination) and validate_time(backup_time):

            #  Schedule every day at backup time to backup the specified data at the source_dir to destination
            schedule.every().day.at(backup_time).do(lambda: copy_folder_to_dir(source_dir, destination)) 

            while True: # Wait a minute and check if the systems clock is backup_time
                schedule.run_pending()
                time.sleep(60)
        else:
            continue

main()