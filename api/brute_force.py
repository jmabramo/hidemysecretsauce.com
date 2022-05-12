import itertools
import string
from database import users 
import sys
import bcrypt


# Takes URL and Username as command line arguments.
user = sys.argv[1]
hash = users.find_one({'name': user})["password"]

for n in range (1, 5):
    for guess in itertools.product(string.printable, repeat=n):
        guess = "".join(guess)
        if bcrypt.checkpw(guess, hash):
            print(guess)
            exit()
