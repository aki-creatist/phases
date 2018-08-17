ARRAY=(a0 a1 a3 a4 a5 b0 b1 b3 b4 b5)

FILE_PATH='02_hundling/metacharacter'

mkdir ${FILE_PATH}

for item in ${ARRAY[@]}; do
    touch ${FILE_PATH}/$item.txt
    touch ${FILE_PATH}/$item.dat
done

#rm linux/02_hundling/metacharacter/*[^sh]