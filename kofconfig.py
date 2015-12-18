#encoding=utf-8
"""
KOF Keyboard Config Tool for Mame OS X.

by mitnk (w@mitnk.com)
Dec 2015
"""
import itertools
import sys
import argparse
import xml.etree.ElementTree as ET


UP = ('JOYSTICK_UP', 'W')
DOWN = ('JOYSTICK_DOWN', 'S')
LEFT = ('JOYSTICK_LEFT', 'A')
RIGHT = ('JOYSTICK_RIGHT', 'D')

BUTTON1 = 'BUTTON1'
BUTTON2 = 'BUTTON2'
BUTTON3 = 'BUTTON3'
BUTTON4 = 'BUTTON4'


def is_unwanted_key(key):
    for k in (UP, DOWN, LEFT, RIGHT, BUTTON1, BUTTON2, BUTTON3, BUTTON4):
        if key.upper().endswith(k):
            return False
    return True


def nest_find(root, key):
    if root.tag == key:
        return root
    for item in root:
        return nest_find(item, key)


def config_player(tag, player_id, keys):
    if not keys:
        return
    key_list = []
    for c in keys:
        if c.upper() not in key_list:
            key_list.append(c.upper())
    if len(key_list) < 4 or len(key_list) > 8:
        print("Wrong Usage. use -h for help")
        exit(1)
    for item in tag.findall('port'):
        key_code = item.attrib['type']
        if is_unwanted_key(key_code):
            tag.remove(item)
        if key_code.startswith('P{}_'.format(player_id)):
            tag.remove(item)

    for DIRECT, KEY in (UP, DOWN, LEFT, RIGHT):
        key_code = 'P{}_{}'.format(player_id, DIRECT)
        element = ET.Element('port', attrib={'type': key_code})
        newseq = ET.Element('newseq', attrib={'type': 'standard'})
        text = 'KEYCODE_{}_{}'.format(player_id, KEY)
        newseq.text = text
        element.append(newseq)
        tag.append(element)

    for KEY, NUM in zip(key_list[:4], itertools.count(start=1)):
        key_code = 'P{}_BUTTON{}'.format(player_id, NUM)
        element = ET.Element('port', attrib={'type': key_code})
        newseq = ET.Element('newseq', attrib={'type': 'standard'})
        text = 'KEYCODE_{}_{}'.format(player_id, KEY)
        if NUM in (1, 2) and len(key_list) >= 5:
            X = key_list[4]
            text += ' OR KEYCODE_{}_{}'.format(player_id, X)
        if NUM in (3, 4) and len(key_list) >= 6:
            Y = key_list[5]
            text += ' OR KEYCODE_{}_{}'.format(player_id, Y)
        if NUM in (1, 2, 3) and len(key_list) >= 7:
            Z = key_list[6]
            text += ' OR KEYCODE_{}_{}'.format(player_id, Z)
        if NUM in (1, 2, 3, 4) and len(key_list) >= 8:
            V = key_list[7]
            text += ' OR KEYCODE_{}_{}'.format(player_id, V)
        newseq.text = text
        element.append(newseq)
        tag.append(element)


def config(keys_p1=None, keys_p2=None):
    tree = ET.parse('kof.cfg')
    root = tree.getroot()
    elem_input = nest_find(root, 'input')
    config_player(elem_input, 1, keys_p1)
    config_player(elem_input, 2, keys_p2)
    tree.write('output.xml')


if __name__ == '__main__':
    desc = "\nkofconfig ABCD[XYZV] ABCD[XYZV]\n\n" \
        "A: 轻拳  B: 轻脚  C: 重拳  D: 重脚\n" \
        "X: A+B  Y: C+D  Z: A+B+C V: A+B+C+D\n\n" \
        "XYZV 为可选\n\n" \
        "也可以: \n" \
        "kofconfig -p1 ABCD[XYZV]\n" \
        "kofconfig -p2 ABCD[XYZV]\n" \
        "kofconfig -p1 ABCD[XYZV] -p2 ABCD[XYZV]\n"
    if len(sys.argv) <= 2:
        print(desc)
        exit(0)
    elif len(sys.argv) == 3 and '-p' not in ''.join(sys.argv).lower():
        p1 = sys.argv[1]
        p2 = sys.argv[2]
    else:
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-p1', '-P1', type=str)
        parser.add_argument('-p2', '-P2', type=str)
        args = parser.parse_args()
        p1 = args.p1
        p2 = args.p2
    config(keys_p1=p1, keys_p2=p2)
