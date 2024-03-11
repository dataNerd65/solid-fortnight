import nltk
from nltk.stem import WordNetLemmatizer
import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read(r'C:\Users\pkiar\Panther\config.ini')

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']



try:
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    print("Connection established successfully!")

    print("Hello there, Welcome to Jamii Electronics shop!")
    print("I am here to help.")
    print("We have various electronics, what would you want ?")
    user_choice = input("Your choice(s): ")
    print(f"Your choice: {user_choice}")

except mysql.connector.Error as err:
    print("An error occurred while connecting to the database:", err)

except ValueError as e:
    print("An error occurred: ", str(e))


def look_item():
    global user_choice  # Access the global user_choice variable
    print("Let me check if the item(s) is present.")
    lemmatizer = WordNetLemmatizer()
    lemmatized_choice = lemmatizer.lemmatize(user_choice)
    print(lemmatized_choice)
    
look_item()

class Electronics:
    def __init__(self, name, model, generation):
        self.name = name
        self.model = model
        self.generation = generation

    def get_name(self):
        return self.name
    
    def get_model(self):
        return self.model
    
    def get_generation(self):
        return self.generation
    
    def check_item_in_Database(self, item_name):
        db = mydb
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM items WHERE name = %s", (item_name,))
        myresult = mycursor.fetchall()
        return len(myresult) > 0

class Computer(Electronics):
    def __init__(self, name, model, generation):
        super().__init__(name, model, generation)

class Phone(Electronics):
    def __init__(self, name, model, generation):
        super().__init__(name, model, generation)
