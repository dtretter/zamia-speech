#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2014, 2018 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import codecs
import traceback
import datetime
import logging
import readline
import wave, struct, array

import numpy as np

from optparse           import OptionParser
from nltools            import misc
from nltools.tokenizer  import tokenize
from speech_lexicon     import Lexicon
from lex_edit           import LexEdit

#
# tokenize transcript, check against lexicon for OOVs
#

PROC_TITLE  = 'abook-preprocess-transcript'
LANG        = 'de'
DICT        = 'dict-de.ipa'
DEFAULT_WRT = 'data/src/dicts/wrt.csv'

#
# init terminal
#

misc.init_app (PROC_TITLE)
readline.set_history_length(1000)

#
# config
#

config = misc.load_config('.speechrc')

#
# command line
#

parser = OptionParser("usage: %prog [options] transcript.txt")

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", 
                  help="enable debug output")
parser.add_option("-w", "--wrt", dest="wrt", type = "str", default=DEFAULT_WRT,
                  help="Word replacement table, default: %s" % DEFAULT_WRT)

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) != 1:
    parser.print_usage()
    sys.exit(1)

inputfn        = args[0]
outputfn       = os.path.splitext(args[0])[0] + ".prompt"

#
# load lexicon
#

logging.info("loading lexicon...")
lex = Lexicon(DICT)
logging.info("loading lexicon...done.")

lex_edit = LexEdit(lex)

#
# load wrt
#

wrt = {}

if os.path.exists(options.wrt):
    logging.info("loading %s" % options.wrt)

    with codecs.open(options.wrt, 'r', 'utf8') as wrtf:

        for line in wrtf:
            parts = line.strip().split(';')
            if len(parts) != 2:
                continue
            wrt[parts[0]] = parts[1]

#
# linecount
#

linetot = 0
with codecs.open(inputfn, 'r', 'utf8') as inputf:
    for line in inputf:
        linetot += 1

#
# main
#

linecnt = 0

with codecs.open(inputfn, 'r', 'utf8') as inputf:
    with codecs.open(outputfn, 'w', 'utf8') as outputf:

        for line in inputf:

            line = line.strip()
            linecnt += 1

            while True:

                oovs = set()
                for token in tokenize(line, lang=LANG):
                    token = wrt[token] if token in wrt else token
                    # print repr(token)
                    if not token in lex:
                        oovs.add(token)

                out_tokens = []
                for token in tokenize(line, lang=LANG, keep_punctuation=True):
                    token = wrt[token] if token in wrt else token
                    out_tokens.append(token)

                outline = u" ".join(out_tokens)

                for t in wrt:
                    outline = outline.replace(t, wrt[t])

                if not oovs:
                    break

                oovs = sorted(list(oovs))
                oov = oovs[0]

                print
                print u"%4d/%4d: %s" % (linecnt, linetot, line)
                print u"%4d/%4d: %s" % (linecnt, linetot, outline)
                print
                print u"OOV: %s" % oov
                print
                
                resp = raw_input("E:Edit L:Lex R:Replace Q:Quit >" )

                if resp.lower() == 'q':
                    sys.exit(0)
                elif resp.lower() == 'e':
                    readline.add_history(line)
                    line = raw_input("Prompt> ")
                elif resp.lower() == 'r':
                    oov_repl = raw_input("Replacement for %s> " % oov).decode('utf8')
                    wrt[oov] = oov_repl
                    with codecs.open(options.wrt, 'w', 'utf8') as wrtf:
                        for w in sorted(wrt):
                            wrtf.write('%s;%s\n' % (w, wrt[w]))
                elif resp.lower() == 'l':
                    lex_edit.edit(oov)

            outputf.write(u"%s\n" % outline)
            outputf.flush()

print "%s written." % outputfn

