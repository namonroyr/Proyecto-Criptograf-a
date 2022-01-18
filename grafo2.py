def graph2(x,y,n):
  if n == 0:
    return {((x,y),(x+1,y))}
  else:
    last = graph2(x,y,n-1)
    borde = set([segmento for segmento in last if segmento[1][0] == n])
    minimo = min([i[1][1] for i in borde])
    temp = set()
    for segmento in borde:
      head = segmento[0]
      tail = segmento[1]
      pendiente = tail[1] - head[1]
      if n%2 == 1 or tail[1] > minimo:
        temp.add((tail, (tail[0]+1,tail[1])))
      temp.add((tail, (tail[0]+1,tail[1]+pendiente+1)))
  return last.union(temp)