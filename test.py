def sieve(N):
    l = list(range(2, N + 1))
    removed = set()
    for i, pivot in enumerate(l):
        if not pivot:
            continue
        removed.add(pivot)
        yield pivot
        # itération sur tous les mutiples de pivot inférieurs à N
        for i in range(pivot, N + 1, pivot):
            if i not in removed:
                l[i-2] = None
                removed.add(i)
            
print(len(list(sieve(3000000))))