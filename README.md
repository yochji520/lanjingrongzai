容灾演练
广州切换到上海（/home/yuanwen.peng/scripts/python/rongzai3）


1.广州DB开启只读，执行脚本：
python read_only.py gz/sh

2.检查只读是否全部开启
python check_readonly.py check_gz_readonly.cfg/check_sh_readonly.cfg

检查数据库连接，并杀掉长连接
python check_database_connect.py gz/sh


3.检查上海容灾DB从库数据是否追平，执行脚本：
python check_slave_behind.py check_gz_slave_behind.cfg/check_sh_slave_behind.cfg

4.提升上海容灾DB为主实例：(得到任务ID，在第5步通过任务ID去检查)
python switchmastertodr.py gzswitch/shgzswitch

5.检查容灾DB是否全部提升成功：
python checkasyncjob.py gzswitch/shgzswitch

6.重新创建复制关系（上海主-广州备）
python changemaster.py gzchange/shchange

7.检查是否重新建立复制关系
python checkasyncjob.py gzchange/shchange

备注：
    1.配置文件gz_sid.txt 里写入需要切换的广州实例id,sh_sid.txt 里写入需要切换的上海实例
    2.配置文件all_sid.py 里以字典的方式写入广州sid：上海sid，顺序完全一致性。


上海切换到广州
同广州一样，只用更改广州执行函数即可
