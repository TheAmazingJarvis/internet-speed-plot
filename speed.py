#!/usr/bin/env python
import os
import csv
import sys
import speedtest
from time import gmtime, strftime
import time
import datetime
from datetime import datetime
from itertools import chain
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math
import shutil

data_path = sys.path[0]
speed_img = '{}/speed.png'.format(data_path)
speed_data = '{}/speed_data.csv'.format(data_path)



def csv_writer(up=[],down=[],ping=[],time_now = []):
	#If running only one plot write the three values to csv plus the time.
	try:			
		with open(speed_data, 'w') as output:
			output.truncate()
			writer = csv.writer(output, lineterminator='\n')
			for up,down,ping,time_hr in zip(up,down,ping,time_now):
				writer.writerow([up,down,ping,time_hr]) 	
		output.close()
	except IOError:
		print('\033[1;31m\nWARNING: Either firat run or user has no permission to write to speed_data.csv\n\033[1;m')
		
def csv_reader_single():
	try:	
		#If running only one plot read the csv, create new lists and return them.
		with open(speed_data) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			up = []
			down = []
			ping = []
			time_pm = []
		
			for row in readCSV:
				up.append(float(row[0]))
				down.append(float(row[1]))
				ping.append(float(row[2]))
				time_pm.append(str(row[3]))
	
		return up,down,ping,time_pm
		csvfile.close()
	except IOError:
		pass
	
		
def speed_test():
	for i in range (1,10):
		try:
			
			servers =[]
			# If you want to test against a specific server visit https://www.speedtestserver.com/
			# and find a server you want to test with e.g. servers = [2627] which is Perth

			s = speedtest.Speedtest()
			s.get_servers(servers)
			s.get_best_server()
			s.download()
			s.upload()	
			results_dict = s.results.dict()
		except:
			time.sleep(60)
			continue
		return results_dict
		break
	
def speed_plot():

	downspeed=[]
	upspeed=[]
	ping_time=[]
	time_now=[]
	counter = 0
	
	try:
		upspeed,downspeed,ping_time,time_now = csv_reader_single()
	except TypeError:
		print('\033[1;33m\nWARNING: First run no data available, waiting to create speed_data.csv\n\033[1;m')
	
	print("Speedtest API running....")
	print("Please Wait....")
	results_dict = speed_test()

	download_now = float(round(results_dict['download']/1000000,2))
	upload_now = float(round(results_dict['upload']/1000000,2))
	ping_now = float(round(results_dict['ping'],2))
	
	downspeed.append(float(download_now))
	upspeed.append(float(upload_now))
	ping_time.append(float(ping_now))
	# Append the values to the lists.
		
	time_now.append(time.strftime('%I %p'))
	# Append the current hour to the time_now list.

	if len(time_now) >= 25:
		del downspeed[0],upspeed[0],ping_time[0],time_now[0]
		# If it has run for a whole 24 hours, remove the first value in all of the lists 
		# to keep the x axis at 24.
		# This is becasue we only want a plot image with 24 x-axis points for a whole day.

	csv_writer(upspeed,downspeed,ping_time,time_now)

	maxdl = round(max(downspeed))
	mindl = round(min(downspeed))
	maxup = round(max(upspeed))
	minup = round(min(upspeed))
	maxping = round(max(ping_time))
	minping = round(max(ping_time))
		# Same as above but only using the lists that are used if it a single test.
	
	downspeed.reverse()
	upspeed.reverse()
	time_now.reverse()
	
	# Start of the plotting.	
	x = np.arange(1,len(time_now)+1)								
	# Set the x axis points.
	fig, ax1 = plt.subplots()
	plt.grid()
	#Choose the plot type
	ax1.plot(x, downspeed, c='#FF6347', label='Down speed')		
	# Draw the first plot line for the Down Speed API
	
	ax1.set_xlabel('{} - {}MAX\MIN - Down {}\{} - Up {}\{} - Ping {}\{} ms\n'\
	.format(results_dict['server']['name'],str(time.strftime('%d-%m-%Y\n')),\
	max(downspeed),min(downspeed),max(upspeed),min(upspeed),max(ping_time),min(ping_time)))

	ax1.set_ylabel('Down Speed', color='#FF6347')
	# Set the Y label and color
	ax1.tick_params('y', colors='#FF6347')	
	if abs(max(downspeed)-min(downspeed)) > 20:
		ax1.set_yticks(np.arange(mindl -20, maxdl +3,4))
	else:
		ax1.set_yticks(np.arange(mindl -20, maxdl +3,2))
	# If the range between maximum and minimum download speeds is < 20 I keep the Y poins of mutiples of 2
	# if > 20 step the y axis by 4 this stops all the numbers cramming up along the spine.
	
	ax1.set_xticklabels( time_now, rotation=45 )
	plt.xticks(x,time_now)								
	# Set the x labels rotation and values.
	
	
	ax2 = ax1.twinx()						## ADD another plot and same as above
	ax2.plot(x, upspeed, label='Up Speed')
	ax2.set_ylabel('Up Speed', color='b')
	ax2.tick_params('y', colors='b')
	if abs(max(upspeed)-min(upspeed)) > 20:
		ax2.set_yticks(np.arange(minup -10, maxup +13,4))
	else:
		ax2.set_yticks(np.arange(minup -10, maxup +13,2))

	ax3 = ax1.twinx()						## ADD another plot and same as above
	ax3.plot(x, ping_time, c = '#006400', linestyle=':',label='Ping')
	ax3.set_ylabel('Ping', color='#006400')
	ax3.tick_params('y', colors='#006400')
	ax3.set_yticks(np.arange(0, maxping +150,20))
	ax3.spines['right'].set_position(('axes', 1.15))
	
	
	h1, l1 = ax1.get_legend_handles_labels()
	h2, l2 = ax2.get_legend_handles_labels()
	h3, l3 = ax3.get_legend_handles_labels()
	# Set the legend labels.
	plt.legend(h1+h2+h3, l1+l2+l3, loc=1)
	# Setup the legend
	fig.tight_layout()
	fig.set_size_inches(6.4, 3.30)
	plt.gcf().subplots_adjust(bottom=0.3)

	
	try:
		plt.savefig(speed_img, dpi=100)	# save the figure to file
		plt.close()
	except IOError:
		print('\033[1;31m\nERROR: Please open as user that has permission to write to the plot image\n\033[1;m')
		
	print ('Plot Complete...\nDownload: {} Mbps\nUpload: {} Mbps\nPing: {}s\nTime: {}'\
	.format(str(downspeed[-1]),str(upspeed[-1]),str(ping_time[-1]),str(time.strftime('%I %p'))))

		
	
