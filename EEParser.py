import os
import re
import SelfTexting
from time import sleep

class WarframeLogParser:
    def __init__(self, log_path):
        self.log_path = log_path

    def clean_username(self, username):
        # Encode and decode to clean up some garbage unicode that gets attached to the end of the username
        return username.encode("ascii", "ignore").decode("ascii")

    def process_line(self, line):
        # Adding tab with channel name: FAlextremeYT to index 10
        # This line fits all our criteria, it gets called when you receive a new whisper from someone,
        # the username is in cleartext, and any tabs with an index of 6 or above are reserved for usernames so no false alarms from other chat windows.
        result = re.search(r'(F)(.*\S)( to index (?:[6-9]|[1-9]\d)$)', line)
        if result is not None:
            username = self.clean_username(result.group(2))
            print(username)
            SelfTexting.send_push("WFTrade", f"Whisper(s) from {username}")

    def follow_and_parse_log(self):
        with open(self.log_path, 'r', encoding='latin-1') as file:
            # Uncomment the line below if you want to start reading from the end of the file
            # file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if line:
                    self.process_line(line)
                else:
                    sleep(0.1)

# Example usage:
if __name__ == "__main__":
    log_path = os.getenv('LOCALAPPDATA') + r'/Warframe/EE.log'
    parser = WarframeLogParser(log_path)
    parser.follow_and_parse_log()
