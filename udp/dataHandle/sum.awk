#!/bin/awk -f
#运行前
BEGIN {
    sum = 0
}
#运行中
{
    sum+=$2
}
#运行后
END {
    printf "TOTAL:%10d", sum
}