def main():
	speed_plot()
	now = datetime.now()
	seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
	if seconds_since_midnight > 1 and seconds_since_midnight < 100:
		try:
			timestr = str(time.strftime('%d-%m-%Y'))
			shutil.copy(speed_img, '{}/speed_logs/{}.png'.format(data_path,timestr))
		except FileNotFoundError:
			if not os.path.exists('{}/speed_logs'.format(data_path)):
				try:
					os.mkdir('{}/speed_logs'.format(data_path))
					shutil.copy(speed_img, '{}/speed_logs/{}.png'.format(data_path,timestr))
				except PermissionError:
					print('\033[1;31m\nERROR: No permission to create a new directory for the speed-plot image logs.\nPlease run as user with permissions\n\033[1;m')

hours_of_day = [3600,7200,10800,14400,18000,21600,25200,28800,32400,36000,39600,43200,46800,50400,54000,57600,61200,64800,68400,72000,75600,79200,82800,1]		

if __name__ == '__main__':

	if sys.version_info <= (3,0):
		sys.stdout.write('\033[1;31m\nSorry, requires Python 3.x, not Python 2.x\n\033[1;m')
		sys.exit(1)
	
	print ('\033[1;32m\nWaiting to run the speed plot on every hour.\033[1;m')
	while True:
		time.sleep(1)
		now = datetime.now()
		seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
		# Loop threw the list of hours of the day in seconds, if seconds since midnight is > one of these values but less than 2 seconds
		# after then run the main job.
		
		for x in hours_of_day:
			if seconds_since_midnight > x and seconds_since_midnight < x + 2:
				print ('Program ran at {} seconds since midnight\n'.format(seconds_since_midnight))
				print ('It was set to run at {} seconds since midnight\n'.format(x))
				main()
				
				print ('\033[1;32m\nWaiting to run the speed plot on every hour.\n\033[1;m')
	# If the length of the list of time values is more then 25, make a copy of the plot image,
	# then set the counter to 0 to wait for another 24 hours of testing before copying again.
