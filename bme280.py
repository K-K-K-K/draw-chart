"""
MIT License

Copyright (c) 2018 Switch Science

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import bme280_temp
import bme280_pres
import bme280_hum
import datetime
import os
import time


dir_path = '/home/pi/work/bme280/data'

if not os.path.exists('/home/pi/work/bme280/data'):
	os.makedirs('/home/pi/work/bme280/data')

if __name__ == '__main__':
	while True:
		now = datetime.datetime.now()
		file_name = now.strftime('%Y%m%d')
		label = now.strftime('%H:%M')
		date = now.strftime('%Y/%m/%d %H:%M')
		csv_temp = bme280_temp.readData()
		csv_pres = bme280_pres.readData()
		csv_hum = bme280_hum.readData()

		f = open('/home/pi/work/bme280/data/' + file_name + '_temp.csv', 'a')
		print("tmp : " + date + "\t" +  csv_temp)
		f.write("'" + date + "'," + csv_temp + "\n")
		f.close() 

		f = open('/home/pi/work/bme280/data/' + file_name + '_pres.csv', 'a')
		print("prs : " + date +  "\t" + csv_pres)

		f.write("'" + date + "'," + csv_pres + "\n")
		f.close()

		f = open('/home/pi/work/bme280/data/' + file_name + '_hum.csv', 'a')
		print("hum : " + date + "\t" +  csv_hum)

		f.write("'" + date + "'," + csv_hum + "\n")
		f.close()

		time.sleep(60)
