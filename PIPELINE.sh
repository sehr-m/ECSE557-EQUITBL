#!/bin/bash

# author: Sehr Moosabhoy (based on code by Hannah Devinney)
# run this script to train a topic model on a corpus and visualize the topics
# takes in descriptor and data file from config file

#shortcut to tm folder
TM=`pwd`'/tools/tm'

#step 1: set up your python environment (replace with whatever path is relevant for you)
ENVIRONMENT='.venv/bin/activate'
source $ENVIRONMENT

#step 1.5: sort out your CONFIG and LOG files
CONFIG='config_files/copilot_config.ini' #make sure to go into this and set appropriate absolute paths!
LOG='logs/log_EXAMPLE.txt'

#get values from config file
DESCRIPTOR=$(grep 'descriptor' $CONFIG | cut -d'=' -f2)
echo $DESCRIPTOR

DATA=$(grep 'data_file' $CONFIG | cut -d'=' -f2)
echo $DATA

#step 2: if your corpus is not already in the right format, convert it
python3 to_schema.py -data_file "$DATA" -descriptor $DESCRIPTOR

#step 3 if your corpus is not already preprocessed, do it now
#N/B: replace with appropriate preprocessing python files as necessary. This one gets the lemmas and parts of speech tags, and then splits articles into documents of 24 terms (moving window)
python3 preprocess.py -config $CONFIG

#(if you have a memory limit increase here is where to do it)
ulimit -d unlimited -v unlimited

#step 4: train the model (+collect timing info)
#/bin/time -o $LOG -v python3 $TM/run_and_save_tm.py -config $CONFIG #OPTIONAL log the time it takes to train
python3 $TM/run_and_save_tm.py -config $CONFIG

#step 5: get the VISUALIZATIONS of that model
OUTNAME=$DESCRIPTOR'_example'
SEEDS='gendered_lemmaPOS/all_seeds.txt'
TITLE=$DESCRIPTOR'_corpus'
python3 visualize_topics.py -config $CONFIG -outname $OUTNAME -seeds $SEEDS -k 30 -num_topics 3 -title $TITLE

