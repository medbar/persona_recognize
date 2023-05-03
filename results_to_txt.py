import json
import os
import argparse
import re
import pandas as pd

from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infname')
    parser.add_argument('out_dir')
    args = parser.parse_args()

    out_files = defaultdict(list)
    for line in open(args.infname, 'r', encoding='utf-8'):
        f = json.loads(line)
        #print(f)
        s = f['audio_filepath'].split('.wav_o')
        if len(s) == 2 :
            orig_fname, o_d_wav = s
            o, d = map(float, o_d_wav.replace('.wav', '').split('_'))
            orig_fname = os.path.basename(orig_fname) # .replace('+', '/').replace('segmented', 'Диалоги_stt')
        elif len(s) == 1:
            orig_fname = Path(f['audio_filepath']).stem
            print(orig_fname)
            o, d = 0, -1
        else:
            raise(f"Wrong audio_filepath {f}")
        out_files[orig_fname].append({'offset': o, 'duration': d, 'text': f['pred_text']})

    # print(out_files)
    os.makedirs(args.out_dir, exist_ok=True)
    for f, data in out_files.items():
        full_f = os.path.join(args.out_dir, f"{f}.txt")
        #print(full_f, len(data), data[0:2])
        tran = " ".join(v['text'] for v in sorted(data, key=lambda x: x['offset']))
        with open(full_f, 'w', encoding='utf-8') as f:
            f.write(f"Sentence={tran}\n")

if __name__ == "__main__":
    main()

