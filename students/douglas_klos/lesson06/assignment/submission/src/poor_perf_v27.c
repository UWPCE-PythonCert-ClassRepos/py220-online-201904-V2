
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

/* I haven't written C in quite some time,
    forgive this code if it's a disaster */

// This is created to be similar to the return value of python analyze function.
typedef struct dataset
{
    clock_t start;
    clock_t end;
    unsigned long int _2013;
    unsigned long int _2014;
    unsigned long int _2015;
    unsigned long int _2016;
    unsigned long int _2017;
    unsigned long int _2018;
    unsigned long int found;
} dataset;

void reset_dataset (struct dataset *record);
void print_dataset (struct dataset *record);
dataset analyze (struct dataset *record);

int main (void)
{
    unsigned short int loop;
    dataset *record = (dataset*) malloc(sizeof(dataset));
    // Loop was used to run the program multiple times for better results on
    //   a higher-performing system.  A single test of say .5 sec was less
    //   reliable than 10 tests at 4.95 seconds.  Left at 10 for submission
    //   because C is just too quick.
    for (loop = 0; loop < 10; loop++)
    {
        printf("loop : %d\n", loop);
        reset_dataset(record);
        analyze(record);
        print_dataset(record);
    }
    free(record);
    printf("Reminder to divide your time by %d", loop);
    return 0;
}

void reset_dataset (struct dataset *record)
{
    record->found = record->start = record->end = 0;
    record->_2013 = record->_2014 = record->_2015 = 0;
    record->_2016 = record->_2017 = record->_2018 = 0;
}

void print_dataset (struct dataset *record)
{
    printf("'ao' found %lu times\n", record->found);
    printf("2013:%lu\t", record->_2013);
    printf("2014:%lu\t", record->_2014);
    printf("2015:%lu\t", record->_2015);
    printf("2016:%lu\t", record->_2016);
    printf("2017:%lu\t", record->_2017);
    printf("2018:%lu\n\n", record->_2018);
    // printf("Start time %ld\n", record->start);
    // printf("End time %ld\n", record->end);
}

dataset analyze (struct dataset *record)
{
    record->start = clock();

    static const char delim[] = ",";
    static const char filename[] = "./data/dataset.csv";
    static const char *ao = "ao";

    int counter = 0;
    int year = 0;

    FILE *file = fopen (filename, "r");
    if (file != NULL)
    {
        char line [ 256 ];
        while (fgets (line, sizeof line, file) != NULL) 
        {
            char *ptr = strtok(line, delim);
            while (ptr != NULL)
            {
                if (counter == 5)
                {
                    year = strtol(&ptr[6], NULL, 0);
                    if (year > 2012)
                    {
                        if (year == 2013) record->_2013++;
                        else if (year == 2014) record->_2014++;
                        else if (year == 2015) record->_2015++;
                        else if (year == 2016) record->_2016++;
                        else if (year == 2017) record->_2017++;
                        else if (year == 2018) record->_2018++;
                    }
                }
                else if (counter == 6)
                {
                    if (strstr(ptr, ao)) record->found++;
                    counter = -1;
                }
                counter++;
                ptr = strtok(NULL, delim);
            }
        }
        fclose (file);
    }
    record->end = clock();
    // Unused, here becuase the original python returned similar data.
    return *record;
}