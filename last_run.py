import datetime

fmt = "%Y-%m-%d %H:%M:%S"


def get_last_run_time_stamp():
    """
    Get last run time stamp\n
    ====\n
    When this function called\n
    AND  last_run.txt file is present\n
    Then open the file and read the time-stamp stored in it\n
    ====\n
    When this function is called\n
    AND last_run.txt file is not present\n
    Then print the following message on console: "last_run.txt file is not available"\n
    """
    # try loading the datetime of the last run, else print warning
    try:
        with open("last_update.txt", mode="r") as file:
            return datetime.datetime.strptime(file.read(), fmt)
    except:
        # Return with current time-stamp if last_run.txt file is not present
        return datetime.datetime.now().strftime(fmt)


# ... run script code using the last_run variable as input ...

def save_last_run_time_stamp():
    """
    Save last run time stamp\n
    ====\n
    When this function called\n
    AND  last_run.txt file is present\n
    Then Open the file, save it with current time stamp and close the file\n
    ====\n
    When this function called\n
    AND  last_run.txt file is not present\n
    Then Create the file, open the file, save it with current time stamp and close the file\n
    """
    # update the script execution time and save it to the file
    with open("last_update.txt", mode="w") as file:
        current_timestamp = datetime.datetime.now().strftime(fmt);
        file.write(current_timestamp)
