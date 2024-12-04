#!/usr/bin/python3
# -*- coding: utf-8 -*-

# version: 1.0
# author: Sehr Moosabhoy (based on code by Hannah Devinney)
# code for transforming our collected corpus into the .json files
# compatible with the rest of EQUITBL and saving them in the corpora folder.
# Should be quite adaptable to other corpora.

from argparse import ArgumentParser
import pandas as pd


# the relevant bits from this package are in tools/corpus/corpus_mapping.py
from tools.corpus.corpus_mapping import map_to_schema


def main():
    a = ArgumentParser()
    a.add_argument(
        "-data_file",
        dest="data_file",
        required=True,
        type=str,
        help="path to data file",
    )
    a.add_argument(
        "-descriptor",
        dest="descriptor",
        required=True,
        type=str,
        help="descriptor for output files",
    )

    out_file_path = "test_files/input/corpora/"

    # load csv file
    print(a.parse_args().data_file)
    df = pd.read_csv(a.parse_args().data_file)
    descriptor = a.parse_args().descriptor

    # take each run and put it in a new row
    data = []
    # make first row the header
    df.columns = df.iloc[0]
    df = df[1:]
    print(df.head())
    for index, row in df.iterrows():
        id = index * 3
        data.append({"file_id": id, "sentences": row["run 1"].replace('"', " ")})
        data.append({"file_id": id + 1, "sentences": row["run 2"].replace('"', " ")})
        data.append({"file_id": id + 1, "sentences": row["run 3"].replace('"', " ")})

    full_df = pd.DataFrame(data)
    # save it somewhere
    full_save = out_file_path + descriptor + "_categories.json"
    full_df.to_json(full_save)

    # so now we have a dataframe with the columns 'file_id' 'category' and 'sentences'
    # (and we will end up ignoring the 'category' field
    # but e.g. if you only wanted to convert a subset of the corpus it would be useful!)
    # we have to tell map_to_schema what IDs and TEXTs are currently called:
    id_name = "file_id"
    text_name = "sentences"

    # map to the EQUITBL schema
    new_df = map_to_schema(
        original_file=full_save, text_path=text_name, id_path=id_name
    )

    # save!
    save_as = out_file_path + descriptor + "_corpus.json"
    new_df.to_json(save_as)


if __name__ == "__main__":
    main()
