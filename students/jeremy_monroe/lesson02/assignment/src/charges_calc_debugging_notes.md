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

