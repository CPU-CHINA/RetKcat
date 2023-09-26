import json
import pickle
import numpy as np
from rdkit import Chem
from collections import defaultdict


class process():
    
    def __init__(self,init=bool,path=''):
        self.path=''
        self.data_path='lib/' if path=='' else path
        self.seed=1220
        self.ngram=3 
        self.radius=2   #the deepth of mol fingerprints
        if init:
            self.mol_dict=defaultdict(lambda :len(self.mol_dict))
            self.seq_dict=defaultdict(lambda :len(self.seq_dict)) 
            self.seq_dict['0'*self.ngram]=0#zero represent begin and final
            self.bond_dict = defaultdict(lambda: len(self.bond_dict))
            self.fingerprint_dict = defaultdict(lambda: len(self.fingerprint_dict))
            self.edge_dict = defaultdict(lambda: len(self.edge_dict))
            
            self.seq_encodes=list()
            self.mol_encodes=list()
            self.kcat_encodes=list()
            self.adjacency=list()
            
            self.dataset=list()

            #it will load the raw data ,and process again

            with open("Kcat_combination_0918.json", "rt") as f:
                self.rawdata=json.load(f)
            with open('test.json') as f:#contain the NCS enzyme infomation
                self.test=json.load(f)
             
            for i in self.rawdata:
                
                if i["ECNumber"]=='4.2.1.78':continue   #keep NCS enzyme from repeating,remove 6
                
                seq,smiles,value=i["Sequence"],i["Smiles"],i["Value"]
                
                if '.' in smiles:continue   
                #it is mainly unbonded atom or coordinate bond with a metal atom ,previous work remove it from dataset

                if float(value)<=0:continue  
                #this work https://doi.org/10.1101/2022.11.23.517595 prepose to remove data which is apporching to 0,
                #DLkcat remove all the values below 0
                
                
                mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
                #add H to mol

                mol_encode,Adjacency=self.F_mol_encode(mol)
                if isinstance(Adjacency,bool)==True:continue

                self.mol_encodes.append(mol_encode)
                self.adjacency.append(Adjacency)
                self.seq_encodes.append(self.F_seq_encode(seq)) #
                self.kcat_encodes.append(np.log2(float(value))) #refering to DLKcat
            
            print("whole:",len(self.rawdata),'testset',len(self.test))
            self.n=len(self.rawdata)
            del self.rawdata
            
            test_dataset=[]
            
            for i in self.test:
                
                seq,smiles,value=i["Sequence"],i["Smiles"],i["Value"]
                
                mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
                mol_encode,Adjacency=self.F_mol_encode(mol)

                test_dataset.append([self.F_seq_encode(seq),mol_encode,Adjacency,np.log2(float(value))])
                
                with open(self.path+'dataset_test.pkl','wb') as f:pickle.dump(test_dataset,f)
            
            del self.test
            

            dataset=list(zip(self.seq_encodes,self.mol_encodes,self.adjacency,self.kcat_encodes))
            print("dataset:",len(dataset))
            pickle.dump(dataset,open(self.path+'dataset_train.pkl','wb'))  
            self.F_dump_data()

        else:
            self.reload(path)
            
            with open('input.json') as f:#["Sequence"],["Smiles"],["Value"]
                self.inp=json.load(f)
            
            inp_dataset=[]
            
            for i in self.inp:
                
                id,seq,smiles,value=i['id'],i["Sequence"],i["Smiles"],i["Value"]
                
                mol=Chem.AddHs(Chem.MolFromSmiles(smiles))
                mol_encode,Adjacency=self.F_mol_encode(mol)


                inp_dataset.append([id,self.F_seq_encode(seq),mol_encode,Adjacency,np.log2(float(value))])
                
            with open('input.pkl','wb') as f:pickle.dump(inp_dataset,f)

            
    def reload(self,path='lib/'):
        
        for par in ['seq_dict','mol_dict','bond_dict','edge_dict','fingerprint_dict']:
            with open(path+par+'.pkl', "rb") as f:self.__dict__[par]=pickle.load(f)

        
        

    def F_seq_encode(self,seq:str):
        encode1,encode2=[],[]
        if len(seq)%2!=0:seq='0'+seq+'00'#padding=3
        else:seq='0'+seq+'0'# padding=2
        for i in range(len(seq)):
            if i%2==0:encode1.append(self.seq_dict[seq[i:i+self.ngram]])
            else:encode2.append(self.seq_dict[seq[i:i+self.ngram]])
        return [encode1,encode2]
    
    def F_mol_encode(self,mol):
        #imitate the mol process from DLkcat
        
        atoms = [a.GetSymbol() for a in mol.GetAtoms()]   #a list contain symbol with H in the last
        adjacency = Chem.GetAdjacencyMatrix(mol)    #a martix record how atoms attach to each other
        if adjacency.shape[0]==1:return True,True

        for atom in mol.GetAromaticAtoms() : atoms[atom.GetIdx()] = atoms[atom.GetIdx()] . lower()
        #replace Aromatic atoms with lowercase (uppercase normally)
        
        i_jbond_dict = defaultdict(lambda: [])
        
        for bond in mol.GetBonds():

            i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx() #get both edge atom in a bond

            bondtype = self.bond_dict[str(bond.GetBondType())]
            
            i_jbond_dict[i].append((j, bondtype))
            i_jbond_dict[j].append((i, bondtype))
        

        if (len(atoms) == 1) or (self.radius == 0):
            fingerprints = [self.fingerprint_dict[a] for a in atoms]
        else:
            for _ in range(self.radius):
                
                """Update each node ID considering its neighboring nodes and edges
                (i.e., r-radius subgraphs or fingerprints)."""
                
                fingerprints = []
                
                for i, j_edge in i_jbond_dict.items():
                    
                    neighbors = [( atoms[j] , edge ) for j , edge in j_edge]
                    
                    fingerprint = ( atoms[i] , tuple(sorted(neighbors)) )
                    
                    try:fingerprints.append(self.fingerprint_dict[fingerprint])
                    except:
                        fingerprints.append(self.fingerprint_dict.get(fingerprint,len(self.fingerprint_dict)))
                
                atoms = fingerprints    #when first excute this line atoms has been transfer from [symbol_like] to [int_like]
                
                _i_jedge_dict = defaultdict(lambda: [])
                
                for i, j_edge in i_jbond_dict.items():
                    for j, edge in j_edge:
                        both_side = tuple(sorted((atoms[i], atoms[j])))
                        try:edge = self.edge_dict[(both_side, edge)]
                        except:edge = self.edge_dict.get((both_side, edge), len(self.edge_dict))
                        _i_jedge_dict[i].append((j, edge))
                
                i_jbond_dict = _i_jedge_dict
            
        return np.array(fingerprints),np.array(adjacency)
   
    def F_dump_data(self):
        for par in ['seq_dict','mol_dict','bond_dict','edge_dict','fingerprint_dict']:
            with open(self.data_path+par+'.pkl', "wb") as f:pickle.dump(dict(self.__dict__[par]),f)
            del self.__dict__[par]

  

        



if __name__ == '__main__':
    pro=process(init=True)
     