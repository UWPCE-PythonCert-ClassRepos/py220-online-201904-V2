import java.lang.Math;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;


class JavaPerf {

    public static void analyze(String filename)
    {
        int found = 0;
        int _2013 = 0;
        int _2014 = 0;
        int _2015 = 0;
        int _2016 = 0;
        int _2017 = 0;
        int _2018 = 0;

        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        double start = System.currentTimeMillis();

        try {
            br = new BufferedReader(new FileReader(filename));
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] record = line.split(cvsSplitBy);
                // System.out.println(record[0]);

                if(record[6].contains("ao"))
                    found++;

                switch (Integer.parseInt(record[5].substring(record[5].length() - 4)))
                {
                    case 2013:
                        _2013++;
                        break;
                    case 2014:
                        _2014++;
                        break;
                    case 2015:
                        _2015++;
                        break;
                    case 2016:
                        _2016++;
                        break;
                    case 2017:
                        _2017++;
                        break;
                    case 2018:
                        _2018++;
                        break;
                    default:
                        break;
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } 
        System.out.println("2013: " + _2013 + "\t2014:" + _2014 + "\t2015:" + _2015 + "\t2016:" + _2016 + "\t2017:" + _2017 + "\t2018:" + _2018 + "\n");
        System.out.println("'ao' was found " + found + " times ");
        double end = System.currentTimeMillis();
    }


    public static void main(String args[])
    {
        analyze("../data/dataset.csv");

    }
}