import json
import os
import argparse

from collections import defaultdict
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infname')
    parser.add_argument('out_dir')
    args = parser.parse_args()

    out_files = defaultdict(list)
    for line in open(args.infname, 'r', encoding='utf-8'):
        f = json.loads(line)
        print(f)
        orig_fname, o_d_wav = f['audio_filepath'].split('.wav_o')
        o, d = map(float, o_d_wav.replace('.wav', '').split('_'))

        original_file_name = orig_fname.replace('+', '/').replace('segmented', 'Диалоги_stt')
        out_files[original_file_name].append({'offset': o, 'duration': d, 'text': f['pred_text']})

    print(out_files)
    for f, data in out_files.items():
        print(f)
        full_f = os.path.join(args.out_dir, f)
        os.makedirs(os.path.dirname(full_f), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(full_f+'.transcibe.csv', sep=';')

if __name__ == "__main__":
    main()

