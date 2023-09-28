# RetKcat: A novel neural network for Kcat prediction  

## Introduction  

The neural network can be divided into two parts: The first part utilizes a retentive network (RetNet) to extract protein features . This is achieved through a combination of causal masking and exponential decay along relative distances, which are combined into a single matrix. The second part employs graph convolutional networks (GCN) to capture substrate characteristics. To assess the model’s robustness, we conducted five rounds of random splitting tests.

fig

## Construction of RetKcat

In this work, we developed an end-to-end learning approach for in vitro _kcat_ value prediction by combining a GCN for substrates and a RetNet for proteins. Molecular structures which were atoms linked with chemical bonds can be naturally converted into a graph and protein sequences can also be seen as a special format of list.  

First, substrate SMILES information was loaded with RDKit v.2022.9.5 (<https://www.rdkit.org>) and then each node will update itself via its neighbor around, which can be seen as dividing atoms with its chemical environment. Moreover the adjacency of molecule was extracted, the molecule was finally represented as adjacency and a ordered node list. Then the edge information and node information has been convoluted. The final output of the GCN is a real-valued matrix M.

The protein sequence is manually split into ‘words’ which contain N amino acids. Every word is corresponding with a real number. Windows was set to limit the length of words list, every N amino acid is transferred into number and hold by windows respectively. Then the matrix maybe embedding to appointed dimension. The protein representation and molecule representation will have same dimension and will be concentrated as the input of RetNet.

The outcome of RetNet will forward an output layers, which is consisting of several Linear, then the vector will be turn to predict value via a single layer Linear.

## Data and Code Availability  

Databases including BRENDA (<https://www.brenda-enzymes.org>), SABIO-RK (<http://sabiork.h-its.org/>) was used in the evaluation of the DLKcat performance. Protein Data Bank in Europe database (<https://www.ebi.ac.uk/pdbe/>). The authors declare that all data supporting the findings and for reproducing all figures of this study are available within the paper and its Supplementary Information.

Source data are provided with this paper. To facilitate further usage, we provide all codes and detailed instruction in the GitHub repository (<https://github.com/CPU-CHINA/RetKcat>). Files and results related to simulation calculations can also be found in the GitHub repository (<https://github.com/CPU-CHINA/collation>).
