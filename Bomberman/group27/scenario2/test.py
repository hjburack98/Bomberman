# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group27')
from unified import TestCharacter


counter = 0
for i in range(200):
    # Create the game
    random.seed(random.randint(0,100000)) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("monster", # name
                                "S",       # avatar
                                3, random.randint(4, 18),      # position
    ))
    g.add_monster(SelfPreservingMonster("monster", # name
                                        "A",       # avatar
                                        3, random.randint(4, 18),     # position
                                        2          # detection range
    ))

    # TODO Add your character
    g.add_character(TestCharacter("me", # name
                                  "C",  # avatar
                                  0, 0  # position
    ))

    # Run!
    counter = counter + g.go()
print(counter/200)
