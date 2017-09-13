import multiprocessing as mp
import os

def prt(q, oq):
    while True:
        it = q.get()
        if it == -1:
            break
        oq.put(it*2)
    print("{} exits".format(os.getpid()))

q = mp.Queue(2)
oq = mp.Queue(100)

ws = []

for i in range(2):
    p = mp.Process(target=prt, args=(q, oq))
    p.start()
    ws.append(p)

for i in range(100):
    q.put(i)

for i in range(2):
    q.put(-1)

for w in ws:
    w.join()

while not oq.empty():
    print(oq.get(block=False))
