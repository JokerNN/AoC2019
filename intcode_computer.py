from collections import defaultdict
from typing import List, Iterable

ADD = 1
MULT = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

KNOWN_COMMANDS = {
  ADD: 1,
  MULT: 2,
  INPUT: 3,
  OUTPUT: 4,
  JUMP_IF_TRUE: 5,
  JUMP_IF_FALSE: 6,
  LESS_THAN: 7,
  EQUALS: 8,
  HALT: 99
}

PARAM_MODES = {
  'ADDRESS': 0,
  'VALUE': 1
}

class IncodeRuntimeException(Exception):
  pass

class LostInput(IncodeRuntimeException):
  pass

class UnknownCommandException(IncodeRuntimeException):
  pass

class ProgramExecutor:
  INIT = 'INIT'
  RUNNING = 'RUNNING'
  HALTED = 'HALTED'
  WAITING_FOR_INPUT = 'WAITING_FOR_INPUT'

  def __init__(
      self, 
      program: List[int], 
      inputs: List[int] = [], 
      logging_pref:dict = {
        "debug": False,
        "verbose": False
      }, 
      max_steps: int = float('inf')
    ):
    self.program = list(program)
    self.pos = 0
    self.result = []
    self.inputs = inputs
    self.debug_log = logging_pref['debug']
    self.verbose_log = logging_pref['verbose']
    self.max_steps = max_steps
    self.state = ProgramExecutor.INIT

  def debug(self, *args, **kwargs):
    if self.debug_log:
      print(*args, **kwargs)
  
  def verbose(self, *args, **kwargs):
    if self.verbose_log:
      print(*args, **kwargs)

  @staticmethod
  def command_to_string(command_int: int):
    COMMAND_TO_STRING = {
      1: 'ADD',
      2: 'MULT',
      3: 'INPUT',
      4: 'OUTPUT',
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

  def parse_op(self):
    pos = self.pos
    command = str(self.program[self.pos])
    self.verbose('Parsing command', command)
    result = {
      'command': int(command[-2:]),
      'param_modes': defaultdict(int),
      'params': {}
    }
    result['command_str'] = ProgramExecutor.command_to_string(result['command'])

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
    
    elif result['command'] == INPUT:
      if result['param_modes'][0] == PARAM_MODES['ADDRESS']:
        addr = self.program[pos + 1]
        result['params'][0] = addr
      else:
        result['params'][0] = self.program[pos + 1]
    elif result['command'] == OUTPUT:
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
    self.verbose('Current program', self.program)
    self.debug('Current pos', self.pos)
    self.verbose('Current pos', self.pos)
    self.debug('Current op', op)

    if command not in KNOWN_COMMANDS:
      raise UnknownCommandException(command)

    if command == ADD:
      self.program[op['params'][2]] = op['params'][0] + op['params'][1]
      # print(self)
      # print('Assigning addr', op['params'][2], ' result of addition ', op['params'][0], ' and ', op['params'][1])

    elif command == MULT:
      self.program[op['params'][2]] = op['params'][0] * op['params'][1]

    elif command == INPUT:
      if len(self.inputs) == 0:
        self.state = ProgramExecutor.WAITING_FOR_INPUT
      else:
        self.program[op['params'][0]] = self.inputs.pop(0)
        self.pos += 2

    elif command == OUTPUT:
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
    elif command in {OUTPUT}:
      self.pos += 2

  def add_inputs(self, *args: List[int]):
    self.inputs.extend(args)

  def run(self):
    counter = 0
    self.state = ProgramExecutor.RUNNING
    while True:
      if self.pos >= len(self.program):
        break

      if self.program[self.pos] == HALT:
        self.state = ProgramExecutor.HALTED
        break

      if counter >= self.max_steps:
        break

      if self.state == ProgramExecutor.WAITING_FOR_INPUT:
        break

      self.__execute_step()

      counter += 1
      
