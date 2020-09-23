# draw-chart
drawing chart of temperature, pressure and humidity by Chart.js

## Used Device :
・Raspberry Pi 3 Model B+  
・BME280 GYBMEP  
Program for getting data from sensor(BME280 GYBMEP) is <https://github.com/SWITCHSCIENCE/samplecodes/blob/master/BME280/Python27/bme280_sample.py>  
(It was written in python2.7. So, I rewrote it in python3.)

## bme280.py
This program gets data(with executing function in program which gets data from sensor) and output it into csv files(_temp.csv, _pres.csv, _hum.csv).

## drawChart.html
In this file, script written in JavaScript get csv file and draw chart with csv data.
***
**If you want to execute this program, you must make circuit using Raspberry Pi 3 Model B+ and BME280 GVBMEP sensor.**
**Be careful about structure of directory. In this program, I estimate following directory structure. **

  /home/
      └work/
          ├bme280/
              ├data/
              └get_senrot_value/
                  
          └html-css/
