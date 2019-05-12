This is the standard run of the map filter timer

```
[venv]
[lesson06 *=]
dklos@reactor:~/git/py220-online-201904-V2/students/douglas_klos/lesson06/activity/source/scripts$ ./MapFilterTimeit.py 


map_filter_with_functions
0.0027073399996879743


map_filter_with_lambdas
0.003257278000091901


comprehension
4.059808438999426


comprehension_with_functions
9.126403174000188


comprehension_with_lambdas
12.914300358000219
```

This is after enclosing the map filter with list so that the return objects are correct.
Big difference in time when actually evaluating the filter.

```
[venv]
[lesson06 *=]
dklos@reactor:~/git/py220-online-201904-V2/students/douglas_klos/lesson06/activity/source/scripts$ ./MapFilterTimeit.py 


map_filter_with_functions
7.466245291000632


map_filter_with_lambdas
8.186630307000087


comprehension
3.7485867489995144


comprehension_with_functions
8.788292103000458


comprehension_with_lambdas
13.157778798000436
```

### Pypy3.6

```
dklos@reactor:~/git/py220-online-201904-V2/students/douglas_klos/lesson06/activity/source/scripts$ pypy ./MapFilterTimeit.py 


map_filter_with_functions
0.0025702639995870413


map_list_filter_with_functions
11.110488194000027


map_filter_with_lambdas
0.0018520230005378835


map_list_filter_with_lambdas
10.88496315500015


comprehension
0.37980406699989544


comprehension_with_functions
0.40445811199970194


comprehension_with_lambdas
0.40452489600011177
[lesson06 *=]
dklos@reactor:~/git/py220-online-201904-V2/students/douglas_klos/lesson06/activity/source/scripts$ 
```