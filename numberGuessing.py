import random


def initBounds():
    global bounds
    applicable = False

    while not applicable:
        bounds = [int(bound) for bound in raw_input("? Enter lower and upper bounds.\n").split(" ")]

        if bounds[0] > bounds[1]:
            print("ERROR: Lower bound > upper bound, redo!\n")
        elif bounds[0] <= 0:
            print("ERROR: Lower bound must be greater than 0\n")
        elif len(bounds) > 2:
            print("ERROR: More than 2 bounds\n")
        else:
            applicable = True


def giveHint():
    global firstAttempt, cpuAnswer, hints
    hint = "TOTAL HINTS:"

    while hint in hints:
        if firstAttempt:
            firstAttempt = False
            hint = "Guessing a number between {0} and {1}.".format(
                bounds[0], bounds[1])
        else:
            randNumber = random.randrange(0, 4)
            if randNumber == 0 and cpuAnswer != bounds[0]:
                hint = "The number is greater than {0}".format(
                    random.randrange(bounds[0], cpuAnswer))
            if randNumber == 1 and cpuAnswer != bounds[1]:
                hint = "The number is less than {0}".format(
                    random.randrange(cpuAnswer + 1, bounds[1] + 1))
            if randNumber == 2:
                for x in range(2, (cpuAnswer / 2) + 1):
                    if cpuAnswer % x == 0:
                        hint = "The number is divisible by {0}.".format(x)
                hint = "The number is prime."
            if randNumber == 3:
                for x in range(cpuAnswer, bounds[1] + 1, cpuAnswer):
                    if x % cpuAnswer == 0 and x != cpuAnswer:
                        hint = "The number is a multiple of {0}.".format(x)
                hint = "The number is not a multiple of any number within the bounds."

    return hint


def totalHints():
    global hints
    output = ""

    hints.append(giveHint())

    for hint in hints:
        output += hint + "\n"

    return output + "\nWhat is it?\n\n"


if __name__ == '__main__':
    # global variables
    points = 2000
    bounds = [1, 0]
    userAnswer = None
    firstAttempt = True
    hints = ["TOTAL HINTS:"]

    # setting seed and initializing bounds
    seed = raw_input("Input a SINGLE int or float seed.\n").split(" ")[0]
    print("Using seed {0}\n".format(seed))
    random.seed(seed)
    initBounds()

    # generated number and prompting user
    cpuAnswer = random.randrange(bounds[0], bounds[1] + 1)
    print("note: For every incorrect guess, points are halved\n")

    while userAnswer != cpuAnswer:
        print("POINT TOTAL: {0}\n".format(points))
        points /= 2
        userAnswer = input(totalHints())

    # confirmation
    print("\nThat's right! The number is {0}, congratulations!".format(userAnswer))
