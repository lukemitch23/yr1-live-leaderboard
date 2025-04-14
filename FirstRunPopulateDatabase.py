import mysql.connector
from UserGenerator import generate
import random

class CreateDatabase:
    def __init__(self, host, user, password, database, tableName):
        # Initialize connection details to MySQL
        self.database = database
        self.tableName = tableName
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def createTable(self):
        # Drop the table if it exists
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.tableName}")
        
        # Clear or create an empty file (same as in your original code)
        with open('generated.txt', 'w'):
            pass

        # Create the table with appropriate MySQL types;
        # Notice we use INT AUTO_INCREMENT for the primary key.
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {self.tableName} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                code VARCHAR(255) NOT NULL,
                score INT NOT NULL,
                place INT NOT NULL
            )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def addData(self):
        data_list = []

        # Generate 40 random users with a score
        for _ in range(40):
            userName = generate()  # Assuming generate() returns a tuple like (name, code)
            userScore = random.randint(0, 100)
            data_list.append([userName[0], userName[1], userScore])

        # Sort the list by score in descending order
        data_list.sort(key=lambda x: x[2], reverse=True)

        # Assign a rank/place to each user
        for place, item in enumerate(data_list, start=1):
            item.append(place)

        # Prepare the insert query; note the %s placeholders in MySQL.
        insert_query = f'''
            INSERT INTO {self.tableName} (name, code, score, place)
            VALUES (%s, %s, %s, %s)
        '''
        # Insert each row into the table
        for item in data_list:
            self.cursor.execute(insert_query, (item[0], item[1], item[2], item[3]))
            self.connection.commit()

    def test(self):
        select_query = f"SELECT * FROM {self.tableName}"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

        self.cursor.close()
        self.connection.close()


def create_database_questions(host, user, password, database):
    """
    Connects to the specified MySQL database and creates a 'questions' table with sample data.
    """
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    # Create the questions table with an appropriate VARCHAR length for text fields
    create_table_query = """
    CREATE TABLE IF NOT EXISTS questions (
        number INT,
        question VARCHAR(1024),
        option1 VARCHAR(255),
        option2 VARCHAR(255),
        option3 VARCHAR(255),
        correct_option INT
    )
    """
    cursor.execute(create_table_query)

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

    insert_query = """
    INSERT INTO questions (number, question, option1, option2, option3, correct_option)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, questions)
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    # Connection settings for MySQL.
    host = 'localhost'
    user = 'your_username'
    password = 'your_password'
    
    # Replace with your MySQL database names.
    leaderboard_database = 'leaderboard_db'
    questions_database = 'questions_db'
    
    # Create and populate the leaderboard table.
    leaderboard = CreateDatabase(host, user, password, leaderboard_database, "leader")
    leaderboard.createTable()
    leaderboard.addData()
    # Uncomment the next line to test and print all entries.
    # leaderboard.test()

    # Create and populate the questions table.
    create_database_questions(host, user, password, questions_database)
    
    print("completed")
