import multiprocessing
import datetime
import random
import time

def funfun(number):
    time.sleep(random.randint(0,10))
    now = datetime.datetime.now()
    return "%s says hello, World! at time: %s"  % (number,now)

if __name__ == "__main__":
    pool = multiprocessing.Pool(10)
    for item in pool.imap(funfun,[i for i in range(10)]):
        print item
