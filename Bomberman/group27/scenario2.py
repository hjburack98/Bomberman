# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def getDistance(self, x1, y1, x2, y2):
        xDist = (x1-x2)**2
        yDist = (y1-y2)**2
        dist = (xDist + yDist)**0.5
        return dist

    def do(self, wrld):
        #
        # Get first monster in the world
        #
        # m = next(iter(wrld.monsters().values()))
        #
        # Go through the possible 8-moves of the monster
        #
        exit = 0
        monsters = []
        bLoc = (-100,-100)
        exploders = []
        gWeight = 6
        mWeight = 10
        walls = []
        for checkx in range(wrld.width()):
            for checky in range(wrld.height()):
                cell = wrld.monsters_at(checkx,checky)
                if(wrld.exit_at(checkx, checky)):
                    exit = (checkx, checky)
                elif(wrld.bomb_at(checkx, checky)):
                    bLoc = (checkx, checky)
                elif(wrld.explosion_at(checkx, checky)):
                    exploders.append((checkx, checky))
                elif(wrld.wall_at(checkx, checky)):
                    walls.append(checky)
                elif(cell is None):
                    pass
                else:
                    monsters.append(cell)
        walls = set(walls)
        moveList = {"Move":[], "Score":[]}
        edges = self.x + 1 == wrld.width() # or self.x == 0
        highest = 20
        farness = 10
        for bad in monsters:
            if(bad[0].y < highest):
                highest = bad[0].y
                farness = abs(self.x - bad[0].x)
        if(self.y + 1 != wrld.height()):
            if(wrld.wall_at(self.x, self.y + 1) and edges and (farness > 4 or (highest - self.y) > 4)):
                self.place_bomb()
        if(edges and self.y - 1 in walls and (highest - self.y) < 4):
            exit = (self.x, 0)
            self.place_bomb()
        # Loop through delta x
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            nextx = self.x+dx
            if (nextx >=0) and (nextx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bound indexing
                    nexty = self.y+dy
                    if (nexty >=0) and (nexty < wrld.height()):
                        # No need to check impossible moves
                        burn = (nextx, nexty) in exploders
                        if not wrld.wall_at(nextx, nexty) and not burn:
                            mD = 0
                            mDist = 100
                            closest = 0
                            for bad in monsters:
                                monsterDist = self.getDistance(bad[0].x,bad[0].y,nextx,nexty)
                                if(monsterDist < mDist):
                                    mDist = monsterDist
                                    closest = bad
                            # if(edges and self.y + 1 not in walls and mDist < 4 and closest[0].x==self.x):
                            #     self.place_bomb()
                            goalDistance = self.getDistance(exit[0],exit[1],nextx,nexty)
                            bombDistance = self.getDistance(bLoc[0],bLoc[1],nextx,nexty)
                            bomber = 0
                            xAllign = (nextx - bLoc[0]) == 0
                            yAllign = (nexty - bLoc[1]) == 0
                            bCheck = bombDistance < 5 and (xAllign or yAllign)
                            if(bCheck):
                                bomber = 500
                            if(mDist < 3):
                                mD = 10
                            scoring = goalDistance*gWeight + mD*mWeight + bomber/(1+bombDistance)
                            moveList["Move"].append((dx,dy))
                            moveList["Score"].append(scoring)
        indice = moveList["Score"].index(min(moveList["Score"]))
        decision = moveList["Move"][indice]
        self.move(decision[0],decision[1])
