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
