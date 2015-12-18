KOF Keyboard Config Tool for MAME OS X
======================================

Tested on [MAME OS X Version 0.135](http://mameosx.sourceforge.net/).
Mac OS X 10.11.2

Install
-------

```
pip install kofconfig
```

use `sudo` if needed.

Usage
-----

```
kofconfig ABCD[XYZV] ABCD[XYZV]

A: 轻拳  B: 轻脚  C: 重拳  D: 重脚
X: A+B  Y: C+D  Z: A+B+C V: A+B+C+D

XYZV 为可选

也可以:
kofconfig -p1 ABCD[XYZV]
kofconfig -p2 ABCD[XYZV]
kofconfig -p1 ABCD[XYZV] -p2 ABCD[XYZV]
```

Valid Examples
--------------

```
$ kofconfig -p1 JKUI
$ kofconfig -p1 JKUIHN
$ kofconfig -p2 JKLO
$ kofconfig -p2 JKLOIU
$ kofconfig -p2 JKLOIUNH
$ kofconfig JKLOIU JKUI  # assume connected two keyboards
$ kofconfig -p2 JKUI -p1 JKLOIU  # assume connected two keyboards
```


MAME OS X does not Work on OS X 10.11?
--------------------------------------

MAME OS X --> Preference --> Video --> Render frames using: OpenGL
--> Restart MAME OS X.
