
	
def append_csv(file_name,timestamp,path,content):
	import csv,time,os,collections
	if not os.path.exists(file_name):
		print("not exist")
		with open(file_name,'a+') as csvfile:
			print("creating file")
	LIST=[]
	#with open("/data2/TMP/tsdss/DSC_Internal_Cross_Ping_Tool/internal_ping_logs/KPI_internal_cross_ping_"+nowTime_hour+".csv", 'a+') as f1:
	#key_list=['HKG-SNG','HKG-AMS']
	key_list=['HK DSC-SG DSC','HK DSC-AMS DSC','HK DSC-FRT DSC','HK DSC-CHI DSC','HK DSC-DAL DSC','SG DSC-AMS DSC','SG DSC-FRT DSC','SG DSC-CHI DSC','SG DSC-DAL DSC','AMS DSC-CHI DSC','AMS DSC-DAL DSC','AMS DSC-FRT DSC','FRT DSC-CHI DSC','FRT DSC-DAL DSC','CHI DSC-DAL DSC']

	
	# if file is empty, add header and first row
	with open(file_name) as csvfile:
		reader =csv.reader(csvfile)
		for row in reader:
			LIST.append(row)
		print(LIST)
		print(len(LIST))
		if len(LIST)<2:
			with open(file_name, 'w',newline='') as csvfile:
				spamwriter = csv.writer(csvfile)
				string=['timestamp']
				for key in key_list:
					string.append(key)
				spamwriter.writerow(string)

				string=['temp']
				for key in key_list:
					string.append("0")
				print("string\n")
				print(string)
				spamwriter.writerow(string)
				
	new_dict = {}
	with open(file_name, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		fieldnames = next(reader)
		reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
		new_dict = [row for row in reader]
	print("new dict\n")
	print(new_dict)
	
	new_entry=collections.OrderedDict()
	match=""
	for row in new_dict:
		match="N"
		if row['timestamp']==timestamp:
			row[path]=content
			match="Y"
	if match=="N":
		#new_entry=[]
		new_entry["timestamp"]=timestamp
		for key in key_list:
			if path==key:
				new_entry[key]=content
			else:
				new_entry[key]="0"
		print("new_entry")
		print(new_entry)
		new_dict.append(new_entry)
	print("new_dict!!!\n")
	print(new_dict)
	
	
	print("write file")
	with open(file_name, 'w',newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		#Write Title
		string=['timestamp']
		for key in key_list:
			string.append(key)
		spamwriter.writerow(string)
		#Write content
		
		for row in new_dict:
			if row['timestamp']!="temp":
				string=[]
				print("row in new dict")
				print(row)
				print(row["HKG-SNG"])
				string=[]
				string.append(row["timestamp"])
				print(row)
				for key in key_list:
					string.append(row[key])
				spamwriter.writerow(string)

#append_csv("KPI_internal_cross_ping.csv","2018101015","HKG-AMS","TEST5")


