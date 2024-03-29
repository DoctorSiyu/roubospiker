#!/usr/bin/env bash

source ../django/env3/bin/activate

###################################
# respage 01

cd trainInJinHua

python spiker.py | python format.py | python writeToRedis.py && python redisToMysql.py

###################################
# producthunt

cd ../productHunt
python spiker.py

###################################
# respage 02
cd ../sharebikeInJinHua
for i in {1..10}
do
    python spiker.py | python format.py | python writeToRedis.py
    if [ "$?" == "0" ]; then
        python redisToMysql.py
    fi
done

