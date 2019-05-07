import java.lang.Math;

class GreatCircle {

    public static double great_circle(double lon1, double lat1, double lon2, double lat2)
    {
        int radius = 3956;
        double x = Math.PI / 180.0;
        double a = (90 - lat1) * (x);
        double b = (90 - lat2) * (x);
        double theta = (lon2 - lon1) * (x);
        double c = Math.acos((Math.cos(a) * Math.cos(b)) + (Math.sin(a) * Math.sin(b) * Math.cos(theta)));
        return radius * c;
    }
    
    public static void main(String args[])
    {
        double lon1 = -72.345;
        double lat1 = 34.323;
        double lon2 = -61.823;
        double lat2 = 54.826;
    
        for (int i = 0; i <= 10000000; i++)
        {
            // System.out.println(great_circle(lon1, lat1, lon2, lat2));
            great_circle(lon1, lat1, lon2, lat2);
        }
    }



}