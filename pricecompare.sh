#!/bin/bash

####################################################################################################################################
#
# Bash script that will run Python to call Amazon and eBay marketplace APIs in order to compare average pricing 
# for a user input item
# ---
# Author: R. Da Costa
# ---
# Execution: 
#   Optional Parameter: test
#   - if you enter the word "test" [no quotes needed] when executing this script,
#     it will perform all actions but will not write results to the file
# Parameters: 
#   @product    - item you wish to price
#   @budget     - used to determine whether or not the "average" price of the "product" you searched, is affordable for you
# ---
# Steps:
#   1. [Bash] Prompt user for item to search [@product]
#   2. [Bash] Run Python script with input from #1 to:
#       i. call Amazon API to get pricing data [or] no data if product is not found
#       ii. call eBay API to get pricing data [or] no data if product is not found
#   3. [Python] Use Amazon/eBay data to calculate average, high, low sale prices for product
#   4. [Python] Generate .csv with the following columns & values:
#       >> product, AmazonLowPrice, AmazonHighPrice, AmazonAvgPrice, eBayLowPrice, eBayHighPrice, eBayAvgPrice
#       >> save file as [product]-timestamp.txt
#   5. Present user with .csv results 
#       i. file path/name
#       ii. StdOut
# ---
# Assumptions:
#   1. Python3 is installed and the correct PATH is set
# 
####################################################################################################################################
# TESTING FLOAT to INT conversion
# ---------------------------------------------------------------------
# float1=1.2
# float2=1.5
# int1=$(printf %0.f "$float1")    # ${float1%%.*}
# int2=$(printf %0.f "$float2")    # ${float2%%.*}
# echo "float1:${float1}, int1:${int1}, float2:${float2}, int2:${int2}"
# exit 0

# Is this a TEST run?? 
# check command line input's first parameter $1 if it exists
tt=0
#if [ "$1" ]; then
if test $# -gt 0; then
    #  echo ">> param1: ${1}"
    if [ "$1" == "test" ]; then 
        # echo ">> SET TEST MODE"
        tt=1
    fi
fi

bot="priceBot"
product=""
echo ">> priceBot activated!"
sleep 1

echo "[${bot}]: Checking your path to Python3"
which python3
# temporarily modify the PATH to add Python to it
# export PATH="${PATH}:/usr/bin/python3"
# echo $PATH
# exit 0
echo "---------------------------------------------------------"
read -p "[${bot}]: What would you like to price? " product
echo "---------------------------------------------------------"

# echo "---------------------------------------------------------"
read -p "[${bot}]: What is your budget [Whole Number Only! No $ or .]: " budget
echo "---------------------------------------------------------"

# exit if product or budget are empty
if [[ -z "$product" || -z "$budget" ]]; then 
    echo "You must enter both product and budget values!"
    exit 1
fi

budgetInt=$(printf %0.f "$budget")
echo "Ok! Let's use your budget of $ ${budgetInt}, and compare it to what the average \"${product}\" is going for these days..."
sleep 1

# call Python script from within Bash script
# https://vividcode.io/return-value-from-python-script-to-bash-shell/
# PS C:\Users\tenne> & python c:/Users/tenne/Documents/personal/kura_labs/_scripts/kura_pricecompare/ebay.py 'iphone 11' 'false'
# python c:/Users/tenne/Documents/personal/kura_labs/_scripts/kura_pricecompare/ebay.py 'iphone 11' 'false'
# ebayRes=$("python ./ebay.py '${product}' >/dev/null 2>&1")
# ebayRes=$("eval python3 ebay.py")

# IMPORTANT! Needed to use "eval" due to usage of single quotes in the string. 
# Q. Why were single quotes necessary? 
# A. In case the user's input contained spaces. If the $parameter value is NOT encapsulated, it would be considered as separate $argv input parameters
# NOTE: "2>&1" sends the ErrOut to the StdOut. In the "ebay.py" script, we exit('with return value') to capture the return
# Return e.g. minPrice20.0,maxPrice:529.0,totPrice:1018.5,count:3,avgPrice:339.5
eBayRes=$(eval "python3 ebay.py '"$product"' 2>&1")
# echo "eBayRes: ${eBayRes}"
# echo "---------------------------------------------------------"
resErr=${eBayRes:0:5}   # ERROR:
if [ "$resErr" == "ERROR" ]; then 
    echo $eBayRes
    exit 1
fi

# split output into array
# Note that the characters in $IFS are treated individually as separators so that in the case [IFS=', '], fields may be separated by either a comma or a space 
# rather than the sequence of the two characters. Interestingly though, empty fields aren't created when comma-space appears in the input because 
# the space is treated specially.
IFS='|' read -r -a resArr <<< "$eBayRes"

minPrice="${resArr[0]/'minPrice:'/''}"
maxPrice="${resArr[1]/'maxPrice:'/''}"
avgPrice="${resArr[4]/'avgPrice:'/''}"

# echo "minPrice:${minPrice}, maxPrice:${maxPrice}, avgPrice:${avgPrice}"
# exit 0

affordable='No'
# convert prices to integers by rounding up to the nearest integer to do comparisons
# int2=$(printf %0.f "$float2")
avgPriceInt=$(printf %0.f "$avgPrice")

if [[ "$avgPriceInt" -le "$budgetInt" ]]; then 
    affordable='Yes'
fi 

echo "..."
sleep 1
echo "Here's what we found:"
echo "minPrice: ${minPrice}"
echo "maxPrice: ${maxPrice}"
echo "avgPrice: ${avgPrice}"
echo "Considering your budget of $ ${budgetInt},"
echo "Can you afford it based on 'AVERAGE' price? ${affordable}"
echo "---------------------------------------------------------"

# NOTE: bash will interpret "dollar sign + single quote + \n" [$'\n'] as a newline. Otherwise "\n" will be interpreted as part of the string
flines=""
flines="marketplace,item,minPrice,maxPrice,averagePrice,affordable?"$'\n'
flines+="eBay,${product},${minPrice},${maxPrice},${avgPrice},${affordable}"

# create and write to .csv file...
ts="$(date +'%Y-%m-%d_%H-%M-%S')"
myfilepath="ebay_pricecompare_${ts}.csv"

mydir=$(pwd)
newFilePath="${mydir}/${myfilepath}"

# writing to file...only if NOT in test mode
if [ "$tt" -lt 1 ]; then 
    sudo touch "./$myfilepath"
    sleep 1
    sudo chmod 755 "./$myfilepath"
    sleep 1

    # write to file
    sudo echo "$flines" > "$newFilePath"        # "/home/$finalUsr/$repoShortName/${finalUsr}_${repoShortName}_${ts}.txt"
    sleep 1
    echo "We've written this information: " # to a .csv file for you: "
    echo ">> file: $newFilePath"
    echo ">> data: $flines"
    echo ""
else 
    sudo echo ">> IN TEST MODE - NO FILE WRITTEN <<"
    echo ">> file: $newFilePath"
    echo ">> data: $flines"
    echo ""
fi 

exit 0