import re

def has_repeated_digits(string):
  res = re.match(r'.*(.)\1.*', string)
  return bool(res)

def has_exactly_two_repeating_chars(string):

  repeats = r'(.)\1+'
  for match in re.finditer(repeats, string):
    g = match.group()
    if len(g) == 2:
      return True

  return False


def is_increasing(string):
  iter = enumerate(string)
  next(iter)
  for idx, char in iter:
    if char < string[idx - 1]:
      return False
  
  return True


def test(password):
  return all((
    has_repeated_digits(password),
    is_increasing(password)
  ))

def test2(password):
  return all((
    has_exactly_two_repeating_chars(password),
    is_increasing(password)
  ))

start = 367479 
end = 893698

counter = 0
for test_pass in range(start, end + 1):
  if test(str(test_pass)):
    counter += 1

print('Answer 1', counter)

counter = 0

for test_pass in range(start, end + 1):
  if test2(str(test_pass)):
    counter += 1

print('Answer 2', counter)

