#!/bin/bash
count=$(who | wc -l)
echo "User Number : ${count}"