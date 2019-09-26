# SSBONDPredict
A machine learning method for disulfide bond engineering site prediction based on structures

## Summary
This program include the following functions:
(1) select/download structure files; 
(2) extract disulfide bonds and generate negative samples; 
(3) convert the coordinates to distance information; 
(4) training and testing; 
(5) disulfide bond engineering site prediction; 
(6) scripts for web-server setup.

## Introduction
SSBONDPredict is a project use a computational method based on neural network to predict residue pairs that can form disulfide bonds after cysteine mutations.The neural network was trained with atomic structures curated from the Protein Data Bank. The webserver are available at [PredDisufideBond](http://liulab.csrc.ac.cn/ssbondpre) and you can get the detail source code and usage in **PreDisulfideBond** folder.Beside predicting the residue pairs which can form disulfide bonds after mutations,it also can calculate the change of entropy and energy due to mutations. 
The predicted result will show you this: 

```CYSA4-ARGA10 0.997 -24.4450 -1.8942```  

from left to right, the columes are:
* Residue pairs that are predicted to form disulfide bonds after mutations.  
* The probability for this residue pairs to form disulfide bonds after mutations.  
* The change of entropy after mutations  
* The change of energy after mutations  

## Detailed Documentation 
see the [README](https://github.com/LiuLab-CSRC/SSBONDPredict/tree/master/PreDisulfideBond) in the Source code pages.

## Copyright  
SSBONDPredict is created by liulab of Beijing Compulational Science Research Center.
