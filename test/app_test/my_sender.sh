#! /bin/bash

set -e

export RMR_SEED_RT=${RMR_SEED_RT:-./app_test.rt}

# echo "2" >.verbose
# export RMR_VCTL_FILE=".verbose"

export RMR_LOG_VLEVEL="5"

./sender_si 20 1000