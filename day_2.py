s_input = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,6,19,23,1,23,13,27,2,6,27,31,1,5,31,35,2,10,35,39,1,6,39,43,1,13,43,47,2,47,6,51,1,51,5,55,1,55,6,59,2,59,10,63,1,63,6,67,2,67,10,71,1,71,9,75,2,75,10,79,1,79,5,83,2,10,83,87,1,87,6,91,2,9,91,95,1,95,5,99,1,5,99,103,1,103,10,107,1,9,107,111,1,6,111,115,1,115,5,119,1,10,119,123,2,6,123,127,2,127,6,131,1,131,2,135,1,10,135,0,99,2,0,14,0'

inp = list(map(int, s_input.split(',')))

program1 = list(inp)

program1[1] = 12
program1[2] = 2

pos = 0

ADD = 1
MULT = 2
HALT = 99


while True:
  if pos >= len(program1):
    break

  if program1[pos] == HALT:
    break

  pos1 = program1[pos + 1]
  pos2 = program1[pos + 2]
  pos_res = program1[pos + 3]

  if program1[pos] == ADD:
    program1[pos_res] = program1[pos1] + program1[pos2]

  if program1[pos] == MULT:
    program1[pos_res] = program1[pos1] * program1[pos2]

  pos += 4
  

print('Answer 1', program1[0])

def execute(program):
  pos = 0
  while True:
    if pos >= len(program):
      break

    if program[pos] == HALT:
      break

    pos1 = program[pos + 1]
    pos2 = program[pos + 2]
    pos_res = program[pos + 3]

    if program[pos] == ADD:
      program[pos_res] = program[pos1] + program[pos2]

    if program[pos] == MULT:
      program[pos_res] = program[pos1] * program[pos2]

    pos += 4

  return program[0]


for i in range(1000):
  for j in range(1000):
    program = list(inp)
    program[1] = i
    program[2] = j
    try:
      res = execute(program)
    except IndexError:
      continue
    # print(res)
    if res == 19690720:
      print ('Answer 2', i, j)
      break

