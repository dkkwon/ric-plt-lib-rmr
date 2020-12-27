#! /bin/bash

set -e

make clean
rm -f receiver recevier_si sender_si sender v_sender sender receiver caller mt_receiver ex_rts_receiver
make all_si