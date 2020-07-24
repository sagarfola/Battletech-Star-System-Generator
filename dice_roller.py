import random


# Function to roll dice for many tables
def rolldice(die_num, die_size):
    a = []  # creates a list to store values
    for roll in range(0, die_num):
        a.append(random.randint(1, die_size))
    add = sum(a[0:])
    # print("Roll: " + str(die_num) + "d" + str(die_size) + " = " + str(add))
    return add
