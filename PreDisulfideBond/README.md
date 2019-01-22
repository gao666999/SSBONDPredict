# PreDisulfideBond
A machine learning method for disulfide bond engineering site prediction based on structures
## Introduction
This folder contain detail source code of SSBONDPredict, mainly included the following parts:
* Nepre is module function can caculate the energy for a pdbfile, if you want to get more detials,you can click this:[Nepre](https://github.com/gao666999/Nepre-Potential).
* SSBOND contain some specific function about predicting the residue pairs which can form disulfide bonds after mutation
* static contain some configuration file for tensorflow
## Usage
### One
Use python predict.py --help to see all the features. Usage is pretty straight forward(if you download this project from github,make sure change the project name from SSBONDPredict-master to SSBONDPredict), you can use predict.py  to predict the residue pairs directly at command line, but pay attention that predict.py must be in the diectory of PreDisulfideBond，like this:
```
# predict the residue pairs which can form disulfide bonds after mutation of 1crn.pdb
python predict.py 'objectfile' 'the diectory of SSBONDPredict in your computer'
```
* For example,predict the residue pairs for 1crn.pdb and SSBONDPredict is on the Desktop:
```
python predict.py '/User/Desktop/1crn.pdb' '/User/Desktop'
```
* And you will see:
```
finish predict.
THRA21-ILEA25 0.580 -19.3885 -1.1023
PHEA13-CYSA26 0.577 -34.0875 -2.0208
THRA1-ALAA38 0.506 -47.1318 -0.0956
the predicted result are saved in : /Users/Desktop/SSBONDresult-1crn/
```
* You can find the result saved in the diectory printed in the command line,one excel used to save the predicted result ,this excel have three sheet,there are respectively ordered by probability,entropy and energy.
* And If you want to generate some pdb files after mutation you can use the --generate argument,for example:
```
python predict.py '/User/Desktop/1crn.pdb' '/User/Desktop' --generate
```
* And you will see:
```
finish predict.
PHEA13-THRA30 0.980 -37.4330 -4.2077
CYSA4-ALAA9 0.980 -22.1713 -0.2770
CYSA3-TYRA44 0.956 -48.4120 -0.7053
ASNA12-THRA30 0.956 -38.1458 -2.9467
ALAA9-CYSA32 0.902 -41.2027 -0.2770
the predicted result are saved in : /Users/Desktop/SSBONDresult/
```
* And this time, if you come to SSBONDresult,beside that excel, you can also find one folder named mutatedpdb used to save mutated pdbfiles, all of them are named by their residue name before mutation,like this:
```
ALA-CYS.pdb ARG-ASN.pdb ASN-THR.pdb CYS-ARG.pdb CYS-TYR.pdb PHE-CYS.pdb THR-ALA.pdb
ALA-THR.pdb ARG-CYS.pdb CYS-ALA.pdb CYS-CYS.pdb ILE-ASN.pdb PHE-THR.pdb THR-CYS.pdb
```

### Two
If you just want to predict the residue pairs which can form disulfide bonds after mutation, you can write like this:
```
# calculate the result which only contain residue pairs and probability
form PreDisulfideBond import predict
result = predict.predict_pairs('objectfile','the position of SSBONDPredict in your computer')
```
* For example:
```
# Make a prediction for 1crn.pdb and get the result which only contain residue pairs and probability
form PreDisulfideBond import predict
result = predict.predict_pairs('/User/Desktop/1crn.pdb','/User/Desktop')
```
* And you will see the result printed in your command line,like this :
```
CYSA16-CYSA26 0.997
CYSA4-ARGA10 0.997
CYSA4-CYSA32 0.982
PHEA13-THRA30 0.980
```
## Extensions
SSBONDPredict also provide some useful functions:
* Give you a standard position templete of Cysteine，you can find it in create_position.py
* Generate new residue information for the residue which mutated into Cysteine.You can  write like this:
```
from PreDisufideBond import generate_mutated_residue
NewResidueInformation = generate_mutated_residue.GenerateMutatedResidue(pdbfile,wildtype_name,AAsequenceNum,chainid)
```
'pdbfile' means the file you want to process, 'wildtype_name' means the residue's name before its mutation,and 'AAsequenceNum' means the sequence number of residue which will mutated into Cysteine.The return result is saved as a list which contain all the information about mutated residue.
## Copyright
SSBONDPredict is created by liulab of Beijing Compulational Science Research Center.



