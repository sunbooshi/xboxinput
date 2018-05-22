# xboxinput
A lib used for get Xbox gamepad input events under RaspberryPi or some other pi contains both C and Python codes, very easy to use.

Because RaspberryPi already support Xbox gamepad, XboxIput just reads from `/dev/input/eventX`  for input events.

Look into xbox.c and xboxinput.py for how to use.

------

XboxInput是一个用于在树莓派或者其它派获取Xbox手柄事件的库，包含了C和Python代码，非常容易使用。

因为树莓派已经原生支持Xbox手柄，XboxInput直接读取`/dev/input/eventX`的内容来获得按键事件。

具体使用方式请参考`xbox.c`和`xboxinput.py`中的代码。

详细的原理说明请参考[这里](http://www.sunboshi.tech/2018/05/22/xbox-gamepad/)。



