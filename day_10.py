s_input = '''\
##.#..#..###.####...######
#..#####...###.###..#.###.
..#.#####....####.#.#...##
.##..#.#....##..##.#.#....
#.####...#.###..#.##.#..#.
..#..#.#######.####...#.##
#...####.#...#.#####..#.#.
.#..#.##.#....########..##
......##.####.#.##....####
.##.#....#####.####.#.####
..#.#.#.#....#....##.#....
....#######..#.##.#.##.###
###.#######.#..#########..
###.#.#..#....#..#.##..##.
#####.#..#.#..###.#.##.###
.#####.#####....#..###...#
##.#.......###.##.#.##....
...#.#.#.###.#.#..##..####
#....#####.##.###...####.#
#.##.#.######.##..#####.##
#.###.##..##.##.#.###..###
#.####..######...#...#####
#..#..########.#.#...#..##
.##..#.####....#..#..#....
.###.##..#####...###.#.#.#
.##..######...###..#####.#'''



# s_input = '''\
# .#....#####...#..
# ##...##.#####..##
# ##...#...#.#####.
# ..#.....#...###..
# ..#.#.....#....##'''


from collections import namedtuple
from copy import copy
import math


class Point:
  def __init__ (self, x: int, y: int):
    self.x = x
    self.y = y

  def __eq__(self, other: 'Point') -> bool:
    return self.x == other.x and self.y == other.y

  def __sub__(self, other: 'Point') -> 'Point':
    return Point(self.x - other.x, self.y - other.y)

  def __repr__(self) -> str:
    return 'Point' + str((self.x, self.y))

  def keys(self):
    return ['x', 'y']

  def __getitem__(self, key):
    if key == 'x' or key == 0:
      return self.x
    elif key == 'y' or key == 1:
      return self.y

    if type(key) == str:
      raise KeyError
    
    if type(key) == int:
      raise IndexError


def angle(p1: Point, p2: Point) -> float:
  return math.atan2(p1.y, p1.x) - math.atan2(p2.y, p2.x)



rows = s_input.split('\n')


def gcd(x, y): 
  while(y): 
      x, y = y, x % y 

  return x


def is_visible(p1: Point, p2: Point):
  vec = Point(p2.x - p1.x, p2.y - p1.y)
  v_gcd = abs(gcd(vec.x, vec.y))
  norm_vec = Point(vec.x // v_gcd, vec.y // v_gcd)
  cur_point = copy(p1)
  while cur_point != p2:
    cur_point.x += norm_vec.x
    cur_point.y += norm_vec.y
    if rows[cur_point.y][cur_point.x] == '#' and cur_point != p2:
      return False

  return True


def count_visible(start_row, start_col):
  count = 0
  for row_idx, row in enumerate(rows):
    for col_idx, val in enumerate(row):
      if row_idx == start_row and col_idx == start_col:
        continue
      
      if val == '#' and is_visible(Point(start_col, start_row), Point(col_idx, row_idx)):
        count += 1

  return count


max_count = 0
best_point = None

for row_idx, row in enumerate(rows):
  for col_idx, val in enumerate(row):
    if val == '#':
      count = count_visible(row_idx, col_idx)
      if count > max_count:
        max_count = count
        best_point = Point(col_idx, row_idx)

print ("Answer 1 is", max_count, best_point)


base_station = best_point

asteroids = []
for row_idx, row in enumerate(rows):
  for col_idx, val in enumerate(row):
    if row_idx == base_station.y and col_idx == base_station.x:
      continue

    if val == '#':
      asteroids.append(Point(col_idx, row_idx))



def rotate(origin: Point, point: Point, angle: float) -> Point:
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return Point(qx, qy)


def shoot(base: Point, target: Point) -> Point:
  # vec = Point(target.x - base.x, target.y - base.y)
  vec = target - base
  v_gcd = abs(gcd(vec.x, vec.y))
  norm_vec = Point(vec.x // v_gcd, vec.y // v_gcd)
  cur_point = copy(base)
  while True:
    cur_point.x += norm_vec.x
    cur_point.y += norm_vec.y
    if cur_point in asteroids:
      return cur_point


laser_vec = Point(0, -1)

def vector_compare(vec):
  ang = angle(vec - base_station, laser_vec)
  if ang < 0:
    ang += 2 * math.pi

  return ang

print(asteroids)

destroyed_count = 0
while destroyed_count < 200:
  closest = min(asteroids, key=vector_compare)
  print('Closest', closest, 'angle', angle(closest - base_station, laser_vec))
  destroyed = shoot(base_station, closest)
  laser_vec = destroyed - base_station
  laser_vec = rotate(Point(0, 0), laser_vec, 0.001)
  print('Destroyed', destroyed)
  print('Laser vec', laser_vec)
  asteroids.remove(destroyed)
  destroyed_count += 1

print('200th destroyed point', destroyed)
