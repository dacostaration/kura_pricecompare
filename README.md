# kura_pricecompare
# Compare Your Budget to the Average Pricing for Product on eBay

Bash script that will run Python to call Amazon and eBay marketplace APIs in order to compare average pricing 
for a user input item
---
Author: R. Da Costa
---
# Execution: 
   Optional Parameter: test
   - if you enter the word "test" [no quotes needed] when executing this script,
     it will perform all actions but will not write results to the file
# Parameters: 
   @product    - item you wish to price
   @budget     - used to determine whether or not the "average" price of the "product" you searched, is affordable for you
---
# Steps:
   1. [Bash] Prompt user for item to search [@product]
   2. [Bash] Run Python script with input from #1 to:
       i. call Amazon API to get pricing data [or] no data if product is not found
       ii. call eBay API to get pricing data [or] no data if product is not found
   3. [Python] Use Amazon/eBay data to calculate average, high, low sale prices for product
   4. [Python] Generate .csv with the following columns & values:
       >> product, AmazonLowPrice, AmazonHighPrice, AmazonAvgPrice, eBayLowPrice, eBayHighPrice, eBayAvgPrice
       >> save file as [product]-timestamp.txt
   5. Present user with .csv results 
       i. file path/name
       ii. StdOut
---
# Assumptions:
   1. Python3 is installed and the correct PATH is set
