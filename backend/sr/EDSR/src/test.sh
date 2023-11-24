N_THREADS=1
BATCH_SIZE=1
MODEL=EDSR
SAVE=edsr
PRE_TRAIN=download
DIR_DATA=../datasets
N_FEATS=64
N_RESBLOCKS=16
SCALE=3

python main.py --test_only --save_results --scale $SCALE --n_resblocks $N_RESBLOCKS --n_feats $N_FEATS --pre_train $PRE_TRAIN --n_threads $N_THREADS --batch_size $BATCH_SIZE --model $MODEL --dir_data $DIR_DATA --save $SAVE
