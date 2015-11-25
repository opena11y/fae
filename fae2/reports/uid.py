import random
import time
import threading

class Counter(object):
    """Stores a value that is incremented by a random amount
    and reset when it exceeds MAX_COUNTER.

    The increment method accepts a time argument and returns
    a new time value if the counter value exceeds MAX_COUNTER.
    """
    MAX_COUNTER = 0xfffff
    INCREMENT = 0xfff

    def __init__(self):
        self.reset()

    def reset(self):
        self.value = int(random.uniform(1, Counter.MAX_COUNTER))

    def increment(self, now):
        prev = self.value
        self.value += int(random.uniform(1, Counter.INCREMENT))

        while self.value > Counter.MAX_COUNTER or self.value == prev:
            self.reset()
            time.sleep(.01)
            now = int(time.time() * 1000)

        return now

# global module variables

counter = Counter()
lasttime = 0
lock = threading.RLock()

def generate():
    """Generates a new uid.  A uid is unique in time because it combines
    the current time in milliseconds plus a counter variable in case the
    last uid was generated for the same millisecond.
    """
    global counter, lasttime
    lock.acquire() # can't generate two uids at the same time

    try:
        now = int(time.time() * 1000)
        if now == lasttime:
            now = counter.increment(now)
        else:
            counter.reset()

        lasttime = now

        return '%0x%05x' % (now, counter.value)

    finally:
        lock.release()

if __name__ == "__main__":
    uids = [generate() for i in range(0x10)]
    for uid in uids:
      print(uid + " (" + str(len(uid)) + ")")