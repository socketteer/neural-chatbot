#!/bin/bash

#argument

#fix vocab size
cd util
python fix_vocab.py "$@"

#train from checkpoint
cd ../char-rnn
th train.lua -data_dir data/"$@" -init_from ../saved_policies/generic.t7 -rnn_size 600 -num_layers 3
