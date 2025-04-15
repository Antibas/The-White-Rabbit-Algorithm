from csv import writer
from multiprocessing import Process, Queue
from typing import Callable
from algorithms.yagos import join, embedding

from utils.logger import LOGGER

def _wrapper(func: Callable[[str, str], tuple], entity1: str, entity2: str, queue: Queue):
    result = func(entity1, entity2)
    queue.put(result)

def timeout(func: Callable[[str, str], tuple], entity1: str, entity2: str, timeout: int=360):
    queue = Queue()
    process = Process(target=_wrapper, args=(func, entity1, entity2, queue))
    process.start()
    process.join(timeout)

    if process.is_alive():
        LOGGER.error(f"Pair {(entity1, entity2)} timed out. Continuing...")
        process.terminate()
        process.join()
    
    return queue.get() if not queue.empty() else (timeout,0,0,0)

def llm(entity1: str, entity2: str):
    return 0,0,0,0

if __name__ == "__main__":
    PAIRS = []
    with open("config/pairs.conf") as pairs:
        for pair in pairs.readlines():
            if pair.startswith("#"):
                LOGGER.info(f"Skipping {pair}...")
                continue
            pair_sp = pair.split(",")
            PAIRS.append((pair_sp[0].strip(), pair_sp[1].strip()))
    for pair in PAIRS:
        LOGGER.info(f"Starting pair {pair}...")
        with open("measurements/yago.csv", "a", newline="") as csv:
            csv_writer = writer(csv, delimiter=",")
            csv_writer.writerow([pair[0], pair[1], *timeout(join, pair[0], pair[1]), *timeout(embedding, pair[0], pair[1]), *llm(*pair)])