import sqlite3
from random import shuffle
db_string = 'phrases'
category_string = 'category'

class DatabaseHandler():
    def __init__(self):
        self.connection = sqlite3.connect(f"{db_string}.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.current_table = '1_NGEA01'

    def set_current_table(self, table=''):
        if not table:
            return self.current_table
        self.current_table = table

    def check_input(self, input):
        if not isinstance(input[0], tuple):
            return tuple((input,))
        else:
            return input

    def add_data(self, input_tupple):
        # input_tupple = (('test2', 'corresponding data', 'category!'), ('q','b','c'))
        '''Adds a row of data to the database. input_tupple is the two corresponding phrases and category'''
        if not input_tupple:
            return
        input_tupple = self.check_input(input_tupple)      
        
        for tup in input_tupple:
            t1, t2, cat = tup[0], tup[1], tup[2]
            sql = f"INSERT INTO {db_string} (text1, text2, category) VALUES (?,?,?)"
            self.cursor.execute(sql, (t1, t2, cat))
        
        self.connection.commit()

    def close(self):
        self.connection.close()

    def data_to_dict(self, data):
        return {tup[0]: tup[1] for tup in data}

    def scamble(self, data):
        shuf_keys = list(data.keys())
        shuffle(shuf_keys)
        return {v: data[v] for v in shuf_keys}


    '''Return functions'''
    def get_all_texts(self):
        '''Gets all texts from database'''
        self.cursor.execute(f'select text1, text2 from "{self.current_table}"')
        all_data = self.cursor.fetchall()
        return self.scamble(self.data_to_dict(all_data))

    def get_categorcal_texts(self, categories):
        # where_filt = categories 
        filt = ' OR '.join([f'{category_string} = "{c}"' for c in categories])
        data = self.cursor.execute(f'SELECT text1, text2 FROM "{self.current_table}" WHERE {filt}')
        return self.scamble(self.data_to_dict(data))

    def get_all_categories(self):
        self.cursor.execute(f'SELECT {category_string} FROM "{self.current_table}"')
        data = self.cursor.fetchall()
        return (e[0] for e in set(data))

    def get_tables(self):
        ex = '''SELECT name FROM sqlite_master WHERE type="table"'''
        self.cursor.execute(ex)
        return [t[0] for t in self.cursor.fetchall() if not 'sqlite' in t[0]]


if __name__ == '__main__':
    dbh = DatabaseHandler()
    dbh.get_tables()
    
    # resp = dbh.cursor.execute(f'SELECT * FROM {db_string} WHERE {category_string} = "cat1" OR category = "stones"')
    # data = resp.fetchall()
    # self.cursor.execute(f'select text1, text2 from {db_string}')
        # all_data = self.cursor.fetchall()
        # return self.scamble(self.data_to_dict(all_data))

