#unlimited arguments
def unlimited_arguments(*args, **kwargs):
    for k, argument in kwargs.items():
        print(k, argument)

unlimited_arguments(3, 4, 5, 2, 7, name="Max", age=29)