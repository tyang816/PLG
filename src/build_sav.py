import argparse
import os
import pandas as pd
from tqdm import tqdm
from utils.utils import load_coords


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='make single mutant tsv')
    parser.add_argument("-d", "--dataset", type=str, default=None)
    parser.add_argument("--pdb_file", type=str, default=None)
    parser.add_argument("--out_file", type=str, default=None)
    parser.add_argument("--start", type=int, default=-1)
    parser.add_argument("--end", type=int, default=int(1e6))
    args = parser.parse_args()

    one_letter = {
            'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q',
            'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y',
            'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A',
            'GLY':'G', 'PRO':'P', 'CYS':'C'
            }
    AA = list(one_letter.values())

    if args.dataset is not None:
        base_dir = os.path.join(args.dataset, "DATASET")
        proteins = os.listdir(base_dir)
        for p in proteins:
            fasta_file = os.path.join(base_dir, p, f"{p}.fasta")
            pdb_file = os.path.join(base_dir, p, f"{p}.pdb")
            if os.path.exists(fasta_file):
                seq = open(fasta_file, "r").readlines()[1].strip()
            elif os.path.exists(pdb_file):
                _, seq = load_coords(pdb_file, "A")
            else:
                raise ValueError(f"Invalid file: {fasta_file} or {pdb_file}")
            data = {"mutant":[], "score":[]}
            for idx, s in tqdm(enumerate(seq)):
                if idx + 1 < args.start or idx + 1 > args.end:
                    continue
                for a in AA:
                    if a == s:
                        continue
                    data["mutant"].append(f"{s}{idx+1}{a}")
                    data["score"].append(0)

            print(f"{p} contains { len(data['mutant'])}")
            out_file = os.path.join(base_dir, p, f"{p}.csv")
            pd.DataFrame(data).to_csv(out_file, index=False)
    elif args.pdb_file is not None:
        out_dir = os.path.dirname(args.out_file)
        os.makedirs(out_dir, exist_ok=True)
        _, seq = load_coords(args.pdb_file, "A")
        data = {"mutant":[], "DMS_score":[]}
        for idx, s in tqdm(enumerate(seq)):
            if idx + 1 < args.start or idx + 1 > args.end:
                continue
            for a in AA:
                if a == s:
                    continue
                data["mutant"].append(f"{s}{idx+1}{a}")
                data["DMS_score"].append(0)
        pd.DataFrame(data).to_csv(args.out_file, index=False)