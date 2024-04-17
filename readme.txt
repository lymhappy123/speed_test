1、安装python
sudo apt install python3

2、安装pip
sudo apt install python3-pip

3、安装依赖库
pip install python-okx
pip install websockets

4、修改test.py里的apiKey，secretKey，passphrase为自己okx账号的api信息

5、运行
nohup python3 test.py > output.log 2>&1 &

6、查看当前目录下的order_records.txt，一行代表一次下单记录，average是所有下单平均耗时

