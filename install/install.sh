#!/bin/bash
#判断是否是root权限运行
if [ `whoami` != "root" ];then
	echo -e "\033[31mError: Please run the script with root privileges on Ubuntu, for example: sudo bash install.sh\033[0m";
	exit;
fi


this_folder=`pwd`
i_folder='';
uname='';
#获取用户名
get_uanme(){
	echo "please input your username about in /home:(input exit to exit)"
	read uname
	f="/home/$uname";
	if [ ! -d "$f/" ];then
		if [ "exit" == "$uname" ];then
			exit		
		fi
		echo "exit" == "$f"
		echo "您输入的用户名错误。"		
		$this_folder/install.sh
		exit
	fi
}
#创建路径
mk_folder(){
	echo "mkdir folder...."
	c=/home/$uname/App/Tools
	i_folder=$c;
	if [ ! -d "/home/$uname/App" ];then
		mkdir /home/$uname/App
	fi
	if [ ! -d "/home/$uname/App/Tools" ];then
		mkdir /home/$uname/App/Tools
	fi
	chown -R $uname:$uname /home/$uname/App
}
#复制程序
cp_app(){
	echo "cp App...."
	cd "$ins_folder/data"
	cp $this_folder/data/leanote-desktop $i_folder/ -r 
	cp $this_folder/data/leanote-server $i_folder/ -r
	chmod 751 $i_folder/leanote-desktop/ -R
	chmod 751 $i_folder/leanote-server/bin/run.sh
	chmod 751 $i_folder/leanote-desktop/Leanote
	chmod +x $i_folder/leanote-desktop/Leanote
	chown -R $uname:$uname /home/$uname/App
}
#安装mongodb
ins_mong(){
	echo "install mongodb...."
	apt-get install mongodb
}
#导入mongodb数据库
replace_mongodb(){
	echo "import database...."
	mongorestore -h 127.0.0.1:27017 -d leanote $this_folder/data/db
	echo "if you look like done and not worng and danger,"
	echo "Congratulations on the success of your install mongodb data"
}
#添加mongodb用户
add_mong_usr(){
	echo "add usr for mongodb...."
	mongo 127.0.0.1:27017/leanote --quiet $this_folder/data/usr.js
}
replace_file(){
	cp $this_folder/data/files $i_folder/leanote-server/ -rf
	chmod 751 $i_folder/leanote-server/files -R
	chown -R $uname:$uname /home/$uname/App
}
add_boot_start(){
	if [ ! -f "/etc/rc.local" ];then
		cp $this_folder/data/rc.local /etc
	else
		echo "$i_folder/leanote-server/bin/run.sh" >> /etc/rc.local 
	fi
	echo ""
	echo "There may be some special circumstances at last"
	echo "at the end of file have \"exit 0\",it's messign is the function is end "
	echo "you must edit this line copy to end."
	echo "do you want to change?(y/n)"
	read is_ok
	if [ "y" = "$is_ok" ];then
		gedit /etc/rc.local 
	fi
}
add_host(){
	echo "127.0.0.1 note.amolnk.top" >> /etc/hosts
}
add_desktop(){
	rm $this_folder/data/files $i_folder/leanote-desktop/leanote-desktop.desktop
	touch $this_folder/data/files $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "[Desktop Entry]" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Version = 1.0" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Name = leanote-desktop" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "GenericName = leanote-desktop" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Comment = leanote-desktop" >>  $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Exec = $i_folder/leanote-desktop/Leanote" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Icon = $i_folder/leanote-desktop/leanote.png" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Terminal = false" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Type = Application" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	echo "Categories = GNOME;Application;Network;" >> $i_folder/leanote-desktop/leanote-desktop.desktop
	cp $i_folder/leanote-desktop/leanote-desktop.desktop /home/$uname/Desktop/
}

#获取并安装程序
get_uanme
mk_folder
cp_app
ins_mong
add_desktop

##导入数据并修改
replace_mongodb
add_mong_usr
replace_file

##设置开机启动leanote并创建快捷方式

add_boot_start
add_host

echo "the install is end"
echo "you can use \"$i_folder/leanote-server/bin/run.sh\" to start leanote-server"
echo "you can open http://note.amolnk.top:3356/ for your chrome to use leanote"
echo "bye"
