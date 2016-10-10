import sys
import math



class Coordinates(object):
    ''' Model the location of an entity.
    Provides the ability to calculate the distance to
    another entity, and also return its own coordinates.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.hypot(other.x - self.x, other.y - self.y)

    def unpack(self):
        return self.x, self.y

class Enemy(object):
    ''' Model an enemy, and store the basic state about it.
    This includes its id, location, and hp.
    '''
    def __init__(self, id, x, y, hp):
        self.id = id
        self.location = Coordinates(x, y)
        self.hp = hp


class Shooter(object):
    ''' This is the class where the magic happens. The shooter
    is the user in this game, and it keeps track of all enemies and
    data points.
    The current functionality is based on the nearest enemy distance,
    and these are the decisions made:
    1. Distance > 5000, move towards enemy
    2. Distance < 2500, move away from enemy
    3. Shoot
    '''

    def __init__(self):
        self.enemies = {}
        self.data_points = {}


    def update_state(self):
        '''
        Parse the input and assign/update state as necessary.
        Goes through user location, then data points, then
        enemies.
        '''
        # Record my location
        me_x, me_y = [int(i) for i in input().split()]
        self.location = Coordinates(me_x, me_y)

        # Data stuff - not doing yet
        data_count = int(input())
        for i in range(data_count):
            data_id, data_x, data_y = [int(j) for j in input().split()]

        # Delegate to assign_enemies for parsing and cleanup
        self.assign_enemies()

    def take_care_of_business(self):
        ''' This method decides the course of action, based on the
        nearest enemy.
        '''
        e_id, e_dist = self.nearest_enemy()
        print('Nearest enemy {} is {} away'.format(e_id, e_dist), file=sys.stderr)
        if e_dist > 5000:
            x, y = self.enemies[e_id].location.unpack()
            print('MOVE {} {}'.format(x, y))
        elif e_dist < 2500:
            print(self.move_away(e_id))
        else:
            print('SHOOT {}'.format(e_id))

    def nearest_enemy(self):
        '''
        Find the nearest enemy, and return their id and distance.
        '''
        min_dist = 99999999
        min_id = -1
        for id, enemy in self.enemies.items():
            dist = self.location.distance(enemy.location)
            if dist < min_dist:
                min_id = id
                min_dist = dist
            #print('enemy {} health: {}, Distance: {}'.format(
                #enemy.id, enemy.hp, dist), file=sys.stderr)
        return min_id, min_dist

    def assign_enemies(self):
        '''
        This method Parses the enemy part of input and creates the
        state of the users enemies as a dict in `self.enemies`
        '''
        # Record enemies and locations
        enemy_count = int(input())
        print('enemy count: {}'.format(enemy_count), file=sys.stderr)
        self.enemies = {}
        for i in range(enemy_count):
            id, x, y, life = [int(j) for j in input().split()]
            # Might want to not instantiate a new enemy each turn?
            self.enemies[id] = Enemy(id, x, y, life)

    def move_away(self, e_id):
        ''' Calculate the vector between the given enemy
        and return a MOVE command string with the appropriate
        x and y coordinates.
        '''

        e_x, e_y = self.enemies[e_id].location.unpack()
        x, y = self.location.unpack()

        # Get the vector distance
        distance = [x - e_x, y - e_y]
        # Get then normalized vector
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        # Get the direction now
        direction = [distance[0] / norm, distance[1] / norm]

        print('enemy: x: {} y: {}'.format(e_x, e_y), file=sys.stderr)
        print('my: x: {} y: {}'.format(x, y), file=sys.stderr)
        print('distance vector: {}'.format(distance), file=sys.stderr)
        print('normalized vector: {}'.format(norm), file=sys.stderr)
        print('direction: {}'.format(direction), file=sys.stderr)

        x_coord = x + 1000 * direction[0]
        y_coord = y + 1000 * direction[1]
        return 'MOVE {} {}'.format(int(x_coord), int(y_coord))



bond = Shooter()
# game loop
while True:
    bond.update_state()
    bond.take_care_of_business()

