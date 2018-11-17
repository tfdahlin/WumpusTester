#!/usr/bin/python3
import subprocess, io, sys

class Tile:
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content
        self.visited = False
        pass
    def __str__(self):
        return self.content
    def visit(self):
        self.visited = True
    def is_visited(self):
        return self.visited

class World:
    def __init__(self, arr):
        self.grid = []
        for i in range(4):
            tmp = []
            for j in range(4):
                curr_tile = Tile(i, j, arr[i][j])
                tmp.append(curr_tile)
            self.grid.append(tmp)
        self.grid[3][0].visit()
        self.bot_x = 0
        self.bot_y = 3
        self.arrow = True
        self.gold = False

    def __str__(self):
        result = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.bot_x == j and self.bot_y == i:
                    result += "r"
                else:
                    result += str(self.grid[i][j])
            result += "\n"
        return result[:-1]
    
    def query(self):
        if self.grid[self.bot_y][self.bot_x].is_visited():
            print("Already visited.")
            return None
        else:
            self.grid[self.bot_y][self.bot_x].visit()
            info = [False, False, False, False]
            if self.bot_x == 0: # don't look left
                # look right
                info = self.pairwise_or(info, self.look_right())
                if self.bot_y == 0: # don't look up
                    # look down
                    info = self.pairwise_or(info, self.look_down())
                elif self.bot_y == 3: # don't look down
                    info = self.pairwise_or(info, self.look_up())
                else: # look all directions
                    info = self.pairwise_or(info, self.look_up())
                    info = self.pairwise_or(info, self.look_down())
            elif self.bot_x == 3: # don't look right
                # look left
                info = self.pairwise_or(info, self.look_left())
                if self.bot_y == 0: # don't look up
                    # look down
                    info = self.pairwise_or(info, self.look_down())
                elif self.bot_y == 3: # don't look down
                    info = self.pairwise_or(info, self.look_up())
                else: # look all directions
                    info = self.pairwise_or(info, self.look_up())
                    info = self.pairwise_or(info, self.look_down())
            else: # look left + right
                info = self.pairwise_or(info, self.look_left())
                info = self.pairwise_or(info, self.look_right())
                if self.bot_y == 0: # don't look up
                    # look down
                    info = self.pairwise_or(info, self.look_down())
                elif self.bot_y == 3: # don't look down
                    info = self.pairwise_or(info, self.look_up())
                else: # look all directions
                    info = self.pairwise_or(info, self.look_up())
                    info = self.pairwise_or(info, self.look_down())
            result = 0
            if(info[0]):
                result += 1
            if(info[1]):
                result += 2
            if(info[2]):
                result += 4
            if(self.grid[self.bot_y][self.bot_x].content == "g"):
                result += 8
            return result

    def pairwise_or(self, arr1, arr2):
        result = []
        for arr1_item, arr2_item in zip(arr1, arr2):
            result.append(arr1_item or arr2_item)
        return result

    def look_left(self):
        return self.assess_contents(self.grid[self.bot_y][self.bot_x-1].content)
    def look_right(self):
        return self.assess_contents(self.grid[self.bot_y][self.bot_x+1].content)
    def look_up(self):
        return self.assess_contents(self.grid[self.bot_y-1][self.bot_x].content)
    def look_down(self):
        return self.assess_contents(self.grid[self.bot_y+1][self.bot_x].content)

    def assess_contents(self, contents):
        if contents == "g":
            return [False, False, True, False]
        elif contents == "w":
            return [False, True, False, False]
        elif contents == "h":
            return [True, False, False, False]
        else:
            return [False, False, False, False]

    def move(self, direction):
        if(direction == "n"):
            if(self.bot_y == 0):
                raise Exception("Walked out of map. (Too far north)")
            else:
                self.bot_y -= 1
        if(direction == "s"):
            if(self.bot_y == 3):
                raise Exception("Walked out of map. (Too far south)")
            else:
                self.bot_y += 1
        if(direction == "e"):
            if(self.bot_x == 3):
                print("Error. Cannot move east.")
                raise Exception("Walked out of map. (Too far east)")
            else:
                self.bot_x += 1
        if(direction == "w"):
            if(self.bot_x == 0):
                raise Exception("Walked out of map. (Too far west)")
            else:
                self.bot_x -= 1
        if(self.grid[self.bot_y][self.bot_x].content in ["h", "w"]):
            cause = self.grid[self.bot_y][self.bot_x].content
            if(cause == "h"):
                raise Exception("You fell into a hole.")
            if(cause == "w"):
                raise Exception("You were killed by the Wumpus.")
        if(self.grid[self.bot_y][self.bot_x].content == "g"):
            self.gold = True
    
    def kill_wumpus(self, direction):
        if(not self.arrow):
            raise Exception("You've already used your arrow.")
        self.arrow = False
        if(direction == "n"):
            if(self.bot_y != 0):
                if(self.grid[self.bot_y-1][self.bot_x].content == "w"):
                    self.grid[self.bot_y-1][self.bot_x].content = "e"
        if(direction == "e"):
            if(self.bot_x != 3):
                if(self.grid[self.bot_y][self.bot_x+1].content == "w"):
                    self.grid[self.bot_y][self.bot_x+1].content = "e"
        if(direction == "s"):
            if(self.bot_y != 3):
                if(self.grid[self.bot_y+1][self.bot_x].content == "w"):
                    self.grid[self.bot_y+1][self.bot_x].content = "e"
        if(direction == "w"):
            if(self.bot_x != 0):
                if(self.grid[self.bot_y][self.bot_x-1].content == "w"):
                    self.grid[self.bot_y][self.bot_x-1].content = "e"
        

