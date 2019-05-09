
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
    int _2013;
    int _2014;
    int _2015;
    int _2016;
    int _2017;
    int _2018;
    int found;
} dataset;

void reset_dataset (struct dataset *record);
void print_dataset (struct dataset *record);
dataset analyze (struct dataset *record);

int main (void)
{
    for (int i = 0; i <= 10; i++)
    {
        dataset *record = (dataset*) malloc(sizeof(dataset));
        reset_dataset(record);
        analyze(record);
        printf("loop : %d\n", i);
        print_dataset(record);
        free(record);
    }
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
    printf("'ao' found %d times\n", record->found);
    printf("2013:%d\t", record->_2013);
    printf("2014:%d\t", record->_2014);
    printf("2015:%d\t", record->_2015);
    printf("2016:%d\t", record->_2016);
    printf("2017:%d\t", record->_2017);
    printf("2018:%d\n\n", record->_2018);
    // printf("Start time %ld\n", record->start);
    // printf("End time %ld\n", record->end);
}

dataset analyze (struct dataset *record)
{
    record->start = clock();

    static const char delim[] = ",";
    static const char filename[] = "./data/dataset2.csv";
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
    return *record;
}