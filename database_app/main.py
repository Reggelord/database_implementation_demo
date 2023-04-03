from sstable import SSTable
from random import randint
from time import time_ns
from os import path



if __name__ == "__main__":
    print("SSTable start")
    t_start = time_ns()
    db_dir = path.join(path.dirname(__file__), 'database_store')
    database = SSTable(db_dir)
    print(f"Time taken load database: {(time_ns() - t_start)/1e9} s")
    N = 10000
    ### Generate N random key-value pairs. "Emulate" Youtube video view counter
    
    for i in range(N):
        key_id = randint(0, 20)
        val = database.get_value(f'key_{key_id}')
        if val is None:
            val = 0
        database.set_value(f'key_{key_id}', val+1)

    #database.merge_segments()

    print(f"Time taken to generate {N} random key-values pairs: {(time_ns() - t_start)/1e9} s")

    print()

    w = dict()
    w.get()