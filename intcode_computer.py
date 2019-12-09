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
ADJUST_REL_BASE = 9
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
  ADJUST_REL_BASE: 9,
  HALT: 99
}


class IncodeRuntimeException(Exception):
  pass

class WriteToValueException(IncodeRuntimeException):
  pass

class UnknownCommandException(IncodeRuntimeException):
  pass


def moves_pointer(num):
  def factory(func):
    def wrapped_func(self, *args,**kwargs):
      res = func(self, *args, **kwargs)
      self.pos += num + 1
      return res

    return wrapped_func
    
  return factory

class ProgramExecutor:

  STATES = {
    'INIT': 'INIT',
    'RUNNING': 'RUNNING',
    'HALTED': 'HALTED',
    'WAITING_FOR_INPUT': 'WAITING_FOR_INPUT'
  }

  PARAM_MODES = {
    'ADDRESS': 0,
    'VALUE': 1,
    'RELATIVE': 2
  }

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
    # self.program = list(program)
    self.program = defaultdict(int, enumerate(program))
    self.pos = 0
    self.result = []
    self.inputs = inputs
    self.debug_log = logging_pref['debug']
    self.verbose_log = logging_pref['verbose']
    self.max_steps = max_steps
    self.state = ProgramExecutor.STATES['INIT']
    self.relative_base = 0

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

  def get_params(self, param_modes: defaultdict, param_count: int):
    params = {}
    pos = self.pos

    for idx in range(1, param_count + 1):
      if param_modes[idx - 1] == ProgramExecutor.PARAM_MODES['ADDRESS']:
        addr = self.program[pos + idx]
        params[idx - 1] = self.program[addr]
      elif param_modes[idx - 1] == ProgramExecutor.PARAM_MODES['RELATIVE']:
        addr = self.program[pos + idx] + self.relative_base
        params[idx - 1] = self.program[addr]
      else:
        params[idx - 1] = self.program[pos + idx]

    return params

    
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

    if result['command'] in {ADD, MULT, LESS_THAN, EQUALS}:
      result['params'] = self.get_params(result['param_modes'], 2)
      
      if result['param_modes'][2] == ProgramExecutor.PARAM_MODES['ADDRESS']:
        result['params'][2] = self.program[pos + 3]
      elif result['param_modes'][2] == ProgramExecutor.PARAM_MODES['RELATIVE']:
        result['params'][2] = self.program[pos + 3] + self.relative_base
      else:
        raise WriteToValueException('Seems like you try to write to constant, but it should be an address')
    
    elif result['command'] == INPUT:
      if result['param_modes'][0] == ProgramExecutor.PARAM_MODES['ADDRESS']:
        addr = self.program[pos + 1]
        result['params'][0] = addr
      elif result['param_modes'][0] == ProgramExecutor.PARAM_MODES['RELATIVE']:
        addr = self.program[pos + 1] + self.relative_base
        result['params'][0] = addr

    elif result['command'] == OUTPUT:
      result['params'] = self.get_params(result['param_modes'], 1)

    elif result['command'] in {JUMP_IF_FALSE, JUMP_IF_TRUE}:
      result['params'] = self.get_params(result['param_modes'], 2)

    elif result['command'] == ADJUST_REL_BASE:
      result['params'] = self.get_params(result['param_modes'], 1)

    return result


  @moves_pointer(3)
  def __execute_add(self, op):
    self.program[op['params'][2]] = op['params'][0] + op['params'][1]


  @moves_pointer(3)
  def __execute_mult(self, op):
    self.program[op['params'][2]] = op['params'][0] * op['params'][1]


  def __execute_input(self, op):
    if len(self.inputs) == 0:
      self.state = ProgramExecutor.STATES['WAITING_FOR_INPUT']
    else:
      self.program[op['params'][0]] = self.inputs.pop(0)
      self.pos += 2


  @moves_pointer(1)
  def __execute_output(self, op):
    self.result.append(op['params'][0])


  def __execute_jump_if_true(self, op):
    if op['params'][0] != 0:
      self.pos = op['params'][1]
    else:
      self.pos += 3


  def __execute_jump_if_false(self, op):
    if op['params'][0] == 0:
      self.pos = op['params'][1]
    else:
      self.pos += 3


  @moves_pointer(3)
  def __execute_less_than(self, op):
    res = 0
    if op['params'][0] < op['params'][1]:
      res = 1

    self.program[op['params'][2]] = res


  @moves_pointer(3)
  def __execute_equals(self, op):
    res = 0
    if op['params'][0] == op['params'][1]:
      res = 1

    self.program[op['params'][2]] = res


  @moves_pointer(1)
  def __execute_adjust_rel_base(self, op):
    self.relative_base += op['params'][0]


  def __execute_step(self):
    op = self.parse_op()
    command = op['command']
    self.verbose('Current program', self.program)
    self.debug('Current pos', self.pos)
    self.verbose('Current pos', self.pos)
    self.debug('Current op', op)

    if command not in KNOWN_COMMANDS:
      raise UnknownCommandException(command)

    op_func = {
      ADD: self.__execute_add,
      MULT: self.__execute_mult,
      INPUT: self.__execute_input,
      OUTPUT: self.__execute_output,
      JUMP_IF_TRUE: self.__execute_jump_if_true,
      JUMP_IF_FALSE: self.__execute_jump_if_false,
      LESS_THAN: self.__execute_less_than,
      EQUALS: self.__execute_equals,
      ADJUST_REL_BASE: self.__execute_adjust_rel_base
    }

    op_func[command](op)

  def add_inputs(self, *args: List[int]):
    self.inputs.extend(args)

  def run(self):
    counter = 0
    self.state = ProgramExecutor.STATES['RUNNING']
    while True:
      if self.pos >= len(self.program):
        break

      if self.program[self.pos] == HALT:
        self.state = ProgramExecutor.STATES['HALTED']
        break

      if counter >= self.max_steps:
        break

      if self.state == ProgramExecutor.STATES['WAITING_FOR_INPUT']:
        break

      self.__execute_step()

      counter += 1
      
