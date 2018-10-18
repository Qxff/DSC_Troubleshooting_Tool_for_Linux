"""*******************************************************************************************************

This script is designed for "DSC Internal Cross Ping for Linux".


History:
v1.0	2018.10.10
		Initial version;

Pending function: 
1. None


Author: Jason Qin
Version: v1.0 2018.10.10

*******************************************************************************************************"""
# -*- coding: utf-8 -*-

import sys,os
import re
import copy
import time
from ssh_ping_cmd_for_Linux import ssh_onetime_ping, ssh_jump_server_cmd,ssh_jump_server_juniper_cmd,ssh_jump_server_cisco_cmd
#from SendEmail import sendemail,html_line_break
import threading
import datetime


dsc_dlb_login_ip={"HK DSC":"10.162.28.187","SG DSC":"10.163.28.132","AMS DSC":"10.160.28.221","FRT DSC":"10.161.28.249","CHI DSC":"10.166.28.201","DAL DSC":"10.164.28.190"}
hk_dsc_application_ip=['173.209.220.115','173.209.220.123']
sg_dsc_application_ip=['173.209.221.115','173.209.221.123']
ams_dsc_application_ip=['173.209.215.102','173.209.215.118']
frt_dsc_application_ip=['173.209.215.166','173.209.215.182']
chi_dsc_application_ip=['131.166.129.119','131.166.129.135']
frt_dsc_application_ip=['131.166.129.151','131.166.129.167']

dsc_pip_dic={"HK DSC":"173.209.220.115","SG DSC":"173.209.221.115","AMS DSC":"173.209.215.102","FRT DSC":"173.209.215.166","CHI DSC":"131.166.129.119","DAL DSC":"131.166.129.151"}
dsc_sip_dic={"HK DSC":"173.209.220.123","SG DSC":"173.209.221.123","AMS DSC":"173.209.215.118","FRT DSC":"173.209.215.182","CHI DSC":"131.166.129.135","DAL DSC":"131.166.129.167"}


#internal_route_ping_list={'1':['HK DSC','SG DSC'],'2':['HK DSC','AMS DSC'],'3':['HK DSC','FRT DSC'],'4':['HK DSC','CHI DSC'],'5':['HK DSC','DAL DSC'],'6':['SG DSC','AMS DSC'],
#'7':['SG DSC','FRT DSC'],'8':['SG DSC','CHI DSC'],'9':['SG DSC','DAL DSC'],'10':['AMS DSC','CHI DSC'],'11':['AMS DSC','DAL DSC'],'12':['AMS DSC','FRT DSC'],'13':['FRT DSC','CHI DSC'],
#'14':['FRT DSC','DAL DSC'],'15':['CHI DSC','DAL DSC'],}

internal_route_ping_list=(['HK DSC','SG DSC'],['HK DSC','AMS DSC'],['HK DSC','FRT DSC'],['HK DSC','CHI DSC'],['HK DSC','DAL DSC'],['SG DSC','AMS DSC'],['SG DSC','FRT DSC'],['SG DSC','CHI DSC'],['SG DSC','DAL DSC'],['AMS DSC','CHI DSC'],['AMS DSC','DAL DSC'],['AMS DSC','FRT DSC'],['FRT DSC','CHI DSC'],['FRT DSC','DAL DSC'],['CHI DSC','DAL DSC'])
#internal_route_ping_list=(['HK DSC','SG DSC'],['HK DSC','AMS DSC'],['HK DSC','FRT DSC'])

#username="g800472"
#password="Selenium666$"

username=sys.argv[1]
password=sys.argv[2]
#print(username)
#print(password)

def ssh_exe_cmd(orgin_dsc,dest_dsc):
	global username, password

	hostname=dsc_dlb_login_ip[orgin_dsc]
	cmd_ping="ping -I "+dsc_pip_dic[orgin_dsc]+' ' + dsc_pip_dic[dest_dsc]+' -s1472 -c60'
	cmd='date;'+cmd_ping
	
	#print(cmd)
	
	#ping_result_directory=os.getcwd()+r'/internal_ping_logs'
	ping_result_directory=r'/data2/TMP/tsdss/DSC_Internal_Cross_Ping_Tool/internal_ping_logs'
	if not os.path.exists(ping_result_directory):
		os.makedirs(ping_result_directory)
	
	while True:
		try:
			nowTime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
			#print(nowTime)
			results=ssh_onetime_ping(hostname,username,password,cmd)
			#flag=flag-1
			result_final=""
			for result in results:
				result_final=result_final+result
			with open("/data2/TMP/tsdss/DSC_Internal_Cross_Ping_Tool/internal_ping_logs/internal_cross_ping_log_"+nowTime+".log", 'a+') as f1:
				print('***************************************************************'+'\n'+orgin_dsc+'---->'+dest_dsc+" ping results:"+'\n'+result_final+'\n', file=f1)
				#print('***************************************************************'+'\n'+orgin_dsc+'---->'+dest_dsc+" ping results:"+'\n'+result_final+'\n')
			
			if '60 received' not in result_final:
				with open("/data2/TMP/tsdss/DSC_Internal_Cross_Ping_Tool/internal_ping_logs/internal_cross_ping_package_loss_log_"+nowTime+".log", 'a+') as f2:
					print('***************************************************************'+'\n'+orgin_dsc+'---->'+dest_dsc+" Package loss detected:"+'\n'+result_final+'\n',file=f2)
		except Exception as e:
			print(e)
			#stop_dsc_internal_cross_ping()
			#print("DSC_Internal_Cross_Ping_for_Linux stopped")
			#start_dsc_internal_cross_ping()
			#print("DSC_Internal_Cross_Ping_for_Linux started")
			pass


def start_dsc_internal_cross_ping():
	global username, password

	try:
		#all_Day_Ping_Result.show()
		for internal_route in internal_route_ping_list:
			t= threading.Thread(target=ssh_exe_cmd,args=(internal_route[0],internal_route[1]))
			t.start()
			print("thread started") 
	except:
		#all_Day_Ping_Result.close()
		QMessageBox.information(self,"Warning","Please analyze your traceroute result first(step2)",QMessageBox.Ok)
		
def stop_dsc_all_thread():
	global username, password
	
	cmd='killall -u '+ username
	print(cmd)
	ssh_onetime_ping('10.162.28.185',username,password,cmd)


def stop_dsc_internal_cross_ping():
	global username, password
	
	cmd="ps -ef | grep g800472 | grep DSC_Internal_Cross_Ping_for_Linux | awk '{print $2}' | xargs kill"
	print(cmd)
	ssh_onetime_ping('10.162.28.185',username,password,cmd)


start_dsc_internal_cross_ping() 
#stop_dsc_internal_cross_ping()
