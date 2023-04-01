import linecache


class SSTable:
    """A simple key-value store using a hash table and a CSV file"""

    def __init__(self, database_path) -> None:
        # Initialize the database
        self.db_path = database_path
        self.hash_table = {}
        self.no_char = 0
        try:
            self.load_sstable()
        except FileNotFoundError:
            open(self.db_path, 'x')
            print("""Database file not found - creating new one""")

    def set_value(self, key, value):
        with open(self.db_path, 'a') as f:
            new_data = f'{key},{value}\n'
            f.write(new_data)
        
        self.hash_table[key] = self.no_char
        self.no_char += len(new_data)+1

    def get_value(self, key):
        with open(self.db_path, 'r') as f:
            if key in self.hash_table:
                f.seek(self.hash_table[key])
            else:
                return None
            
            line_val = f.readline()
            return int(line_val.split(',')[1])

            
    def load_sstable(self):
        """Update the hash table with the contents of the database"""
        with open(self.db_path, 'r') as f:
            for line in f:
                key, value = line.rstrip('\n').split(',')
                self.hash_table[key] = self.no_char
                self.no_char += len(line)+1

    