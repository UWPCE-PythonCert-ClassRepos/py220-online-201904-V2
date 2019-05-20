
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* I haven't written C in quite some time,
    forgive this code if it's a disaster */

int main ( void )
{
    static const char delim[] = ",";
    static const char filename[] = "../data/dataset.csv";
    static const char *ao = "ao";

    int found = 0;
    int _2013 = 0;
    int _2014 = 0;
    int _2015 = 0;
    int _2016 = 0;
    int _2017 = 0;
    int _2018 = 0;
    int counter = 0;
    // int total = 0;
    int last_four = 0;

    FILE *file = fopen ( filename, "r" );
    if ( file != NULL )
    {
        char line [ 256 ]; /* or other suitable maximum line size */
        while ( fgets ( line, sizeof line, file ) != NULL ) /* read a line */
        {
            char *ptr = strtok(line, delim);
            while (ptr != NULL)
            {
                if (counter == 5)
                {
                    int len = strlen(ptr);
                    // char *last_four = &ptr[len-4];
                    last_four = atoi(&ptr[len-4]);
                    if (last_four > 2012)
                    {
                        // total++;
                        if (last_four == 2013)
                            _2013++;
                        if (last_four == 2014)
                            _2014++;
                        if (last_four == 2015)
                            _2015++;
                        if (last_four == 2016)
                            _2016++;
                        if (last_four == 2017)
                            _2017++;
                        if (last_four == 2018)
                            _2018++;
                    }
                }
                else if (counter == 6)
                {
                    if (strstr(ptr, ao))
                    {
                        found++;
                    }
                    counter = -1;
                }
                counter++;
                ptr = strtok(NULL, delim);
            }
        }
        printf("ao found %d times\n", found);
        printf("2013:%d\t", _2013);
        printf("2014:%d\t", _2014);
        printf("2015:%d\t", _2015);
        printf("2016:%d\t", _2016);
        printf("2017:%d\t", _2017);
        printf("2018:%d\n", _2018);
        // printf("total:%d\n", total);
        fclose ( file );
    }
    else
    {
        perror ( filename ); /* why didn't the file open? */
    }
    return 0;
}
