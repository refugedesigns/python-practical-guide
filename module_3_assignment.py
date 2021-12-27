# 1) Create a list of names and use a for loop to output the length of each name(len()).
names = ["Max", "Eras", "Philo", "Vida", "Dacosta", "Portia", "Patricia", "Eric", "David", "Samuel", "Solomon"]

for index in range(len(names)):
    print(len(names[index]))

# 2) Add an if check inside the loop to only output names longer than 5 characters.
for index in range(len(names)):
    if len(names[index]) > 5:
        print(names[index])

# 3) Add another if check to see whether a name includes a “n” or “N”  character.
for index in range(len(names)):
    if len(names[index]) > 5 and ("n" in names[index] or "N" in names[index]):
        print(names[index])

# 4) Use a while loop to empty the list of names(via pop())
list_not_empty = True 

while list_not_empty:
    names.pop()
    if len(names) < 1:
        list_not_empty = False 

print(names)

