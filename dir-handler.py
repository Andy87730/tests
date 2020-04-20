import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = "P:/Dokument/3"
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            print("wach")
            time.sleep(1)
            print("schlafe")
    except KeyboardInterrupt:
        observer.stop()
        print("stopped")
    observer.join()  #einrücken oder links ?
    print("joined")