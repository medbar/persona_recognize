import json
import librosa
import argparse
from glob import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_file', required=True)
    parser.add_argument('wavs', nargs='+', help='wavs to dump')
    args = parser.parse_args()
    lines=[]
    #for w in glob('data/Диалоги/*/*/*.wav'):
    for w in args.wavs:
        print(w)
        #audio, sample_rate = librosa.load(w)
        #d = audio.shape[0] / sample_rate
        d = librosa.get_duration(filename=w)

        line='{' + f'"audio_filepath": "{w}", "duration": {d}, "offset": 0, "text": "<unk>"' + '}'
        lines.append(line)
        print(line)

    with open(args.out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))




if __name__ == '__main__':
    main()
