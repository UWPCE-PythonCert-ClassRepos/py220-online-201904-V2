
POW = 2

def f(x):
  print(x**POW)

# def g(*args):
def g():
  global POW
  POW = 3

def main():
  function_list = ((f, (10,)), (g, (),), (f, (10,)))
  list(map(lambda x: x[0](*x[1]), function_list))

if __name__ == "__main__":
  main()