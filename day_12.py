s_input = '''<x=1, y=4, z=4>
<x=-4, y=-1, z=19>
<x=-15, y=-14, z=12>
<x=-17, y=1, z=10>'''

# s_input = '''<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>'''

# s_input = '''<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>'''

import re
from types import SimpleNamespace
from itertools import product
import pprint
from copy import deepcopy
from string import Template


parse_template = re.compile(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>')
moon_lines = s_input.split('\n')

def parse_moon(moon_line):
  res = parse_template.match(moon_line)
  return SimpleNamespace(
    pos=SimpleNamespace(x=int(res.group('x')), y=int(res.group('y')), z=int(res.group('z'))),
    vel=SimpleNamespace(x=0, y=0, z=0)
  )
   

moons = {
  'Io': parse_moon(moon_lines[0]),
  'Europa': parse_moon(moon_lines[1]),
  'Ganymede': parse_moon(moon_lines[2]),
  'Callisto': parse_moon(moon_lines[3])
}


def process_gravity(moons: list):
  for m1, m2 in product(moons, moons):
    if m1 == m2:
      continue

    if m1.pos.x > m2.pos.x:
      m1.vel.x -= 1
      m2.vel.x += 1

    if m1.pos.y > m2.pos.y:
      m1.vel.y -= 1
      m2.vel.y += 1

    if m1.pos.z > m2.pos.z:
      m1.vel.z -= 1
      m2.vel.z += 1

    


def process_velocity(moons: list):
  for moon in moons:
    moon.pos.x += moon.vel.x
    moon.pos.y += moon.vel.y
    moon.pos.z += moon.vel.z


def calc_energy(moons):
  total = 0
  for moon in moons:
    pot = abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)
    kin = abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z)
    total += kin * pot

  return total


for step in range(1000):
  process_gravity(moons.values())
  process_velocity(moons.values())


print('Answer 1', calc_energy(moons.values()))


pp = pprint.PrettyPrinter()


moons = {
  'Io': parse_moon(moon_lines[0]),
  'Europa': parse_moon(moon_lines[1]),
  'Ganymede': parse_moon(moon_lines[2]),
  'Callisto': parse_moon(moon_lines[3])
}

count = 0

hash_template = Template('$pos_x|$pos_y|$pos_z||$vel_x|$vel_y|$vel_z')

def state_hash(moons):
  def moon_hash(moon):
    return hash_template.substitute(
      pos_x = moon.pos.x,
      pos_y = moon.pos.y,
      pos_z = moon.pos.z,
      vel_x = moon.vel.x,
      vel_y = moon.vel.y,
      vel_z = moon.vel.z
    )

  moons_hash = ''
  for moon_name, moon in moons.items():
    mh = moon_name + '_' + moon_hash(moon)
    moons_hash += mh

  return moons_hash


def coord_hash(moons, coord):

  def single_hash(moon, coord):
    pos = moon.pos
    vel = moon.vel

    return '{0}_{1}'.format(pos.__dict__.get(coord), vel.__dict__.get(coord))

  moons_hash = ''
  for moon_name, moon in moons.items():
    mh = moon_name + '_' + single_hash(moon, coord) + '__'
    moons_hash += mh

  return moons_hash

x_history = dict()
y_history = dict()
z_history = dict()

# history = set()

x_repeated, y_repeated, z_repeated = [None] * 3

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)

while True:
  process_gravity(moons.values())
  process_velocity(moons.values())
  count += 1
  x_hash = coord_hash(moons, 'x')
  y_hash = coord_hash(moons, 'y')
  z_hash = coord_hash(moons, 'z')

  if x_hash in x_history and not x_repeated:
    x_repeated = count - x_history[x_hash]
    print('x repeated after ', x_repeated)
  
  if y_hash in y_history and not y_repeated:
    y_repeated = count - y_history[y_hash]
    print('y repeated after', count - y_history[y_hash])
  
  if z_hash in z_history and not z_repeated:
    z_repeated = count - z_history[z_hash]
    print('z repeated after', count - z_history[z_hash])

  if all([x_repeated, y_repeated, z_repeated]):
    break
    
  x_history[x_hash] = count
  y_history[y_hash] = count
  z_history[z_hash] = count

print('Answer 2', lcm(lcm(x_repeated, y_repeated), z_repeated))