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
        # Loop through delta x
        exit = 0
        dist = {}
        moves = {}
        parent = {}
        unvisited = []
        for checkx in range(wrld.width()):
            for checky in range(wrld.height()):
                if(wrld.exit_at(checkx, checky)):
                    exit = (checkx, checky)
                if(not wrld.wall_at(checkx, checky)):
                    point = (checkx, checky)
                    unvisited.append(point)
                    parent[point] = 0
                    dist[point] = 10000
                    moves[point] = 0
        dist[(self.x,self.y)] = 0
        while(unvisited):
            d = 10000
            point = 0
            for tar in unvisited:
                if(dist[tar] < d):
                    d = dist[tar]
                    point = tar
            unvisited.remove(point)
            # next_move = self.pather((self.x,self.y))
            for dx in [-1, 0, 1]:
                # Avoid out-of-bound indexing
                nextx = point[0]+dx
                if (nextx >=0) and (nextx < wrld.width()):
                    # Loop through delta y
                    for dy in [-1, 0, 1]:
                        # Avoid out-of-bound indexing
                        nexty = point[1]+dy
                        if (nexty >=0) and (nexty < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(nextx, nexty):
                                newP = (nextx, nexty)
                                newDist = dist[point] + self.getDistance(nextx,nexty,point[0],point[1])
                                newMoves = moves[point] + round(self.getDistance(nextx,nexty,point[0],point[1]))
                                if(newDist < dist[newP]):
                                    dist[newP] = newDist
                                    parent[newP] = point
                                    moves[newP] = newMoves

        motion = moves[exit]
        curr = exit
        for i in range(motion - 1):
            curr = parent[curr]
        newX = curr[0] - self.x
        newY = curr[1] - self.y
        self.move(newX, newY)
