#!/bin/awk -f
#运行前
BEGIN {
    math = 0
    english = 0
    computer = 0
    current = "g"
}
#运行中
{
    if( $1 == current ){
        math++
    }else{
        current = $1
        math = 0
    }
    printf "%s%d %s %s\n", $1,math, $2, $3
}
#运行后
END {
}
