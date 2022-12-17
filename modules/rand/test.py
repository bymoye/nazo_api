import nazorand
import timeit
print(timeit.timeit(lambda: nazorand.randbelow(1000000), number=10000000))