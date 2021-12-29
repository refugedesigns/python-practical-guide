import copy
# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person.
# Fill in any data you want.
persons = [{"name": "Frank", "age": 20, "hobbies": ["football", "cooking"]}, {
    "name": "Samuel", "age": 32, "hobbies": ["skating", "basketball"]}, {"name": "Erica", "age": 25, "hobbies": ["racing", "singing"]}]

# 2) Use a list comprehension to convert this list of persons into a list of names(of the persons).
names = [person['name'] for person in persons]
print(names)
# 3) Use a list comprehension to check whether all persons are older than 20.
age = all([person['age'] > 20 for person in persons])
print(age)
# 4) Copy the person list such that you can safely edit the name of the first person(without changing the original list).
new_persons = copy.deepcopy(persons)
new_persons[0]['name'] = "Max"
print(new_persons)
print(persons)
# 5) Unpack the persons of the original list into different variables and output these variables.
person1, person2, person3 = persons
print(person1)
print(person2)
print(person3)