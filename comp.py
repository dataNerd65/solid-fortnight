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


def look_item(user_choice):
    print("Let me check if the item(s) is present.")
    lemmatizer = WordNetLemmatizer()
    lemmatized_choice = lemmatizer.lemmatize(user_choice)
    #print("Lemmatized choice:", lemmatized_choice)
    return lemmatized_choice

def check_item_in_Database(user_choice):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("SELECT * FROM itemsinfo WHERE item_type = %s", (user_choice,))

            myresult = mycursor.fetchall()
        return len(myresult) > 0
    except mysql.connector.Error as err:
        print("An error occurred while querying the database:", err)
        return False

lemmatized_choice = look_item(user_choice)
is_in_database = check_item_in_Database(lemmatized_choice)

#print("Is the item in the database?", is_in_database)

if is_in_database is True:
    print(f"Yes we have {user_choice}.")
else:
    print("Sorry, we do not have what you want.")
    

#print(f"We have the following types of {user_choice}.")

def get_item_details(user_choice):
    try:
        with mydb.cursor() as mycursor:
            mycursor.execute("SELECT * FROM itemsinfo WHERE item_type = %s", [user_choice])
            item_details = mycursor.fetchall()
        return item_details
    except mysql.connector.Error as err:
        print("An error occurred while querying the database:", err)
        return None

# Fetch item details from the database
item_details = get_item_details(lemmatized_choice)

if item_details:
    print(f"Here are the details of {user_choice}:")
    print("ID\tBrand\tModel\tQuantity\tPrice\tDescription\tCreated At")
    for item in item_details:
        print(f"{item[0]}\t{item[2]}\t{item[3]}\t{item[4]}\t{item[5]}\t{item[6]}\t{item[7]}")
else:
    print("Sorry, we do not have details for the requested item.")




