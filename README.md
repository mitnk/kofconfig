KOF Keyboard Config Tool for MAME OS X
======================================

Tested on [MAME OS X Version 0.135](http://mameosx.sourceforge.net/).
Mac OS X 10.11.2

This tool is here for you to config KOF settings for multiple keyboards
(Yes, MAME support this!!!). But it support simple config for single keyboard.

All the directions KEYs are set to `WSAD` hard coded.

Install
-------

```
sudo pip install kofconfig
```

Usage
-----

```
kofconfig ABCD[XYZV] ABCD[XYZV]

A: 轻拳  B: 轻脚  C: 重拳  D: 重脚
X: A+B  Y: C+D  Z: A+B+C V: A+B+C+D

XYZV are optional.

Other Usage:
kofconfig [-p1] ABCD[XYZV]
kofconfig -p2 ABCD[XYZV]
kofconfig -p1 ABCD[XYZV] -p2 ABCD[XYZV]
```

Valid Real World Examples
-------------------------

```
$ kofconfig [-p1] JKUI
$ kofconfig [-p1] JKUIHN

$ kofconfig -p2 JKLO
$ kofconfig -p2 JKLOIU
$ kofconfig -p2 JKLOIUNH
$ kofconfig JKLOIU JKUI
$ kofconfig -p2 JKUI -p1 JKLOIU
```

You can use `-` to skip key configs:

```
$ kofconfig [-p1] JKLO-U  # Skip X, Set Y to U.
$ kofconfig -p2 JKUI--HU  # Skip X and Y, Set Z and V.
```

When you only have one keyboard, and want set P2 for **Single Play**:

```
$ kofconfig -S -p2 JKUI
```


MAME OS X does not Work on OS X 10.11?
--------------------------------------

MAME OS X --> Preference --> Video --> Render frames using: OpenGL
--> Restart MAME OS X.
