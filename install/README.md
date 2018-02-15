# leanote 一件安装程序。（测试环境：deepin4.9）

----------
因为本菜鸟经常玩坏我的deepin...而且我的主要笔记是自己搭建的leanote，所以不得不写一个一键安装程序，来节省我的时间。(自用程序，如果您想用建议你先读一下下面的介绍和源码)

----------
## 目录结构：

    .
    ├── data
    │   ├── db/     leanote服务器端备份数据库
    │   ├── files/       leanote服务器端备份文件
    │   ├── leanote-desktop/      leanote客户端
    │   ├── leanote-server/      leanote服务器端
    │   ├── rc.local       备份的启动文件
    │   └── usr.js       mongodb用户插入语句
    ├── install.sh    主程序
    └── README.md     帮助文档
    
----------
##使用方法：

 1. 将数据库导出到data/db中，
 2. 将files文件夹所有的内容放到data/files中，
 3. 将leanote服务器端程序配置文件的数据库端口、用户名密码，系统管理员，http地址改成自己所用的，
 4. 修改usr.js添加的用户名密码
 5. 以管理员身份执行index.sh,并填入所用用户名（根据用户名安装在\home\username\App\Tool下）

----------
##db文件夹：
备份了整个数据库，

----------
##files文件夹：
备份了leanote所有的图片，也就是服务端下的files文件夹
每次备份需要将图片放入这个文件里


----------
##leanote-server文件夹：
服务端程序，这里需要对conf先配置，数据库用户和密码要和usr.js相对应，而且域名要对应install.sh的第90行代码的域名。

----------
##usr.js文件：
mongodb V3对应的添加用户脚本，具体按照自己情况改，现在最高v3，也肯定是V3、






