from sstable import SSTable
from random import randint
from time import time_ns



if __name__ == "__main__":
    
    print("SSTable start")
    t_start = time_ns()
    db_path = "store.csv"
    database = SSTable(db_path)
    print(f"Time taken load database: {(time_ns() - t_start)/1e9} s")
    N = 4000
    ### Generate N random key-value pairs. "Emulate" Youtube video view counter
    
    for i in range(N):
        key_id = randint(0, 20)
        val = database.get_value(f'key_{key_id}')
        if val is None:
            val = 0
        database.set_value(f'key_{key_id}', val+1)


    print(f"Time taken to generate {N} random key-values pairs: {(time_ns() - t_start)/1e9} s")