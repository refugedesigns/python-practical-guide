name = input("Enter your name: ")
age = int(input("Enter your age: "))


def print_age_and_name():
    """Print user name and age"""
    print("My name is " + name + ", I am " + str(age) + " years")


def print_height_and_weight(height, weight):
    """Print the height and weight of a user"""
    print("My height is " + str(height) + " and my weight is " + str(weight))


def return_decades(years):
    """
    Calculates the number of decades of the user

    Arguments: 
        params years: The years of which the use has lived

    Returns a string together with the calculated decades
    """
    result = years // 10
    return print("I have lived for " + str(result) + " decades")


print_age_and_name()

print_height_and_weight(5.8, 63)

return_decades(32)
