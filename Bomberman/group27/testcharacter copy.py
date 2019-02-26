# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        #
        # Get first monster in the world
        #
        # m = next(iter(wrld.monsters().values()))
        #
        # Go through the possible 8-moves of the monster
        #
        exit1 = 0
        exit2 = 0
        monsters = []
        bLoc = (-100,-100)
        exploders = []
        gWeight = 6
        mWeight = 10
        split = [4, 5, 6, 7, 11, 12, 13, 14]
        for checkx in range(wrld.width()):
            for checky in range(wrld.height()):
                cell = wrld.monsters_at(checkx,checky)
                if(wrld.exit_at(checkx, checky)):
                    exit1 = (checkx, checky)
                    exit2 = (0, checky)
                elif(wrld.bomb_at(checkx, checky)):
                    bLoc = (checkx, checky)
                elif(wrld.explosion_at(checkx, checky)):
                    exploders.append((checkx, checky))
                elif(cell is None):
                    pass
                else:
                    monsters.append(cell)
        moveList = {"Move":[], "Score":[]}
        if(self.y + 1 != wrld.height()):
            edges = self.x + 1 == wrld.width() or self.x == 0
            if(wrld.wall_at(self.x, self.y + 1) and edges):
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
                        if not wrld.wall_at(nextx, nexty):
                            if(self.y in split):
                                exit = exit2
                            else:
                                exit = exit1
                            mD = 0
                            mDist = 100
                            gmdist = 100
                            lowest = 1
                            for bad in monsters:
                                distX = (bad[0].x - nextx)**2
                                distY = (bad[0].y - nexty)**2
                                if((distX + distY)**0.5 < mDist):
                                    mDist = (distX + distY)**0.5
                                gdistX = (bad[0].x - nextx)**2
                                gdistY = (bad[0].y - nexty)**2
                                if((gdistX + gdistY)**0.5 < gmdist):
                                    gmdist = (distX + distY)**0.5
                                if(mDist < 5):
                                    mD = mDist
                                if(bad[0].y > lowest):
                                    lowest = bad[0].y
                            goalX = (exit[0] - nextx)**2
                            goalY = (exit[1] - nexty)**2
                            goalD = (goalX + goalY)**0.5
                            scoring = goalD*3 - 10*mD
                            bombX = (bLoc[0] - nextx)**2
                            bombY = (bLoc[1] - nexty)**2
                            bombD = (bombX + bombY)**0.5
                            bomber = 0
                            burning = 0
                            for cell in exploders:
                                if(nextx == cell[0] and nexty == cell[1]):
                                    burning = 500
                            bCheck = bombD < 5 and (nextx - bLoc[0] < 2 or nexty - bLoc[1] < 2)
                            if(bCheck):
                                bomber = 500
                            if(goalD < gmdist or self.y > lowest):
                                gWeight = 10
                                mWeight = 0
                            if(bLoc[0] > 0):
                                scoring = goalD*gWeight - mD*mWeight + bomber/(1+bombD) + burning
                            else:
                                scoring = goalD*gWeight - mD*mWeight + burning
                            moveList["Move"].append((dx,dy))
                            moveList["Score"].append(scoring)
        # print(moveList)
        indice = moveList["Score"].index(min(moveList["Score"]))
        decision = moveList["Move"][indice]
        self.move(decision[0],decision[1])
