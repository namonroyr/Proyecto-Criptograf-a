def tipo1(x,y,n):
  paths = set()
  curr = (x,y)
  for i in range(n+1):
    next = (curr[0] + 1 , curr[1] + i)
    segment = (curr, next)
    curr = next
    paths.add(segment)
  return paths

def tipo2(x,y,n):
  type1 = tipo1(x,y,n)
  paths = set()
  for segment in type1:
    last = segment[1]
    altura = last[1]
    temp = tipo1(*last, n)
    paths = paths.union(temp)
  return paths

def tipo3(x,y,n):
  type2 = tipo2(x,y,n)
  paths = set()
  for segment in type2:
    last =  segment[1]
    pendiente = segment[1][1]-segment[0][1]
    temp = tipo1(*last,pendiente)
    paths = paths.union(temp)
  return paths

def paths(x,y,n):
  total = set()
  return ((total.union(tipo1(x,y,n))).union(tipo2(x,y,n))).union(tipo3(x,y,n))