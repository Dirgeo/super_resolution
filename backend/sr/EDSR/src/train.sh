N_THREADS=1
BATCH_SIZE=1
MODEL=EDSR
SAVE=edsr_x3
PRE_TRAIN=download
DIR_DATA=../datasets
N_FEATS=64
N_RESBLOCKS=16
SCALE=4
EPOCHS=100
DATA_RANGE='1-800/801-900'

python main.py --save_results --data_range $DATA_RANGE --epochs $EPOCHS --scale $SCALE --n_resblocks $N_RESBLOCKS --n_feats $N_FEATS --n_threads $N_THREADS --batch_size $BATCH_SIZE --model $MODEL --dir_data $DIR_DATA --save $SAVE
