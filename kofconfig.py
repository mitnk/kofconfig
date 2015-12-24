#encoding=utf-8
"""
KOF Keyboard Config Tool for Mame OS X.

by mitnk (w@mitnk.com)
Dec 2015
https://github.com/mitnk/kofconfig
"""
import argparse
import itertools
import os.path
import subprocess
import sys
import xml.etree.ElementTree as ET


KEYS_TO_NONE = (
    "JOYSTICKRIGHT_UP",
    "JOYSTICKRIGHT_DOWN",
    "JOYSTICKRIGHT_LEFT",
    "JOYSTICKRIGHT_RIGHT",
    "JOYSTICKLEFT_UP",
    "JOYSTICKLEFT_DOWN",
    "JOYSTICKLEFT_LEFT",
    "JOYSTICKLEFT_RIGHT",
    "UI_CANCEL",  # Preventing ESC to quit game
)

KEYS_UP = ('JOYSTICK_UP', 'W', 'UP')
KEYS_DOWN = ('JOYSTICK_DOWN', 'S', 'DOWN')
KEYS_LEFT = ('JOYSTICK_LEFT', 'A', 'LEFT')
KEYS_RIGHT = ('JOYSTICK_RIGHT', 'D', 'RIGHT')

BUTTON1 = 'BUTTON1'
BUTTON2 = 'BUTTON2'
BUTTON3 = 'BUTTON3'
BUTTON4 = 'BUTTON4'

KEYS_LIST = (
    KEYS_UP[0],
    KEYS_DOWN[0],
    KEYS_LEFT[0],
    KEYS_RIGHT[0],
    BUTTON1,
    BUTTON2,
    BUTTON3,
    BUTTON4,
)

BASE_XML = """<?xml version="1.0"?>
<mameconfig version="10">
    <system name="default"><input></input></system>
</mameconfig>"""


DST = os.path.expanduser('~/Library/Application Support/MAME OS X/Config/default.cfg')


def is_unwanted_key(key):
    for k in KEYS_LIST:
        if key.upper().endswith(k):
            return False
    return True


def nest_find(root, key):
    if root.tag == key:
        return root
    for item in root:
        return nest_find(item, key)


def config_player(tag, player_id, keys, single_play=False):
    if not keys:
        return
    key_list = []
    for c in keys:
        key_list.append(c.upper())
    if len(key_list) < 4 or len(key_list) > 8:
        print("Too few keys. See -h for details.")
        exit(1)

    for item in tag.findall('port'):
        key_code = item.attrib['type']
        if is_unwanted_key(key_code):
            tag.remove(item)
            continue
        if key_code.startswith('P{}_'.format(player_id)):
            tag.remove(item)
            continue

    kbd_id = 1 if single_play else player_id
    for DIRECT, KEY_1, KEY_2 in (KEYS_UP, KEYS_DOWN, KEYS_LEFT, KEYS_RIGHT):
        key_code = 'P{}_{}'.format(player_id, DIRECT)
        element = ET.Element('port', attrib={'type': key_code})
        newseq = ET.Element('newseq', attrib={'type': 'standard'})
        if player_id == 2 and not single_play:
            KEY = KEY_2
        else:
            KEY = KEY_1
        text = 'KEYCODE_{}_{}'.format(kbd_id, KEY)
        newseq.text = text
        element.append(newseq)
        tag.append(element)

    for KEY, NUM in zip(key_list[:4], itertools.count(start=1)):
        key_code = 'P{}_BUTTON{}'.format(player_id, NUM)
        element = ET.Element('port', attrib={'type': key_code})
        newseq = ET.Element('newseq', attrib={'type': 'standard'})
        text = 'KEYCODE_{}_{}'.format(kbd_id, KEY)
        if NUM in (1, 2) and len(key_list) >= 5 and key_list[4] != '-':
            X = key_list[4]
            text += ' OR KEYCODE_{}_{}'.format(kbd_id, X)
        if NUM in (3, 4) and len(key_list) >= 6 and key_list[5] != '-':
            Y = key_list[5]
            text += ' OR KEYCODE_{}_{}'.format(kbd_id, Y)
        if NUM in (1, 2, 3) and len(key_list) >= 7 and key_list[6] != '-':
            Z = key_list[6]
            text += ' OR KEYCODE_{}_{}'.format(kbd_id, Z)
        if NUM in (1, 2, 3, 4) and len(key_list) >= 8 and key_list[7] != '-':
            V = key_list[7]
            text += ' OR KEYCODE_{}_{}'.format(kbd_id, V)
        newseq.text = text

        element.append(newseq)
        tag.append(element)

def set_none_keys(root):
    for key in KEYS_TO_NONE:
        for player_id in (1, 2):
            if key.startswith("UI_"):
                key_code = key
            else:
                key_code = 'P{}_{}'.format(player_id, key)
            element = ET.Element('port', attrib={'type': key_code})
            newseq = ET.Element('newseq', attrib={'type': 'standard'})
            newseq.text = 'NONE'
            element.append(newseq)
            root.append(element)


def config(keys_p1=None, keys_p2=None, single_play=False):
    if os.path.exists(DST):
        tree = ET.parse(DST)
        root = tree.getroot()
    else:
        root = ET.fromstring(BASE_XML)
        tree = ET.ElementTree(root)
    elem_input = nest_find(root, 'input')
    config_player(elem_input, 1, keys_p1, single_play=single_play)
    config_player(elem_input, 2, keys_p2, single_play=single_play)
    set_none_keys(elem_input)
    tree.write(DST)
    print("Done Config! Please Restart Mame.")


def main():
    desc = "\nkofconfig ABCD[XYZV] ABCD[XYZV]\n\n" \
        "A: 轻拳  B: 轻脚  C: 重拳  D: 重脚\n" \
        "X: A+B  Y: C+D  Z: A+B+C V: A+B+C+D\n\n" \
        "XYZV 为可选\n\n" \
        "也可以: \n" \
        "kofconfig -p1 ABCD[XYZV]\n" \
        "kofconfig -p2 ABCD[XYZV]\n" \
        "kofconfig -p1 ABCD[XYZV] -p2 ABCD[XYZV]\n"

    single_play = False

    if len(sys.argv) < 2:
        print(desc)
        exit(0)
    elif len(sys.argv) == 2 and (sys.argv[1] not in ['-h', '--help']):
        p1 = sys.argv[1]
        p2 = None
        single_play = True
    elif len(sys.argv) == 3 and '-p' not in ''.join(sys.argv).lower():
        p1 = sys.argv[1]
        p2 = sys.argv[2]
    else:
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('-p1', '-P1', type=str)
        parser.add_argument('-p2', '-P2', type=str)
        parser.add_argument('-S', '-s', '--single-play', action='store_true')
        args = parser.parse_args()
        single_play = args.single_play
        p1 = args.p1
        p2 = args.p2
    config(keys_p1=p1, keys_p2=p2, single_play=single_play)


if __name__ == '__main__':
    main()
