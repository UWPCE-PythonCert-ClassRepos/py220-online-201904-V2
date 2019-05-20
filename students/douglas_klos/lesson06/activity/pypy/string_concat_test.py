#  Mastering Python High Performance
#  http://proquest.safaribooksonline.com.ezproxy.spl.org:2048/book/programming/python/9781783989300/pypy/ch06lvl2sec51_html?uicode=spl


from io import StringIO

TIMES = 100000

#  Normal Python style string concatenation
init = time.process_time()
value = ''
for i in range(TIMES):
    value += str(i)
print("Concatenation: %s" % (time.process_time() - init))

#  cStringIO concatenation
init = time.process_time()
value = StringIO()
for i in range(TIMES):
    value.write(str(i))
print("StringIO: %s" % (time.process_time() - init))

#  List concatenation
init = time.process_time()
value = []
for i in range(TIMES):
    value.append(str(i))
finalValue = ''.join(value)
print("List: %s" % (time.process_time() - init))
