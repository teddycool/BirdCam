import random, string
myrg = random.SystemRandom()
length = 10
# If you want non-English characters, remove the [0:52]
alphabet = string.letters[0:52] + string.digits
pw = str().join(myrg.choice(alphabet) for _ in xrange(length))
print pw