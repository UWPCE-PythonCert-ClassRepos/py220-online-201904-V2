#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

double great_circle(double lon1, double lat1, double lon2, double lat2)
{
    int radius = 3956;
    double x = M_PI / 180.0;
    double a = (90 - lat1) * (x);
    double b = (90 - lat2) * (x);
    double theta = (lon2 - lon1) * (x);
    double c = acos((cos(a) * cos(b)) + (sin(a) * sin(b) * cos(theta)));
    return radius * c;
}

void main()
{
    double lon1 = -72.345;
    double lat1 = 34.323;
    double lon2 = -61.823;
    double lat2 = 54.826;

    for (int i = 0; i <= 10000000; i++)
    {
        great_circle(lon1, lat1, lon2, lat2);
    }
}
