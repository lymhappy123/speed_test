1、安装python
sudo apt install python3

2、安装pip
sudo apt install python3-pip

3、安装依赖库
pip install python-okx
pip install websockets

4、修改test.py里的apiKey，secretKey，passphrase为自己okx账号的api信息

5、运行，大约会运行5小时后结束。
nohup python3 test.py > output.log 2>&1 &

6、查看当前目录下的order_records.txt，一行代表一次下单记录
内容大体如下，最前面是测试下单的次数，最后test end行是结论，average是平均延时毫秒数，min是最小延迟的毫秒数，max是最大延迟的毫秒数。
1   orderId: 1713750138938706300, orderTime: 1713750139379570400, openTime: 1713750139461543800,  reqCost:440.8641ms, cost_time:522.8375ms, average:522.8375ms, min:522.8375ms, max:522.8375ms
2   orderId: 1713750159392331800, orderTime: 1713750159816161600, openTime: 1713750159900091500,  reqCost:423.8298ms, cost_time:507.7597ms, average:515.2986ms, min:507.7597ms, max:522.8375ms
3   orderId: 1713750179841955700, orderTime: 1713750180294850000, openTime: 1713750180385727800,  reqCost:452.8943ms, cost_time:543.7721ms, average:524.7897666666667ms, min:507.7597ms, max:543.7721ms
4   orderId: 1713750200291706900, orderTime: 1713750200733508200, openTime: 1713750200817438000,  reqCost:441.8013ms, cost_time:525.7311ms, average:525.0251ms, min:507.7597ms, max:543.7721ms
5   orderId: 1713750220750803900, orderTime: 1713750221223339500, openTime: 1713750221315589300,  reqCost:472.5356ms, cost_time:564.7854ms, average:532.97716ms, min:507.7597ms, max:564.7854ms
6   orderId: 1713750241236727000, orderTime: 1713750241737669100, openTime: 1713750241819765300,  reqCost:500.9421ms, cost_time:583.0383ms, average:541.3206833333334ms, min:507.7597ms, max:583.0383ms
7   orderId: 1713750261764666400, orderTime: 1713750262190926600, openTime: 1713750262247262500,  reqCost:426.2602ms, cost_time:482.5961ms, average:532.9314571428571ms, min:482.5961ms, max:583.0383ms
8   orderId: 1713750282205947400, orderTime: 1713750282591801700, openTime: 1713750282685300800,  reqCost:385.8543ms, cost_time:479.3534ms, average:526.2342ms, min:479.3534ms, max:583.0383ms
9   orderId: 1713750302599328700, orderTime: 1713750302985163100, openTime: 1713750303071898600,  reqCost:385.8344ms, cost_time:472.5699ms, average:520.2715000000001ms, min:472.5699ms, max:583.0383ms
10   orderId: 1713750322996908300, orderTime: 1713750323365256800, openTime: 1713750323471323000,  reqCost:368.3485ms, cost_time:474.4147ms, average:515.68582ms, min:472.5699ms, max:583.0383ms
test end,   average:515.68582ms, min:472.5699ms, max:583.0383ms

7、平均延时average最好在50ms左右，最大延时max不要超过75ms。

