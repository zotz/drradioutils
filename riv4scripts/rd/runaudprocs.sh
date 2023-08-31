#!/bin/bash


for i in "/home/rd/liqs/"*
do
    "$i" &
done

wait

top
