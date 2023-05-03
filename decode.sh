#!/bin/bash - 

set -o nounset                              # Treat unset variables as an error
set -e

data_dir=data # change it 
exp_dir=exp

[ ! -d $exp_dir ] && mkdir -p $exp_dir

if [ ! -f $data_dir/.done.m4a2wav ] ; then 
    find $data_dir -name '*.m4a' > $data_dir/m4a.list
    for f in $(cat $data_dir/m4a.list) ; do 
        echo "$f"
        [ ! -f ${f%.*}.wav ] && ffmpeg -i $f -ar 16000 ${f%.*}.wav 
    done 

    ( 
    cd $data_dir
    find ./ -name '*.wav' | while read f ; do 
        new_f=$(echo $f | sed -e 's/\.\///g' -e 's/\//+/g') 
        echo $f $new_f
        ln -s $f $new_f 
    done
    )
    touch $data_dir/.done.m4a2wav
fi

if [ ! -f $exp_dir/.done.vad ] ; then 
    python to_json.py --out_file $exp_dir/wavs.json \
        $(ls $data_dir/*.wav)

    python NeMo/examples/asr/speech_classification/vad_infer.py \
        --config-path ../conf/vad/ \
        --config-name=vad_inference_postprocessing.yaml \
        dataset=$exp_dir/wavs.json \
        vad.model_path=vad_multilingual_marblenet \
        frame_out_dir="$exp_dir/vad_frame" \
        vad.parameters.window_length_in_sec=0.63 \
        vad.parameters.postprocessing.onset=0.7 \
        vad.parameters.postprocessing.offset=0.4 \
        vad.parameters.postprocessing.min_duration_on=1 \
        vad.parameters.postprocessing.min_duration_off=0.5 \
        out_manifest_filepath=$exp_dir/vad.json
    touch $exp_dir/.done.vad
fi

if [ ! -f $exp_dir/.done.asr ] ; then 
    python vad_to_segments.py --out_dir $exp_dir/processed/ \
        $exp_dir/vad.json

    python NeMo/examples/asr/transcribe_speech.py \
        model_path=./stt_ru_conformer_transducer_large.nemo \
        dataset_manifest=$exp_dir/processed/segmented.json \
        output_filename=$exp_dir/asr.json \
        batch_size=4

    python results_to_csv.py $exp_dir/asr.json $exp_dir
    touch $exp_dir/.done.asr
fi
