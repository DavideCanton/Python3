import re

r = re.sub("(?<=abc)(?=ef)", "d", "abcefghabcf")
print(r)
