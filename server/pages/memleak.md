#Android内存泄露的定位检测
##Android内存泄露的定位检测
----------------
Android内存泄露分为java端内存泄露和native代码的内存泄露
dumpsys meminfo信息的[解析](http://developer.android.com/tools/debugging/debugging-memory.html)

dumpsys 的unknow部分文档中说和ASLR(Address space layout randomization)有关可以使用如下方法[关闭ASLR](http://askubuntu.com/questions/318315/how-can-i-temporarily-disable-aslr-address-space-layout-randomization)

一些实用的技巧，排除法
先把怀疑的代码注释掉，用来确认出现问题的部分,比如把native的实现全部改为空测试，把java部分的调用全部注释为空之后调用，这样可以进一步缩小问题出现的范围。

