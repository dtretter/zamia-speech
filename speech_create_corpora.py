#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
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
# creates a vf-like corpora from given wav files.
# the wav files are assumed to be 16bit/16kHz Mono
# the wav files can be renamed if necessary
#
#
#

#TODO

# options "source folder" (under arc) "target folder" (corpus name) to be created
# option flag to auto transcript
# check target dir is empty
# read wav files from arc folder/<src>/[<sub>]/*
# copy / rename files to corpora/<trgt>/[<sub>]/wav/*
# create corpora/<trgt>/[<sub>]/etc/auto_prompts.txt with file ids
# auto create transcription with kaldi-model (py-kaldi-asr)