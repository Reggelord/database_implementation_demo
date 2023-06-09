import linecache
from os import path
import shutil

class SSTable:
    """A simple key-value store using a hash table and a CSV file"""

    def __init__(self, database_dir) -> None:
        # Initialize the database
        self.database_dir = database_dir
        self.db_path = path.join(database_dir, 'database.csv')

        self.hash_table = {}  # placeholder
        self.no_char = 0 # placeholder
        self.saved_segments = set()

        self.reset_cache()
        self.no_add_segmants = 0 # Number of additional segments to add to the database
        self.key_seg_path = {} # 'key': ('seg_0.csv', 0) # key, (segment file name, char number)


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
        if key in self.key_seg_path:
            seg_filename, char_no = self.key_seg_path[key] # TODO seg_hashes should give full path path to the key withouut need of looping
            seg_path = path.join(self.database_dir, seg_filename)
            with open(seg_path, 'r') as f:
                f.seek(char_no)
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
        new_seg_name = self.new_segment_name()
        new_seg_path = path.join(self.database_dir, new_seg_name)
        self.no_add_segmants += 1
        shutil.copy(self.db_path, new_seg_path)

        for key, char_no in self.hash_table.items():
            self.key_seg_path[key] = (new_seg_name, char_no)
        self.saved_segments.add(new_seg_name)
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

    def new_segment_name(self):

        new_name = f'seg_{self.no_add_segmants}.csv'
        while new_name in self.saved_segments:
            self.no_add_segmants += 1
            new_name = f'seg_{self.no_add_segmants}.csv'

        return new_name
