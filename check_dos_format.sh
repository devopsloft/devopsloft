#!/bin/bash
# for use by travis
declare -i error_counter=0

for f in $(find . -type f)
do
    if [[ ! "${f}" =~  (png|db|.git|__pycache__|csv) ]]
    then    
        grep -c -m 1 $'\r$' $f 2>&1 > /dev/null
        if [ $? -eq 0 ]
        then
            echo "File $f has CRLF"
            error_counter=error_counter+1
        fi
    fi
done
echo Total errors: $error_counter
exit $error_counter
