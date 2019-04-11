## Initial debugging

The first thing I determined was that there was an error in the source.json file.

> ```
> python3 -m pdb charges_calc.py --input=source.json --output=test_output.json 
> 
> > /home/jereamon/Documents/webDev/uwClass/py220-online-201904-V2/students/jeremy_monroe/lesson02/assignment/src/charges_calc.py(3)<module>()
> > -> '''
> > (Pdb) b 25
> > Breakpoint 1 at /home/jereamon/Documents/webDev/uwClass/py220-online-201904-V2/students/jeremy_monroe/lesson02/assignment/src/charges_calc.py:25
> > (Pdb) c
> > -> with open(filename) as file:
> > (Pdb) n
> > -> try:
> > (Pdb) n
> > -> data = json.load(file)
> > (Pdb) n
> > json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 5884 column 23 (char 130093)
> > -> data = json.load(file)
> > (Pdb) n
> > -> except:
> > (Pdb) n
> > -> exit(0)
> > (Pdb) n
> > SystemExit: 0
> ```
>
> 



First thing I added debug argument to `parse_cmd_arguments` then I debugged again just to make sure it was set properly.

```
python3 -m pdb charges_calc.py --input=source.json --output=test_output.json -d=1

> b 25
> Breakpoint 1 at /home/jereamon/Documents/webDev/uwClass/py220-online-201904-V2/students/jeremy_monroe/lesson02/assignment/src/charges_calc.py:25
> (Pdb) c/home/jereamon/Documents/webDev/uwClass/py220-online-201904-parse_cmd_arguments()
> -> return parser.parse_args()
> (Pdb) n
> --Return--
> -> return parser.parse_args()
> (Pdb) n
> -> data = load_rentals_file(args.input)
> (Pdb) pp args.debug
> '1'
```



Ok, I've implemented an error message for buggy json imports and have moved on to  `calculate_additional_fields`.  By debugging I discovered that `total_days` was resulting in a negative number of days and subsequently throwing an error when calculating `sqrt_total_price`.

This is me later. Looks like it's not `rental_end - rental_start` that's giving me negative `total_days` but errors in the json file.

```
python3 -m pdb charges_calc.py -i=source_bug_fixed.json -o=test_output.json -d=1

-> '''
(Pdb) b 59
Breakpoint 1 at charges_calc.py:59
(Pdb) c
-> print("in first line of calculate_additional_fields")
(Pdb) n
in first line of calculate_additional_fields
-> for value in data.values():
(Pdb) n
-> try:
(Pdb) n
-> rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
(Pdb) pp value['rental_start']
'6/12/17'
(Pdb) n
-> rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
(Pdb) pp rental_start
datetime.datetime(2017, 6, 12, 0, 0)
(Pdb) n
-> value['total_days'] = (rental_end - rental_start).days
(Pdb) n
-> value['total_price'] = value['total_days'] * value['price_per_day']
(Pdb) pp value['total_days']
-82
(Pdb) n
-> value['sqrt_total_price'] = math.sqrt(value['total_price'])
(Pdb) pp value['price_per_day']
31
(Pdb) pp rental_start - rental_end
datetime.timedelta(82)
(Pdb) pp (rental_start - rental_end).days
82
(Pdb) n
ValueError: math domain error
-> value['sqrt_total_price'] = math.sqrt(value['total_price'])
(Pdb) pp value['total_price']
-2542
(Pdb) n
-> except:
(Pdb) pp value['unit_cost']
*** KeyError: 'unit_cost'
(Pdb) pp value['total_price'] / value['units_rented']
-317.75
(Pdb) pp value['sqrt_total_price']
*** KeyError: 'sqrt_total_price'
(Pdb) pp value['total_price']
-2542
(Pdb) pp math.sqrt(value['total_price'])
*** ValueError: math domain error

```



I changed the for loop at the start of `calculate_additional_fields()` to `for key, value in data.items()` so that I can use the `key` in the logging message to help users find and correct errors in the json file.

```
python3 -m pdb charges_calc.py -i=source_bug_fixed.json -o=test_output.json -d=1

-> '''
(Pdb) b 59
Breakpoint 1 at charges_calc.py:59
(Pdb) c
-> print("in first line of calculate_additional_fields")
(Pdb) b 74
Breakpoint 2 at charges_calc.py:74
(Pdb) c
in first line of calculate_additional_fields
-> print(value)
(Pdb) pp key
'RNT776'
(Pdb) pp value
{'price_per_day': 14,
 'product_code': 'PRD70',
 'rental_end': '',
 'rental_start': '6/19/16',
 'units_rented': 1}
(Pdb)
```

