#!/usr/bin/env python3
"""Generate the data subpackage
"""

import codecs
import os
import re
import shutil
import sys
from operator import itemgetter

FOLDED_NAMES = {
    "Latin-1 Supplement": "Extended Latin",
    "Latin Extended-A": "Extended Latin",
    "IPA Extensions": "Extended Latin",
    "Hiragana": "Kana",
    "Katakana": "Kana",
    "Katakana Phonetic Extensions": "Kana",
}
MAX_BLOCKS = 0x2fa1f
BLOCK_RSHIFT = 4
PACKAGE_NAME = "guess_language"
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, PACKAGE_NAME, "data")
BLOCKS_PATH = os.path.join(DATA_DIR, "__init__.py")
MODELS_DIR = os.path.join(DATA_DIR, "models")
TRIGRAMS_DIR = os.path.join(SCRIPT_DIR, "trigrams")
BLOCKS_URL = "http://unicode.org/Public/UNIDATA/Blocks.txt"
BLOCKS_FN = os.path.basename(BLOCKS_URL)
ENCODING = "utf-8"


def make_data_dir():
    for dir_path in [DATA_DIR, MODELS_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        init_path = os.path.join(dir_path, "__init__.py")
        with open(init_path, "w"):
            pass


def download_file(remote, local):
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen
    from contextlib import closing

    with closing(urlopen(remote)) as inf, open(local, "wb") as ouf:
        while True:
            data = inf.read()
            if not data:
                break
            ouf.write(data)


def build_blocks():
    blocks_path = os.path.join(os.path.dirname(__file__), BLOCKS_FN)

    if not os.path.exists(blocks_path):
        download_file(BLOCKS_URL, blocks_path)

    splitter = re.compile(r"^([0-9A-F]+)\.\.([0-9A-F]+);\s*(.*)$", re.I)

    with open(BLOCKS_PATH, "a") as f:
        f.write("BLOCK_RSHIFT = {!r}\n".format(BLOCK_RSHIFT))
        f.write("BLOCKS = [None] * {:#x}\n".format(
            MAX_BLOCKS + 1 >> BLOCK_RSHIFT))

        for line in open(blocks_path):
            if line.startswith("#"):
                continue

            m = splitter.match(line)

            if not m:
                continue

            start = int(m.group(1), 16)
            end = int(m.group(2), 16) + 1
            name = m.group(3)

            if all(not chr(n).isalpha() for n in range(start, end)):
                continue

            shifted_start = start >> BLOCK_RSHIFT
            shifted_end = end >> BLOCK_RSHIFT

            assert shifted_start << BLOCK_RSHIFT == start
            assert shifted_end << BLOCK_RSHIFT == end

            if name in FOLDED_NAMES:
                comment = name
                name = FOLDED_NAMES[name]
            else:
                comment = None

            s = "BLOCKS[{:#x}:{:#x}] = [{!r}] * {:#x}{}\n".format(
                shifted_start, shifted_end, name, shifted_end - shifted_start,
                "  # " + comment if comment else ""
            )
            f.write(s)

            if end >= MAX_BLOCKS:
                break


def build_models():
    line_re = re.compile(r"^(.{3})\s+(.*)$")
    consecutive_spaces_re = re.compile(r"\s{2,}", re.U)

    for model_file in sorted(os.listdir(TRIGRAMS_DIR)):
        model_path = os.path.join(TRIGRAMS_DIR, model_file)

        if os.path.isdir(model_path):
            continue

        model = {}  # QHash<QString,int> model

        with codecs.open(model_path, encoding=ENCODING) as f:
            for n, line in enumerate(f):
                m = line_re.match(line)
                if m:
                    value = m.group(1)
                    assert not consecutive_spaces_re.search(value)
                    assert n == int(m.group(2))
                    model[value] = n
            assert len(model) == 300

        path = os.path.join(MODELS_DIR, model_file.lower() + ".py")

        with codecs.open(path, "w", encoding=ENCODING) as f:
            f.write("# -*- coding: {} -*-\nmodel = {{\n".format(ENCODING))
            for k, v in sorted(model.items(), key=itemgetter(1)):
                f.write(" {!r}: {!r},\n".format(k, v))
            f.write("}\n")


def generate_data(overwrite=False):
    if os.path.isdir(DATA_DIR):
        if overwrite:
            shutil.rmtree(DATA_DIR)
        else:
            return

    make_data_dir()
    build_blocks()
    build_models()


def setup_hook(config):
    generate_data()


if __name__ == "__main__":
    sys.exit(generate_data(overwrite=True))
