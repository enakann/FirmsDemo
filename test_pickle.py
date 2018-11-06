import pickle
from os import path

user_to_delete = 'user2'

# Open the database if it exists, otherwise create one...
if path.isfile('database.db'):
    with open('database.db','rb') as f:
        db = pickle.load(f)
else: # Create some database.db with users&passwords to test this program..
    db = {'user1':'password1', 'user2':'password2', 'user3':'password3'}
    with open('database.db', 'wb') as f:
        pickle.dump(db, f)

# try to delete the given user, handle if the user doesn't exist.
try:
    del db[user_to_delete]
except KeyError:
    print("{user} doesn't exist in db".format(user=user_to_delete))

# write the 'new' db to the file.
with open('database.db', 'wb') as f:
    pickle.dump(db, f)
