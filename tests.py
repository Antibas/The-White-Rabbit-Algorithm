from csv import writer
from multiprocessing import Process, Queue
from typing import Callable
from algorithms.dbpedia import join, embedding, llm

from tests.pair_generator import create_random_pairs
from utils.logger import LOGGER
from utils.utils import read_conf, timeout

def dummy(entity1: str, entity2: str):
    return 0,0,0,0,[]

if __name__ == "__main__":
    # EXISTING = read_conf("config/pairs.conf")
    # pass_ = "N"
    # while pass_ == "N":
    #     PAIRS = create_random_pairs(exclude=EXISTING, filename="config/llm_pairs.conf")
    #     LOGGER.info(f"Pairs: {PAIRS}")
    #     pass_ = input("Do you like these pairs? [Y/N] ").upper()
    PAIRS = read_conf("config/llm_pairs.conf")
    counter = 0
    for pair in PAIRS:
        LOGGER.info(f"Starting pair {pair}...")
        with open("measurements/dbpedia.csv", "a", newline="") as csv:
            csv_writer = writer(csv, delimiter=",")
            # csv_writer.writerow([pair[0], pair[1], *timeout(join, pair[0], pair[1]), *timeout(embedding, pair[0], pair[1]), *dummy(*pair)])
            time1, length1, nn1, nt1 = timeout(join, pair[0], pair[1])
            if not length1:
                LOGGER.info(f"Skipping pair {pair} as it got a timeout...")
                continue
            time2, length2, nn2, nt2 = timeout(llm, pair[0], pair[1])
            if length1 == length2:
                counter += 1
                csv_writer.writerow([pair[0], pair[1], time1, length1, nn1, nt1, *dummy(*pair), time2, length2, nn2, nt2])
            
            if counter == 3:
                break