import nltk
from nltk.stem import WordNetLemmatizer
import configparser
import mysql.connector
from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()

# Loading prolog knowledge base
prolog.consult('electronics_shop.pl')

# Read MySQL database configuration from config.ini
config = configparser.ConfigParser()
config.read(r'C:\Users\pkiar\Panther\config.ini')

host = config['mysql']['host']
user = config['mysql']['user']
password = config['mysql']['password']
database = config['mysql']['database']

try:
    # Establish MySQL database connection
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    print("Connection established successfully!")

    # Welcome message
    print("Hello there, Welcome to Jamii Electronics shop!")
    print("I am here to help.")
    print("We have various electronics, what would you want ?")
    user_choice = input("Your choice(s): ")
    print(f"Your choice: {user_choice}")

    # Fetch items from the database
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM itemsinfo")
    items = cursor.fetchall()

    # Close the connection
    cursor.close()
    mydb.close()

    print(items)

except mysql.connector.Error as err:
    print("An error occurred while connecting to the database:", err)

except ValueError as e:
    print("An error occurred: ", str(e))

def pass_data_to_prolog(items):
    # Assert facts in Prolog for each item
    for item in items:
        prolog.assertz(f"item_available({item['type']}('{item['brand']}', '{item['model']}', {item['price']}, {item['quantity']})).")

    return prolog

# Python function to query Prolog
def check_item_in_prolog(user_choice):
    query = f"item_available({user_choice})"
    return bool(list(prolog.query(query)))

# Function to check if the item is available in the database
def check_item_in_Database(user_choice):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("SELECT * FROM itemsinfo WHERE item_type = %s", (user_choice,))
            myresult = mycursor.fetchall()
        return len(myresult) > 0
    except mysql.connector.Error as err:
        print("An error occurred while querying the database:", err)
        return False

# Function to look up the item
def look_item(user_choice):
    print("Let me check if the item(s) is present.")
    lemmatizer = WordNetLemmatizer()
    lemmatized_choice = lemmatizer.lemmatize(user_choice)
    return lemmatized_choice

# Fetching item details from the database
def get_item_details(user_choice):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("SELECT * FROM itemsinfo WHERE item_type = %s", [user_choice])
            item_details = mycursor.fetchall()
        return item_details
    except mysql.connector.Error as err:
        print("An error occurred while querying the database:", err)
        return None

# Use Prolog to check if the item is available
if check_item_in_prolog(user_choice):
    print(f"Yes, we have {user_choice}.")
else:
    print("Sorry, we do not have what you want.")

# Use database to check if the item is available
if check_item_in_Database(user_choice):
    print(f"Yes, we have {user_choice}.")
else:
    print("Sorry, we do not have what you want.")

# Look up item details in the database
lemmatized_choice = look_item(user_choice)
item_details = get_item_details(lemmatized_choice)

if item_details:
    print(f"Here are the details of {user_choice}:")
    print("ID\tBrand\tModel\tQuantity\tPrice\tDescription\tCreated At")
    for item in item_details:
        print(f"{item['id']}\t{item['brand']}\t{item['model']}\t{item['quantity']}\t{item['price']}\t{item['description']}\t{item['created_at']}")
else:
    print("Sorry, we do not have details for the requested item.")