def usage(usage_type = None):
    print("Error: invalid usage.", end="")
    if(usage_type != None):
        print(" " + usage_type)
    print()
    print("Usage:")
    print(sys.argv[0] + " <your_executable> <difficulty>")
    print()
    print("Difficulty is an optional argument to test against a set of prebuilt examples. Valid difficulty settings are \"easy\", \"medium\", and \"hard\".")

def main():
    argc = len(sys.argv)
    if argc < 3:
        usage("Too few arguments.")
    elif argc == 3:
        difficulty = sys.argv[2]
        if difficulty.lower() in ["easy", "medium", "hard"]:
            runTests(sys.argv[1], difficulty.lower())
        else:
            usage("'" + difficulty + "' is not a valid difficulty setting.")
    else:
        usage("Too many arguments.")


def test(program, world):
    try:
        my_process = subprocess.Popen(program, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        valid_inputs = [
            "n", "e", "s", "w",
            "kill n", "kill e", "kill s", "kill w",
            "input:"
        ]
        while(my_process.returncode is None):
            line = my_process.stdout.readline().decode('utf-8').rstrip()
            if line in [None, ""] or line.isspace():
                break
            elif line in valid_inputs:
                if "kill" in line: 
                    world.kill_wumpus(line[-1:])
                elif "input" in line:
                    value = world.query()
                    if value is None:
                        return False
                    else:
                        my_process.stdin.write(str.encode(str(value) + "\n"))
                        my_process.stdin.flush()
                else:
                    try:
                        world.move(line)
                    except Exception as e:
                        print("Test failed. ",end="")
                        print(e)
                        return False
                    
            else:
                print("Invalid input: " + line)
                return False
                
    except Exception as e:
        print(e)
        print("Quitting test.")
        return False
    if(world.bot_x == 0 and world.bot_y == 3):
        if(world.gold):
            print("Passed!")
            return True
        else:
            print("Test failed. Did not retrieve gold.")
            return False
    else:
        print("Test failed. Did not return to start.")
        return False


def runTests(program, difficulty):
    failures = 0
    if difficulty == "easy":
        print("Running easy tests.")
        world1 = World([
            ["e", "e", "e", "g"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "w"]
        ])
        if(test(program, world1)):
            pass
        else:
            failures += 1
        world2 = World([
            ["e", "e", "e", "h"],
            ["e", "g", "e", "e"],
            ["e", "e", "e", "w"],
            ["e", "e", "e", "e"]
        ])
        if(test(program, world2)):
            pass
        else:
            failures += 1
        world3 = World([
            ["h", "h", "e", "e"],
            ["e", "e", "e", "w"],
            ["e", "e", "g", "e"],
            ["e", "e", "e", "e"]
        ])
        if(test(program, world3)):
            pass
        else:
            failures += 1
        print()
    elif difficulty == "medium":
        # TODO: Medium tests
        print("Running medium tests.")
    elif difficulty == "hard":
        # TODO: Hard tests
        print("Running hard tests.")

        # Uncomment this challenge if you dare.
        '''
        evil = World([
            ["e", "e", "h", "g"],
            ["e", "e", "h", "w"],
            ["e", "e", "e", "e"],
            ["e", "e", "h", "h"]
        ])
        '''
    else:
        pass
    print("All tests completed with %d failures." % failures)


if __name__ == "__main__":
    main()
