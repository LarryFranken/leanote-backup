## **leanote一键备份程序1.0 ** 
#### *此程序必须是经过leanote一键还原程序1.0安装的才能正常使用（测试环境：deepin15.5）*

---

### **下载**
    git clone https://github.com/LarryFranken/leanote-backup.git
    

--- 


### **依赖程序：**

 - leanote一键还原程序1.0（已集成）
 - apt-get install tcl
 - apt-get install expect
 - python3
 - py库没有自己装

--- 
### **使用方法一**
管理员执行 backup.py
其中会依次填入：

 - 当前用户名（以管理员用户执行无法获取当前系统用户）
 - mongodb数据库leanote的用户名和密码（因为自动化获取参数可能会导致程序出现意外情况，程序会根据conf显示对应行让用户对应输入），
 - 域名参数：是负责写入hosts文件的部分，需要用户指定参数 已空格隔开


--- 
### **使用方法二**
如果已经用过方法一，并且明白每一步需要填入什么参数，可以修改并执行auto_backup.sh
执行命令：  <span style="color:#b94a48">sudo expect auto_backup.sh </span>


            