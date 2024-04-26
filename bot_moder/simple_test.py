# test postgres for moder bot

import sqlhelper

print('- start test sql -')
print()

result = sqlhelper.db_check_violations(2)

if result:
    print('user exists')
else:
    print('not exists: result is ' + str(result)) 


print()
print(' - end - ')
