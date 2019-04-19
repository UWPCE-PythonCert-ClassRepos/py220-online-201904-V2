With the way our recursive function is set up if our initial argument
is not a power of two the function will continue calling itself until
the maximum recursion depth is reached.

We need to include an additional statement that will end the recursion
 if n < 2.

