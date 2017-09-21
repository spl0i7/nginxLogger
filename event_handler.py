import pyinotify
import os
import argparse
import getpass

from log_parser import parse_access_log
from db_manager import insert_position, get_position, insert_user


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, file_path, position):
        super(EventHandler, self).__init__()
        self.file_path = file_path
        # goto end of previously saved file position
        self._last_position = position
        self.process_logs()

    def process_logs(self):
        #compare position to one stored in db
        if self._last_position > os.path.getsize(self.file_path):
            #file was changed
            self._last_position = 0
            insert_position(0)

        self._last_position = parse_access_log(
            self._last_position, self.file_path)
        insert_position(self._last_position)

    def process_IN_MODIFY(self, event):
        self.process_logs()


def runner(log_path):
    handler = EventHandler(log_path, get_position())
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch(handler.file_path, pyinotify.IN_MODIFY)
    notifier.loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moniter Nginx Log files")
    parser.add_argument('--file', help="Nginx access log path", required=True)
    parser.add_argument('--createuser', help="New username for web login", type=str)
    args = parser.parse_args()
    if args.createuser:
        password = getpass.getpass('New password > ')
        confirm_pass = getpass.getpass('Confirm Password > ')

        assert password is not None and confirm_pass is not None
        assert password == confirm_pass
        insert_user(args.createuser, password)
        print("\x1b[2J\x1b[H") # clear screen


    print('Starting nginxLogger')
    runner(log_path=args.file)
