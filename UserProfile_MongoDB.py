import pymongo
from pymongo import MongoClient

# CONNECT TO THE DB
client = MongoClient()

## Add your connection info here
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<cluster>/test?retryWrites=true&w=majority")
db = client.CityHall

# THE ID OF THE USER WHOSE PROFILE WE WILL BE RETRIEVING AND UPDATING
userId = 1

# GET THE USER'S PROFILE INFORMATION
## We can pull all of the info from the same document since we used embedding
user = db['Users'].find_one({"_id": userId})

# UPDATE THE USER DICTIONARY BASED ON USER INPUT IN THE APP
## We'll just update the user dictionary manually to save space
user.update( {
    "city": "Washington, DC",
    "latitude": 38.897760,
    "longitude": 77.036809,
    "hobbies": ["scrapbooking", "eating waffles", "signing bills"]
    } )

# UPDATE THE USER'S PROFILE IN THE DATABASE
## Since the user's data is stored in a single document, we only have to make one update
result = db['Users'].update_one({"_id": userId}, {"$set": user})
