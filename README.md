# RetKcat: A novel neural network for Kcat prediction

## How to start

### Requirements

***freeze.yml*** and ***requirements.txt*** were provided in the folder "RetKcat", you can install the packages by running the following command in the folder you want to install ***RetKcat***.
The model was trained on a RTX 3090 costing average 19 Gib memory also 16 Gib on a RTX 4090, while predicting is available on a RTX 3070Ti with 6Gib on average via pretrained model state provided by us.
Amount of evidence shows that this model will have a better performance with higher hidden dimension, which is 64 in our work due to the limit of GPU memory.

### Begin

We recommend conda to construct an environment *(may need install some packages which were provided by others)*

```cmd
conda env create -f freeze.yml -n RetKcat
conda activate RetKcat
```

or try pip

```cmd
pip install -r requirements.txt
```

try to download the code with git or zip.

```cmd
git clone https://github.com/CPU-CHINA/RetKcat.git
```

and run the code in the folder **RetKcat**,

```cmd
cd RetKcat
```

put any sample you want to predict in the **RetKcat/input.json** allow the format below

```json
    {   
        "id": "['WT-4-HPAA']",
        "Smiles": "Oc1ccc(cc1)C/C=N/CCc2cc(O)c(O)cc2",
        "Sequence": "MMKMEVVFVFLMLLGTINCQKLILTGRPFLHHQGIINQVSTVTKVIHHELEVAASADDIWTVYSWPGLAKHLPDLLPGAFEKLEIIGDGGVGTILDMTFVPGEFPHEYKEKFILVDNEHRLKKVQMIEGGYLDLGVTYYMDTIHVVPTGKDSCVIKSSTEYHVKPEFVKIVEPLITTGPLAAMADAISKLVLEHKSKSNSDEIEAAIITV",
        "Value": 21.35
    }

```

and run **predict.py** ,out file will appear in the current folder,a temporary file *input.pkl* will be created and then removed after predicting.

## Introduction  

The neural network can be divided into two parts: The first part utilizes a retentive network (RetNet) to extract protein features . This is achieved through a combination of causal masking and exponential decay along relative distances, which are combined into a single matrix. The second part employs graph convolutional networks (GCN) to capture substrate characteristics.

![Construction](https://github.com/CPU-CHINA/RetKcat/blob/main/figure/construction.png)

**(A) RetKcat learning performance analysis. The
trained model is tested on the training set, and R-square is
used to measure whether the model has correctly learned
the training set. (B) NCS samples prediction test. On the test
set derived from the experiment, by comparing RetKcat with
the currently better DLKcat. (C) RetKcat schematic diagram.
RetKcat is composed of two parts, GCN is used to read molecular information, and RetNet is used to read protein information.**

## Construction of RetKcat

In this work, we developed an end-to-end learning approach for in vitro *kcat* value prediction by combining a GCN for substrates and a RetNet for proteins. Molecular structures which were atoms linked with chemical bonds can be naturally converted into a graph and protein sequences can also be seen as a special format of list.  

First, substrate SMILES information was loaded with RDKit v.2022.9.5 (<https://www.rdkit.org>) and then each node will update itself via its neighbor around, which can be seen as dividing atoms with its chemical environment. Moreover the adjacency of molecule was extracted, the molecule was finally represented as adjacency and a ordered node list. Then the edge information and node information has been convoluted. The final output of the GCN is a real-valued matrix M.

The protein sequence is manually split into ‘words’ which contain N amino acids. Every word is corresponding with a real number. Windows was set to limit the length of words list, every N amino acid is transferred into number and hold by windows respectively. Then the matrix maybe embedding to appointed dimension. The protein representation and molecule representation will have same dimension and will be concentrated as the input of RetNet.

The outcome of RetNet will forward an output layers, which is consisting of several Linear, then the vector will be turn to predict value via a single layer Linear.

## Data and Code Availability  

Databases including BRENDA (<https://www.brenda-enzymes.org>), SABIO-RK (<http://sabiork.h-its.org/>) was used in the evaluation of the DLKcat performance. Protein Data Bank in Europe database (<https://www.ebi.ac.uk/pdbe/>).

Source data are provided with this paper. To facilitate further usage, we provide all codes and detailed instruction in the GitHub repository (<https://github.com/CPU-CHINA/RetKcat>). Files and results related to simulation calculations can also be found in the GitHub repository (<https://github.com/CPU-CHINA/collation>).
