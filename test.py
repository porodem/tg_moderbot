from datetime import datetime, timedelta
import re

# calculate time now + 3 minutes
ban_time = datetime.now() + timedelta(hours=0, minutes=3)

print(ban_time)

# read line from file
token = open("token.txt","r")
token = token.readline()

print(token)

# regex test
choice = ""
while choice != "exit":
    choice = input("Write something: ")
    if re.search("fu(c|k)|bitch",choice):
        print('offencive')
    else:
        print('good')

print('- END -')


