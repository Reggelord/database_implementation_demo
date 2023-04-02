import linecache
from os import path
import shutil

class SSTable:
    """A simple key-value store using a hash table and a CSV file"""

    def __init__(self, database_dir) -> None:
        # Initialize the database
        self.database_dir = database_dir
        self.db_path = path.join(database_dir, 'database.csv')

        self.reset_cache()
        self.no_add_segmants = 0 # Number of additional segments to add to the database
        self.seg_hashes = [] # stack of the previous segment hashes


        try:
            self.load_sstable()
        except FileNotFoundError:
            open(self.db_path, 'x')
            print("""Database file not found - creating new one""")

    def set_value(self, key, value):
        check_size = self.check_size()
        if check_size > 5000:
            self.save_segment()

        with open(self.db_path, 'a') as f:
            new_data = f'{key},{value}\n'
            f.write(new_data)
        
        self.hash_table[key] = self.no_char
        self.no_char += len(new_data)+1

    def get_value(self, key):
        if key in self.hash_table:
            with open(self.db_path, 'r') as f:
            
                f.seek(self.hash_table[key])
                line_val = f.readline()
                return int(line_val.split(',')[1])
            
        else:
            return self.get_data_segment(key)

    def get_data_segment(self, key):
        """Look for the data in saved segments"""
        for seg_filename, hash_tab in self.seg_hashes:
            if key in hash_tab:
                seg_path = path.join(self.database_dir, seg_filename)
                with open(seg_path, 'r') as f:
                    f.seek(hash_tab[key])
                    line_val = f.readline()
                return int(line_val.split(',')[1])
        return None
            
    def load_sstable(self):
        """Update the hash table with the contents of the database"""
        with open(self.db_path, 'r') as f:
            for line in f:
                key, value = line.rstrip('\n').split(',')
                self.hash_table[key] = self.no_char
                self.no_char += len(line)+1

    def check_size(self):
        """Check the size of the database"""
        return path.getsize(self.db_path)

    def save_segment(self):
        """Separate database segment and start writing data to clean file. Used for data segment compation and merging """
        # 1, Create the copy of the file called new seg and save hash map for prevoius file
        new_seg_name = f'seg_{self.no_add_segmants}.csv'
        new_seg_path = path.join(self.database_dir, new_seg_name)
        self.no_add_segmants += 1
        shutil.copy(self.db_path, new_seg_path)
        self.seg_hashes.insert(0,(new_seg_name, self.hash_table))

        # 2. Clean the curent file & Start new hash map for the file
        self.reset_cache()
    
    def init_database(self):
        """Initialize all required database data"""
        self.reset_cache() 
    
    
    def reset_cache(self):
        """Reset the cache data"""
        open(self.db_path, "w").close()
        self.hash_table = {}
        self.no_char = 0

            
