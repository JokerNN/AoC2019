from intcode_computer import ProgramExecutor, IncodeRuntimeException
from itertools import permutations, cycle

s_input = '''3,8,1001,8,10,8,105,1,0,0,21,38,63,88,97,118,199,280,361,442,99999,3,9,1002,9,3,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,102,5,9,9,101,3,9,9,1002,9,3,9,101,3,9,9,4,9,99,3,9,1002,9,2,9,1001,9,3,9,102,3,9,9,101,2,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,2,9,9,101,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99'''
# s_input = '''3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'''
inp = list(map(int, s_input.split(',')))

max_output = 0

for amp_setting in permutations([0, 1, 2, 3, 4]):
  prev_output = 0
  # print(amp_setting)
  for phase in amp_setting:
    program = list(inp)
    amp = ProgramExecutor(program, inputs=[phase, prev_output])
    amp.run()
    prev_output = amp.result[-1]

  max_output = max(max_output, prev_output)


print('Answer 1', max_output)

# s_input = '''3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'''
inp = list(map(int, s_input.split(',')))
max_output = 0



for amp_setting in permutations(range(5, 10)):
  prev_output = 0
  phase_gen = cycle(amp_setting)

  ampA = ProgramExecutor(inp, inputs=[amp_setting[0]])
  ampB = ProgramExecutor(inp, inputs=[amp_setting[1]])
  ampC = ProgramExecutor(inp, inputs=[amp_setting[2]])
  ampD = ProgramExecutor(inp, inputs=[amp_setting[3]])
  ampE = ProgramExecutor(inp, inputs=[amp_setting[4]])

  while True:
    ampA.add_inputs(prev_output)
    ampA.run()
    prev_output = ampA.result.pop(0)
    ampB.add_inputs(prev_output)
    ampB.run()
    prev_output = ampB.result.pop(0)
    ampC.add_inputs(prev_output)
    ampC.run()
    prev_output = ampC.result.pop(0)
    ampD.add_inputs(prev_output)
    ampD.run()
    prev_output = ampD.result.pop(0)
    ampE.add_inputs(prev_output)
    ampE.run()
    prev_output = ampE.result.pop(0)

    if ampE.state == ProgramExecutor.HALTED:
      break


  max_output = max(max_output, prev_output)

print('Answer 2', max_output)