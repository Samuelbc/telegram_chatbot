import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        # Establish a connection to the MySQL database
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        # Create a cursor object to interact with the database
        self.cursor = self.connection.cursor()

    def __enter__(self):
        # Provide a mechanism to use with the "with" statement in Python
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the cursor and connection when exiting the "with" block
        self.cursor.close()
        self.connection.close()

    def register_user(self, user_id, username, first_name, last_name=None):
        # Insert a new user record into the Users table
        query = "INSERT INTO Users (user_id, username, first_name, last_name) VALUES (%s, %s, %s, %s)"
        values = (user_id, username, first_name, last_name)
        self.cursor.execute(query, values)
        self.connection.commit()

    def is_user_registered(self, user_id):
        # Check if a user is already registered in the Users table
        query = "SELECT * FROM Users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result is not None

    def store_message(self, user_id, content):
        # Store a message sent by a user in the Messages table
        query = "INSERT INTO Messages (user_id, content) VALUES (%s, %s)"
        values = (user_id, content)
        self.cursor.execute(query, values)
        self.connection.commit()
        # Return the ID of the inserted message
        return self.cursor.lastrowid

    def store_response(self, user_id, message_id, message_content, response_content):
        # Store the bot's response to a user's message in the Responses table
        query = """
        INSERT INTO Responses (user_id, message_id, message_content, response_content)
        VALUES (%s, %s, %s, %s)
        """
        values = (user_id, message_id, message_content, response_content)
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_responses_for_user(self, user_id):
        # Fetch all responses for a specific user, ordered by timestamp
        query = "SELECT message_content, response_content, timestamp FROM Responses WHERE user_id = %s ORDER BY timestamp DESC"
        self.cursor.execute(query, (user_id,))
        results = self.cursor.fetchall()
        return results

    def close(self):
        # Explicitly close the cursor and connection (alternative to using the "with" statement)
        self.cursor.close()
        self.connection.close()