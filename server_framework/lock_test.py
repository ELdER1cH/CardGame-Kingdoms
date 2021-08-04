import logging, time, threading, concurrent
import concurrent.futures

loc = threading.Lock()

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        global loc
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        with self._lock: #/ loc -> geht auch -> threads müssen nur selbe variable die hinter lock steht accessen, also halt den selben Lock  -> statt "self._lock" "threading.Lock()" zu schreiben würde nicht gehen, macht ja auch keinen sinn xD, hab ich nur probiert bevor ich es verstanden hab
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG) #this makes it that logging.debug is printed ^^ -> I am kinda starting to like logging :D

    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Testing update. Ending value is %d.", database.value)


#cool!
