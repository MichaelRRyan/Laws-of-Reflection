import GameObject

class Level(object):
    def __init__(self):
        self.level_width = 0
        self.top_goal = GameObject.GameObject(0, 0, 25, 50, 2)
        self.bottom_goal = GameObject.GameObject(0, 0, 25, 50, 2)
        self.top_blocks = []
        self.bottom_blocks = []

def load_level(level_num):
    file = open("levels/level" + str(level_num) + ".data", "r")

    level = Level()

    for line in file:
        items = line.split()

        if len(items) == 0 or line[0] == "#":
            continue

        if len(items) == 2 and items[0] == "w":
            level.level_width = float(items[1])
            continue

        if len(items) == 3:
            if items[0] == "tg":
                level.top_goal.x = int(items[1])
                level.top_goal.y = 300 - int(items[2])
            elif items[0] == "bg":
                level.bottom_goal.x = int(items[1])
                level.bottom_goal.y = 300 + int(items[2]) - level.bottom_goal.height
            continue


        if len(items) == 5:
            if items[0] == "t":
                level.top_blocks.append(GameObject.GameObject(float(items[1]), 300 - float(items[2]), float(items[3]), float(items[4]), 0))
            else:
                level.bottom_blocks.append(GameObject.GameObject(float(items[1]), 300 + float(items[2]) - float(items[4]), float(items[3]), float(items[4]), 0))

    file.close()

    return level