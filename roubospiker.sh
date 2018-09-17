#!/usr/bin/env bash

source ../django/env3/bin/activate

###################################
# respage 01

cd trainInJinHua

python spiker.py | python format.py | python writeToRedis.py && python redisToMysql.py