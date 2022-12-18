import nazorand
import timeit

for _ in range(100):
    print(nazorand.randbelow(1000000))
print(timeit.timeit(lambda: nazorand.randbelow(1000000), number=10000000))
