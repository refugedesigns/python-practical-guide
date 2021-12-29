# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.

def print_result(fun):
    print(fun())

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.

print_result(lambda: 2 * 5)

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.


def tweaked_fun(fun, *args):
    for num in fun(*args):
        print(num)

tweaked_fun(lambda *args: [el * 2 for el in args], 3, 5, 5, 4, 6, 6)

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.

def tweaked_function(fun, *args):
    for num in fun(*args):
        print("{0:^20}".format(num))

tweaked_function(lambda *args: [el * 2 for el in args], 3, 5, 5, 4, 6, 6)
