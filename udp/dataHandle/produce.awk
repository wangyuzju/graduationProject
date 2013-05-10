#!/bin/awk -f
#运行前
BEGIN {
    math = 0
    english = 0
    computer = 0
    sum = 0
}
#运行中
{
    if( $1 == "" ){
        print sum
        math += sum
        sum = 0
    }else{
        sum ++
    }
}
#运行后
END {
    print "Total: %d", math
}
