import mysql.connector

# CONNECT TO THE DB
## Add your connection info here
mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  passwd="password",
  database="CityHall"
)
mycursor = mydb.cursor(dictionary=True)

# THE ID OF THE USER WHOSE PROFILE WE WILL BE RETRIEVING AND UPDATING
userId = 1

# GET THE USER'S PROFILE INFORMATION
## Pull the info from the Users and Hobbies tables
sql = "SELECT * FROM Users LEFT JOIN Hobbies ON Users.ID = Hobbies.user_id WHERE Users.id=%s"
values = (userId,)
mycursor.execute(sql, values)
user = mycursor.fetchone()

## Loop through the remaining results in the cursor to get the list of hobbies 
## and store them in the user dictionary
hobbies = []
if (user["hobby"]):
  hobbies.append(user["hobby"])
for user in mycursor:
  hobbies.append(user["hobby"])
user["hobbies"] = hobbies

# UPDATE THE USER DICTIONARY BASED ON USER INPUT IN THE APP
## We'll just update the user dictionary manually for simplicity
user.update( {
    "city": "Washington, DC",
    "location": [-77.036809, 38.897760],
    "hobbies": ["scrapbooking", "eating waffles", "signing bills"]
    } )

# UPDATE THE USER'S PROFILE IN THE DATABASE
## First update what is stored in the Users table
sql = "UPDATE Users SET first_name=%s, last_name=%s, cell=%s, city=%s, latitude=%s, longitude=%s, school=%s WHERE (ID=%s)"
values = (user["first_name"], user["last_name"], user["cell"], user["city"], user["location"][1], user["location"][0], user["school"], userId)
mycursor.execute(sql, values)
mydb.commit()

## Delete existing records in Hobbies table and add new ones
sql = "DELETE FROM Hobbies WHERE user_id=%s"
values = (userId,)
mycursor.execute(sql, values)
mydb.commit()

if(len(user["hobbies"]) > 0):
  sql = "INSERT INTO Hobbies (user_id, hobby) VALUES (%s, %s)"
  values = []
  for hobby in user["hobbies"]:
    values.append((userId, hobby))
  mycursor.executemany(sql,values)
  mydb.commit()
