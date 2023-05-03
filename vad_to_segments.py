import librosa
import os
import json
import argparse
import soundfile as sf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_dir', required=True)
    parser.add_argument('vad_json')
    args = parser.parse_args()
    os.makedirs(os.path.join(args.out_dir, 'segmented'), exist_ok=True)
    man = []
    for line in open(args.vad_json, 'r', encoding='utf-8'):
        file = json.loads(line)
        man.append(file)

    lines = []
    for m in man:
        print(m)
        w, o, d = m['audio_filepath'], m['offset'], m['duration']
        wav, sr = librosa.load(w, offset=o, duration=d)
        out_fname = os.path.join(args.out_dir, 'segmented', f'{os.path.basename(w)}_o{o}_{d}.wav')
        sf.write(out_fname, wav, sr)
        line = '{' + f'"audio_filepath": "{out_fname}", "duration": {d}, "offset": 0, "text": "<unk>"' + '}'
        lines.append(line)

    with open(os.path.join(args.out_dir, 'segmented.json'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()

