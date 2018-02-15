#! /usr/bin/env python3
import random
import sys
import os
import subprocess
import re
import threading
import time
import getpass  
import readline

tools_folder = "/home/amoln/App/Tools"
L_desk = tools_folder+"/leanote-desktop"
L_server = tools_folder+"/leanote-server"
gpus = sys.argv
This_folder = ""
sys_usr_name = input("please input your username (because we want to change user for chown at last ): ")
db_username = ""
db_passwd = ""
domain_name = ""

##获取当前路径
def get_folder():
	global This_folder
	cmd_sys = subprocess.Popen('pwd',stdout=subprocess.PIPE)
	cmd_res =  str(cmd_sys.stdout.read())    
	pattern = re.compile('\'(.*)\'')
	cmd_res = pattern.findall(cmd_res)
	cmd_res = str(cmd_res[0])
	cmd_res = cmd_res.replace('\\n','')
	This_folder = cmd_res
##拷贝配置文件
def cp_conf():
	os.system("rm -rf "+This_folder+"/install/data/leanote-server/conf/app.conf")
	os.system("cp "+L_server+"/conf/app.conf "+This_folder+"/install/data/leanote-server/conf/")
	pass
##获取数据库用户名密码域名
def get_database_conf():
	global db_username
	global db_passwd
	global domain_name
	#打印帮助信息
	print("\n\nBecause the program is not smart enough, you need to manually enter these parameters")
	print("Please fill in the number according to the displayed content database user name password and domain name...")
	print("Don't press Ctrl+C ,the program will terminate")
	print("The press copy is Ctrl+Shift+C")
	#获取并打印conf信息
	sss = {}
	print("\n")
	for line in open(This_folder+"/install/data/leanote-server/conf/app.conf"):
		if "site.url" in line:
			sss[0] =line.strip().replace('\n', '').replace('\t', '').replace('\r', '')
			print("   "+sss[0].replace('//', '// '))
			sss[0] = sss[0].replace("site.url","")

		if "db.username" in line:
			sss[1] =line.strip().replace('\n', '').replace('\t', '').replace('\r', '')
			print("   "+sss[1])
			sss[1] = sss[1].replace("db.username","")

		if "db.password" in line:
			sss[2] =line.strip().replace('\n', '').replace('\t', '').replace('\r', '')
			print("   "+sss[2])
			sss[2] = sss[2].replace("db.password","")
	print("\n")
	
	#提示用户输入信息
	while 1:
		db_username = input("db_username(like admin): ").replace("\t"," ").replace("  "," ").replace("  "," ")
		if db_username == "\n" or db_username == "\r" or db_username == "": 
			is_ok = input("you input domain_name is not in conf,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
			else:
				continue
		if " " in db_username: 
			is_ok = input("you input domain_name have space,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
			else:
				continue
		if db_username in sss[1]:
			break
		else:
			is_ok = input("you input db_username is not in conf,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;

	while 1:
		db_passwd = input("db_passwd(like abc123): ").replace("\t"," ").replace("  "," ").replace("  "," ")
		if db_passwd == "\n" or db_passwd == "\r" or db_passwd == "": 
			is_ok = input("you input domain_name is not in conf,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
			else:
				continue
		if " " in db_passwd: 
			is_ok = input("you input domain_name have space,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
			else:
				continue
		if db_passwd in sss[2]:
			break
		else:
			is_ok = input("you input db_passwd is not in conf,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
	
	while 1:
		domain_name = input("domain_name(like 127.0.0.1	www.baidu.com): ").replace("\t"," ").replace("  "," ").replace("  "," ")
		if domain_name == "\n" or domain_name == "\r" or domain_name == "": 
			is_ok = input("you input domain_name is not in conf or is not two string,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
			else:
				continue
		domain_name_url = domain_name.split(" ")
		if (len(domain_name_url) == 2) or (domain_name_url[1] in sss[0]) or (domain_name_url[1] == ""):
			break
		else:
			is_ok = input("you input domain_name is not in conf or is not two string,Do you want to reenter it?(y/n)")
			if is_ok == "n" or is_ok == "N":
				break;
	
##生成usr.js
def generate_usr_js():
	os.system("echo 'db.createUser({' > "+This_folder+"/install/data/usr.js")
	os.system("echo '    user: \""+db_username+"\",'  >> "+This_folder+"/install/data/usr.js")
	os.system("echo '    pwd: \""+db_passwd+"\",'  >> "+This_folder+"/install/data/usr.js")
	os.system("echo '    roles: [{role: 'dbOwner', db: 'leanote'}]'   >> "+This_folder+"/install/data/usr.js")
	os.system("echo '});'   >> "+This_folder+"/install/data/usr.js")
##修改install.sh
def update_install():
	folder = This_folder+"/install/install.sh"
	str = ""
	for line in open(folder):
		if "/etc/hosts" in line:
			str +="	echo \""+domain_name+"\" >> /etc/hosts\n"
		else:
			str +=line
	f = open(folder, 'w')
	f.write(str)
	f.close()
##备份数据库
def update_database():
	os.system("rm -rf "+This_folder+"/install/data/db")
	os.system("rm -rf "+This_folder+"/install/data/leanote")
	os.system("mongodump --host 127.0.0.1 --port 27017 -d leanote -o "+This_folder+"/install/data  > backup.log");
	os.system("mv "+This_folder+"/install/data/leanote "+This_folder+"/install/data/db")
##备份文件图片
def backup_files():
	os.system("cp -r "+L_server+"/files "+This_folder+"/install/data/")
##主函数
def main():
	get_folder()
	cp_conf()
	get_database_conf()
	generate_usr_js()
	update_install()
	update_database()
	backup_files()
	os.system("chown "+sys_usr_name+":"+sys_usr_name+" "+This_folder+"/install/  -R")
	pass



if __name__ =="__main__":
	if os.geteuid() != 0:
		print("This program must be run as root. Aborting.")
		exit()
	main()
