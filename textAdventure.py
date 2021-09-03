# 'textAdventurePreset' file can be modified to create custom maps, refer to specified file format

# Player object holds user relevant info
class Player:
    def __init__(self, name, skill, traveled=0):
        self.name = name
        self.skill = skill
        self.traveled = traveled

    def info(self):
        print('\n"They call me {0} and my skill is {1}!"\n'.format(self.name, self.skill))

    def distance(self):
        print('\nYou have traveled a distance of {0} rooms.\n'.format(self.traveled))


# Room object used to fill Map(), store routes to other rooms
class Room():
    def __init__(self, name, desc, paths):
        self.name = name
        self.desc = desc
        self.paths = paths

    def routes(self):
        output = ""
        for path in self.paths.keys():
            if path == "forward":
                output += "To your front is the {0}.\n".format(self.paths.get(path))
            else:
                output += "To your {0} is the {1}.\n".format(path, self.paths.get(path))
        print(output)

    def arrival(self):
        print("\nYou enter the {0} and observe your surroundings. {1}\n".format(self.name, self.desc))


# Map object instantiates rooms from 'textAdventurePreset' file
class Map:
    def __init__(self):
        self.rooms = self.readFile()

    # method reading file, very format-dependent
    def readFile(self):
        global info
        roomList = []
        roomInfo = []
        pathDict = {}
        entry = ""

        for line in open('textAdventurePreset', 'r').readlines()[4:]:
            line = line.strip()

            if line != "":
                entry += line
            else:
                while len(entry) != 0:
                    a = entry.find('"')
                    b = entry.find('"', a + 1)

                    roomInfo.append(entry[a + 1:b])
                    entry = entry[b + 1:]

                for route in roomInfo[2:]:
                    routeInfo = route.split(':')
                    pathDict[routeInfo[0]] = routeInfo[1]

                roomList.append(Room(roomInfo[0], roomInfo[1], pathDict))
                pathDict = {}
                roomInfo = []

        return roomList


# Game object acts as MASTER, tracking player's location, input, and map restrictions
class Game:
    def __init__(self):
        self.title = "A Walk Throughout the Castle"
        self.castle = Map()
        print("Welcome to {0}, programmed by Anthony Norderhaug :)\n".format(self.title))

        # add except handling
        self.player = Player(raw_input('What is your name, adventurer?\n'),
                             raw_input('And what is your skill? (swordsmanship, alchemy, blacksmithing, etc.) \n'))
        self.process()

    def process(self):
        location = self.retrieveRoom("Grand Hall")
        # to change starting point, edit "Grand Hall" to another pre-existing room

        while location != 'exit':

            choice = self.action()
            if choice == 'a':
                self.player.info()
            elif choice == 'b':
                self.player.distance()
            elif choice == 'c':
                location.arrival()
                location.routes()
                location = self.prompt(location)
                self.player.traveled += 1
            elif choice == 'd':
                location = 'exit'

        print('\nBASED ENDING!\n'
              'Having walked around the castle for long enough, you come across a map.\n'
              'On it are detailed routes in and out of the forest.\n'
              'The mystery still remains how and why you came here...\n'
              "And what happened to the castle's original inhabitants...\n"
              "But it's something you'd rather not bother yourself with.\n")

        print("SCORE:")
        self.player.distance()
        print("(THANKS FOR PLAYING {0}, HOPE YOU ENJOYED THE GAME!)\n".format(self.title))

    def action(self):
        inputs = ['a', 'b', 'c', 'd']
        msg = ("What action would you like to take?\n"
               "a: Retrieve player info\n"
               "b: Retrieve distance traveled\n"
               "c: Travel onward!\n"
               "d: Exit\n")

        choice = raw_input(msg).strip()
        while choice not in inputs:
            choice = input('Invalid input, try again').strip()

        return choice

    def prompt(self, room):
        move = raw_input('In which direction would you like to go? (ex: forward, left, right, back)\n')

        while move.lower() not in [direct.lower() for direct in room.paths.keys()]:
            if move.lower() == "exit":
                return 'exit'
            elif room.name == "Forest":
                move = raw_input("You cannot go {0}. You're sure to get lost.\n".format(move.lower()))
            else:
                move = raw_input('You cannot go {0}. There is a wall.\n'.format(move.lower()))

        print('Heading {0}...\n'.format(move.lower()))

        return self.retrieveRoom(room.paths.get(move))

    def retrieveRoom(self, name):
        for room in self.castle.rooms:
            if room.name == name:
                return room


# Main function to run program
if __name__ == '__main__':
    myGame = Game()
