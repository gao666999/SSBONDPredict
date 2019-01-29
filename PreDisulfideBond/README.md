# PreDisulfideBond
A machine learning method for disulfide bond engineering site prediction based on structures

## Introduction
This folder contain source code of SSBONDPredict, includeds the following:

* SSBOND : main function for predicting the residue pairs which can form disulfide bonds after mutation
* static : configuration file for tensorflow (trained networks)
* Nepre  : a function can caculate the energy for a pdbfile, more detials are available at :[Nepre](https://github.com/gao666999/Nepre-Potential).

## Usage

### Requirement
tensorflow 1.10.0,and two packages,rmsd and Biopython
```
install rmsd: pip insatll rmsd   
install BioPython: pip insatll Biopython
```
Depending on the Python environment, the following modules might be required:
``` chardet, openpyxl ```
### Running the program
Download the code from GitHub, and rename the folder name from "SSBONDPredict-master" to "SSBONDPredict" if necessary.

```python predict.py --help```
Will display all parameters and features. 

The source path should be provided to predict.py at commandline in this format:

```
python predict.py PDB_file the_path_of_SSBONDPredict
```

* For example, to predict the residue pairs for 1crn.pdb and if the SSBONDPredict is saved in '/Users/ssb/Desktop', the commandline will be:

```
python predict.py /Users/ssb/Desktop/1crn.pdb /Users/ssb/Desktop
```
* And the prediction will show at the prompt:
```
Prediction Finished.
THRA21-ILEA25 0.580 -19.3885 -1.1023
PHEA13-CYSA26 0.577 -34.0875 -2.0208
THRA1-ALAA38 0.506 -47.1318 -0.0956
the predicted result are saved in : /Users/ssb/Desktop/SSBONDresult-1crn/
```
* You can find the result saved in the diectory shown above. The results are saved in an excel file with three data sheets, where the predictions are ordered based on probability,entropy change and energy change, respectively.

* And If you want to generate some pdb files after mutation you can use the --generate argument,for example:
```
python predict.py '/Users/ssb/Desktop/1crn.pdb' '/Users/ssb/Desktop' --generate
```
* And you will see:
```
Prediction Finished.
PHEA13-THRA30 0.980 -37.4330 -4.2077
CYSA4-ALAA9 0.980 -22.1713 -0.2770
CYSA3-TYRA44 0.956 -48.4120 -0.7053
ASNA12-THRA30 0.956 -38.1458 -2.9467
ALAA9-CYSA32 0.902 -41.2027 -0.2770
the predicted result are saved in : /Users/Desktop/SSBONDresult-1crn/
```
* And this time, in the folder of SSBONDresult-1crn,beside the excel file, you can also find one folder named mutatedpdb used to save mutated pdbfiles, all of them are named by their residue name before mutation,like this:
```
ALA-CYS.pdb ARG-ASN.pdb ASN-THR.pdb CYS-ARG.pdb CYS-TYR.pdb PHE-CYS.pdb THR-ALA.pdb
ALA-THR.pdb ARG-CYS.pdb CYS-ALA.pdb CYS-CYS.pdb ILE-ASN.pdb PHE-THR.pdb THR-CYS.pdb
```

### Application Interface
If you just want to use this Python program to predict the residue pairs that can form disulfide bonds after mutation within another program, you can write like this:
```
form PreDisulfideBond import predict
result = predict.predict_pairs('objectfile','the position of SSBONDPredict in your computer')
```
Note that this only gives the residue pairs and the associated probabilities, not the entropy/energy changes.

* For example:
```
# Make a prediction for 1crn.pdb and get the result which only contain residue pairs and probability
form PreDisulfideBond import predict
result = predict.predict_pairs('/Users/ssb/Desktop/1crn.pdb','/Users/ssb/Desktop')
```
* And you will see the result printed in your command line,like this :
```
CYSA16-CYSA26 0.997
CYSA4-ARGA10 0.997
CYSA4-CYSA32 0.982
PHEA13-THRA30 0.980
```
## Extensions
SSBONDPredict provides other utility functions:
* Give you a standard position template of Cysteine，you can find it in create_position.py
* Generate new residue information for the residue which mutated into Cysteine.You can  write like this:
```
from PreDisufideBond import generate_mutated_residue
NewResidueInformation = generate_mutated_residue.GenerateMutatedResidue(pdbfile,wildtype_name,AAsequenceNum,chainid)
```
'pdbfile' means the file you want to process, 'wildtype_name' means the residue's name before its mutation,and 'AAsequenceNum' means the sequence number of residue which will mutated into Cysteine.The return result is saved as a list which contain all the information about mutated residue.

## Copyright
SSBONDPredict is created by liulab of Beijing Compulational Science Research Center.



