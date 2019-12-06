from collections import defaultdict

ADD = 1
MULT = 2
SAVE = 3
PRINT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

KNOWN_COMMANDS = {
  ADD: 1,
  MULT: 2,
  SAVE: 3,
  PRINT: 4,
  JUMP_IF_TRUE: 5,
  JUMP_IF_FALSE: 6,
  LESS_THAN: 7,
  EQUALS: 8,
  HALT: 99
}

def command_to_string(command_int):
  COMMAND_TO_STRING = {
    1: 'ADD',
    2: 'MULT',
    3: 'SAVE',
    4: 'PRINT',
    5: 'JUMP_IF_TRUE',
    6: 'JUMP_IF_FALSE',
    7: 'LESS_THAN',
    8: 'EQUALS',
    99: 'HALT'
  }

  try:
    return COMMAND_TO_STRING[command_int]
  except KeyError:
    return 'UNKNOWN'

PARAM_MODES = {
  'ADDRESS': 0,
  'VALUE': 1
}

DEBUG_LOG = False
VERBOSE_LOG = False

def debug(*args, **kwargs):
  if DEBUG_LOG:
    print(*args, **kwargs)

def verbose(*args, **kwargs):
  if VERBOSE_LOG:
    print(*args, **kwargs)

class UnknownCommandException(Exception):
  pass

class ProgramExecutor:
  def __init__(self, program, default_input=1):
    self.program = list(program)
    self.pos = 0
    self.result = []
    self.input = default_input

  def parse_op(self):
    pos = self.pos
    command = str(self.program[self.pos])
    verbose('Parsing command', command)
    result = {
      'command': int(command[-2:]),
      'param_modes': defaultdict(int),
      'params': {}
    }
    result['command_str'] = command_to_string(result['command'])

    for idx, char in enumerate(reversed(command[:-2])):
      result['param_modes'][idx] = int(char)

    # print('Param modes', result['param_modes'])

    if result['command'] in {ADD, MULT, LESS_THAN, EQUALS}:
      for i in range(1, 3):
        if result['param_modes'][i - 1] == PARAM_MODES['ADDRESS']:
          # print('Cur pos', pos + i)
          addr = self.program[pos + i]
          # print('Value', addr)
          # print(pos)
          result['params'][i - 1] = self.program[addr]
        else:
          result['params'][i - 1] = self.program[pos + i]

      result['params'][2] = self.program[pos + 3]
    
    elif result['command'] == SAVE:
      if result['param_modes'][0] == PARAM_MODES['ADDRESS']:
        addr = self.program[pos + 1]
        result['params'][0] = addr
      else:
        result['params'][0] = self.program[pos + 1]
    elif result['command'] == PRINT:
      if result['param_modes'][0] == PARAM_MODES['ADDRESS']:
        addr = self.program[pos + 1]
        result['params'][0] = self.program[addr]
      else:
        result['params'][0] = self.program[pos + 1]

    elif result['command'] in {JUMP_IF_FALSE, JUMP_IF_TRUE}:
      for i in range(1, 3):
        if result['param_modes'][i - 1] == PARAM_MODES['ADDRESS']:
          addr = self.program[pos + i]
          result['params'][i - 1] = self.program[addr]
        else:
          result['params'][i - 1] = self.program[pos + i]

    return result

  def __execute_step(self):
    op = self.parse_op()
    command = op['command']
    verbose('Current program', self.program)
    debug('Current pos', self.pos)
    verbose('Current pos', self.pos)
    debug('Current op', op)

    if command not in KNOWN_COMMANDS:
      raise UnknownCommandException(command)

    if command == ADD:
      self.program[op['params'][2]] = op['params'][0] + op['params'][1]
      # print(self)
      # print('Assigning addr', op['params'][2], ' result of addition ', op['params'][0], ' and ', op['params'][1])

    elif command == MULT:
      self.program[op['params'][2]] = op['params'][0] * op['params'][1]

    elif command == SAVE:
      self.program[op['params'][0]] = self.input

    elif command == PRINT:
      self.result.append(op['params'][0])

    elif command == JUMP_IF_TRUE:
      if op['params'][0] != 0:
        self.pos = op['params'][1]
      else:
        self.pos += 3

    elif command == JUMP_IF_FALSE:
      if op['params'][0] == 0:
        self.pos = op['params'][1]
      else:
        self.pos += 3

    elif command == LESS_THAN:
      res = 0
      if op['params'][0] < op['params'][1]:
        res = 1

      self.program[op['params'][2]] = res

    elif command == EQUALS:
      res = 0
      if op['params'][0] == op['params'][1]:
        res = 1

      self.program[op['params'][2]] = res

    if command in {ADD, MULT, LESS_THAN, EQUALS}:
      self.pos += 4
    elif command in {SAVE, PRINT}:
      self.pos += 2

  def run(self):
    counter = 0
    while True:
      if self.pos >= len(self.program):
        break

      if self.program[self.pos] == HALT:
        break

      # counter += 1
      # if counter == 100:
      #   break

      self.__execute_step()
      # break


s_input = '3,225,1,225,6,6,1100,1,238,225,104,0,1102,79,14,225,1101,17,42,225,2,74,69,224,1001,224,-5733,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,1002,191,83,224,1001,224,-2407,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1101,18,64,225,1102,63,22,225,1101,31,91,225,1001,65,26,224,101,-44,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,101,78,13,224,101,-157,224,224,4,224,1002,223,8,223,1001,224,3,224,1,224,223,223,102,87,187,224,101,-4698,224,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,79,85,224,101,-6715,224,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1101,43,46,224,101,-89,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1101,54,12,225,1102,29,54,225,1,17,217,224,101,-37,224,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,1102,20,53,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,226,226,224,1002,223,2,223,1006,224,329,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,344,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,359,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,374,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,389,101,1,223,223,1108,226,226,224,102,2,223,223,1006,224,404,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,419,101,1,223,223,8,677,677,224,1002,223,2,223,1005,224,434,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,449,1001,223,1,223,1008,226,677,224,102,2,223,223,1006,224,464,101,1,223,223,1107,677,677,224,102,2,223,223,1006,224,479,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,494,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,524,101,1,223,223,7,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,554,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,569,1001,223,1,223,1008,677,677,224,102,2,223,223,1006,224,584,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,599,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,614,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,629,101,1,223,223,1107,677,226,224,1002,223,2,223,1006,224,644,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,659,101,1,223,223,1007,677,226,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226'
# s_input = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
inp = list(map(int, s_input.split(',')))



executor1 = ProgramExecutor(inp)
executor1.run()
print("Answer 1", executor1.result[-1])


DEBUG_LOG = False

executor2 = ProgramExecutor(inp, default_input=5)
executor2.run()
print("Answer 2", executor2.result[-1])
