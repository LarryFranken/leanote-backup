#!/bin/expect  
set timeout 30  
spawn sudo ./backup.py
expect "please input your username (because we want to change user for chown at last ): "  
send "amoln\n"  
expect "db_username(like admin)"  
send "admin\n"  
expect "db_passwd(like abc123): "  
send "abc123\n"  
expect "domain_name(like 127.0.0.1	www.baidu.com): "  
send "127.0.0.1 note.amolnk.top\n"  
interact  