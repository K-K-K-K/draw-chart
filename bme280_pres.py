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

from smbus2 import SMBus
import time

bus_number = 1
i2c_address = 0x76

bus = SMBus(bus_number)

dig_temp = []
dig_pres = []
dig_hum = []

t_fine = 0.0

def writeReg(reg_address, data):
	bus.write_byte_data(i2c_address, reg_address, data)

def get_calib_param():
	calib = []

	for i in range(0x88, 0x88+24):
		calib.append(bus.read_byte_data(i2c_address, i))
	calib.append(bus.read_byte_data(i2c_address, 0xA1))
	for i in range(0xE1, 0xE1+7):
		calib.append(bus.read_byte_data(i2c_address, i))

	dig_temp.append((calib[1]  << 8) | calib[0])
	dig_temp.append((calib[3]  << 8) | calib[2])
	dig_temp.append((calib[5]  << 8) | calib[4])
	dig_pres.append((calib[7]  << 8) | calib[6])
	dig_pres.append((calib[9]  << 8) | calib[8])
	dig_pres.append((calib[11] << 8) | calib[10])
	dig_pres.append((calib[13] << 8) | calib[12])
	dig_pres.append((calib[15] << 8) | calib[14])
	dig_pres.append((calib[17] << 8) | calib[16])
	dig_pres.append((calib[19] << 8) | calib[18])
	dig_pres.append((calib[21] << 8) | calib[20])
	dig_pres.append((calib[23] << 8) | calib[22])
	dig_hum.append(  calib[24]  )
	dig_hum.append(( calib[26] << 8) | calib[25])
	dig_hum.append(  calib[27]  )
	dig_hum.append(( calib[28] << 4) | (0x0F & calib[29]))
	dig_hum.append(( calib[30] << 4) | ((calib[29] >> 4) & 0x0F))
	dig_hum.append(  calib[31]  )

	for i in range(1, 2):
		if dig_temp[i] & 0x8000:
			dig_temp[i] = (-dig_temp[i] ^ 0xFFFF) + 1

	for i in range(1, 8):
		if dig_pres[i] & 0x8000:
			dig_pres[i] = (-dig_pres[i] ^ 0xFFFF) + 1

	for i in range(0, 6):
		if dig_hum[i] & 0x8000:
			dig_pres[i] = (-dig_hum[i] ^ 0xFFFF) + 1

def readData():
	data = []
	for i in range(0xF7, 0xF7+8):
		data.append(bus.read_byte_data(i2c_address, i))
	pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
	temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
	hum_raw = (data[6] << 8) | data[7]

	#compensate_temp(temp_raw)
	#compensate_pres(pres_raw)
	#compensate_hum(hum_raw)

	#print("pres")
	t = compensate_temp(temp_raw)
	p = compensate_pres(pres_raw)
	h = compensate_hum(hum_raw)
	return p

def compensate_temp(adc_temp): # 'adc' maybe mean 'analog to degital converter'.
	global t_fine
	v1 = (adc_temp / 16384.0 - dig_temp[0] / 1024.0) * dig_temp[1]
	v2 = (adc_temp / 131072.0 - dig_temp[0] / 8192.0) * (adc_temp / 131072.0 - dig_temp[0] / 8192.0) * dig_temp[2]
	t_fine = v1 + v2
	temp = t_fine / 5120.0
	#print("temp : %-6.2f °C" % (temp))
	return "%.2f" % (temp)

def compensate_pres(adc_pres):
	global t_fine
	pres = 0.0

	v1 = (t_fine / 2.0) - 64000.0
	v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * dig_pres[5]
	v2 += ((v1 * dig_pres[4]) * 2.0)
	v2 = (v2 / 4.0) + (dig_pres[3] * 65536.0)
	v1 = (((dig_pres[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8) + ((dig_pres[1] * v1) / 2.0)) / 262144
	v1 = ((32768 + v1) * dig_pres[0]) / 32768

	if v1 == 0:
		return 0

	pres = ((1048567 - adc_pres) - (v2 / 4096)) * 3125
	if pres < 0x80000000:
		pres = (pres * 2.0) / v1
	else:
		pres = (pres / v1) * 2

	v1 = (dig_pres[8] * (((pres / 8.0) * (pres / 8.0)) / 8192.0)) / 4096
	v2 = ((pres / 4.0) * dig_pres[7]) / 8192.0
	pres += ((v1 + v2 + dig_pres[6]) / 16.0)

	#print("pres : %7.2f hPa" % (pres / 100))
	return "%7.2f" % (pres / 100)

def compensate_hum(adc_hum):
	global t_fine
	var_hum = t_fine - 76800.0
	if var_hum != 0:
		var_hum = (adc_hum - (dig_hum[3] * 64.0 + dig_hum[4] / 16384.0 * var_hum)) * (dig_hum[1] / 65536.0 * (1.0 + dig_hum[5] / 67108864.0 * var_hum * (1.0 + dig_hum[2] / 67108864.0 * var_hum)))
	else:
		print("humidity is 0")
		return 0

	var_hum *= (1.0 - dig_hum[0] * var_hum / 524288.0)
	if var_hum > 100.0:
		var_hum = 100.0
	elif var_hum < 0.0:
		var_hum = 0.0
	
	#print("hum : %6.2f " % var_hum)
	return "%.2f" % (var_hum)

def setup():
	oversmp_temp = 1
	oversmp_pres = 1
	oversmp_hum = 1
	mode = 3
	t_sb = 5
	filter = 0
	spi3w_en = 0

	ctrl_meas_reg = (oversmp_temp << 5) | (oversmp_pres << 2) | mode
	#config_reg = (t_sb << 5) | (filter << 2) | spi3w_en
	config_reg = (t_sb) | (filter << 2) | spi3w_en
	ctrl_hum_reg = oversmp_hum

	writeReg(0xF2, ctrl_hum_reg)
	writeReg(0xF4, ctrl_meas_reg)
	writeReg(0xF5, config_reg)

setup()
get_calib_param()

if __name__ == '__main__':
	try:
		readData()
	except KeyboardInterrupt:
		pass
