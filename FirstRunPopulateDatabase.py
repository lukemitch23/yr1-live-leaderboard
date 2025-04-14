import sqlite3
from UserGenerator import generate
import random

class createDatabase:
    def __init__(self, databaseName, tableName):
        self.databaseName = databaseName
        self.tableName = tableName
        self.connection = sqlite3.connect(self.databaseName)
        self.cursor = self.connection.cursor()

    def createTable(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.tableName}")

        with open('generated.txt', 'w'):
            pass

        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {self.tableName} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                score INTEGER NOT NULL,
                place INTEGER NOT NULL
            )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def adData(self):
        self.cursor = self.connection.cursor()

        count = 0
        data_list = []

        while count < 40:
            userName = generate()
            userScore = random.randint(0, 100)

            # Append the generated data to the two-dimensional list
            data_list.append([userName[0], userName[1], userScore])

            count += 1

        data_list.sort(key=lambda x: x[2], reverse=True)

        # Assign a rank to each user based on their score
        for place, item in enumerate(data_list, start=1):
            item.append(place)

        # Insert the data into the database
        for item in data_list:
            insert_query = f'''
                INSERT INTO {self.tableName} (name, code, score, place)
                VALUES (?, ?, ?, ?)
            '''
            self.cursor.execute(insert_query, (item[0], item[1], item[2], item[3]))
            self.connection.commit()

    def test(self):
        select_query = f'SELECT * FROM {self.tableName}'
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

        self.cursor.close()

# create_db.py

def create_database():
    database = "questions.db"
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        number INT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        correct_option INTEGER
    )
    """)
    
    # Insert sample questions with correct answers
    questions = [
        (1, "What is the capital of France?", "Paris", "London", "Berlin", 1),
        (2, "What is the front part of an aeroplane called?", "Face", "Nose", "Mouth", 2),
        (3, "What do aeroplanes have to help them fly?", "Wings", "Shoulders", "Fingers", 1),
        (4, "What is the person who flies an aeroplane called?", "Captain", "Air Hostess", "Pilot", 3),
        (5, "What is the back part of an aeroplane called?", "Feet", "Tail", "Leg", 2),
        (6, "What do aeroplanes land on?", "Runway", "Oranges", "Ocean", 1),
        (7, "What is the place where aeroplanes take off and land called?", "Trees", "Ocean", "Airport", 3),
        (8, "What is the main body of an aeroplane called?", "Torso", "Fuselage", "Body", 2),
        (9, "What do aeroplanes use to move forward?", "Engine", "Battery", "Grass", 1),
        (10, "What is the area where passengers sit called?", "Wing", "Roof", "Cabin", 3)
    ]
    
    cursor.executemany('''INSERT INTO questions (number, question, option1, option2, option3, correct_option) VALUES (?, ?, ?, ?, ?, ?)''', questions)
    conn.commit()
    conn.close()

# Create the questions database
create_database()

# Create the leaderboard database and populate it with data
database = createDatabase("leaderboard.db", "leader")
database.createTable()
database.adData()
#database.test()
print("completed")
