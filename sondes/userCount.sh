#!/bin/bash
count=$(who | wc -l)
echo "${count}"