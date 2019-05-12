""" Version 14 redone for python2 """
#!/usr/bin/env python2
import datetime


def analyze(filename):
    """ Analyze input filename for some arbitray, but consistent, data """

    found = 0
    _2013 = 0
    _2014 = 0
    _2015 = 0
    _2016 = 0
    _2017 = 0
    _2018 = 0

    start = datetime.datetime.now()

    with open(filename) as csvfile:
        for line in csvfile:
            lrow = line.split(",")

            if "ao" in lrow[6]:
                found += 1

            # pylint: disable=C0122
            # Less than should be the default comparison operation
            if "2012" < lrow[5][6:]:
                if lrow[5][6:] == "2013":
                    _2013 += 1
                elif lrow[5][6:] == "2014":
                    _2014 += 1
                elif lrow[5][6:] == "2015":
                    _2015 += 1
                elif lrow[5][6:] == "2016":
                    _2016 += 1
                elif lrow[5][6:] == "2017":
                    _2017 += 1
                elif lrow[5][6:] == "2018":
                    _2018 += 1

    print("'ao' was found %d times" % found)
    print(
        "2013:%d\t " % (_2013) +
        "2014:%d\t " % (_2014) +
        "2015:%d\t " % (_2015) +
        "2016:%d\t " % (_2016) +
        "2017:%d\t " % (_2017) +
        "2018:%d\n" % (_2018)
    )

    end = datetime.datetime.now()
    return (
        start,
        end,
        {
            "2013": _2013,
            "2014": _2014,
            "2015": _2015,
            "2016": _2016,
            "2017": _2017,
            "2018": _2018,
        },
        found,
    )


if __name__ == "__main__":
    for loop in range(10):
        print("loop : %d" % loop)
        analyze("data/dataset.csv")
