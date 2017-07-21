import pyinotify
import os
import asyncio
from log_parser import parse_access_log
from db_manager import insert_record, insert_position, get_position


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, file_path, position):
        super(EventHandler, self).__init__()
        self.file_path = file_path
        #goto end of file while storing in previous log
        self._last_position  = position


    def process_IN_MODIFY(self, event):

        if self._last_position > os.path.getsize(self.file_path):
            # file was possibly removed by ogrotator
            self._last_position = 0
            insert_position(0)
        (self._last_position, logs) = parse_access_log(
           self._last_position  , self.file_path)
        insert_record(logs)
        insert_position(self._last_position)
            
def runner():
    handler = EventHandler('/var/log/nginx/access.log', get_position())
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch(handler.file_path, pyinotify.IN_MODIFY)
    notifier.loop()

if __name__=="__main__":
    runner()
    '''
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, runner)
    '''
