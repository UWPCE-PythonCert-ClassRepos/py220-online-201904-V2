class Cache:
	myvar = 1

def foo():
	Cache.myvar = 2
	return Cache.myvar

print(Cache.myvar)
print(foo())