import os
import sys
import argparse

from util import load_kb, generate_tmp_file, unlink_tmp_file, OpenNMT_dir

def build_arg_parser():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    # Create the parser for the "prepare" command
    parser_prepare = subparsers.add_parser('prepare')
    parser_prepare.add_argument('-data_dir', type=str, required=True,
            help="Path to the dataset")
    parser_prepare.add_argument('-data_out', type=str, required=True,
            help="Output file for the prepared data")
    parser_prepare.set_defaults(func=data_preparation)

    # Create the parser for the "train" command
    parser_train = subparsers.add_parser('train')
    parser_train.add_argument('-data', type=str, required=True,
            help='Path prefix to the ".train.pt" and ".valid.pt" file path')
    parser_train.add_argument('-model', type=str, required=True,
            help="Model filename")
    parser_train.set_defaults(func=train)

    # Create the parser for the "generate" command
    parser_generate = subparsers.add_parser('generate')
    parser_generate.add_argument('-data_dir', type=str,
            required=True, help="Path to the dataset")
    parser_generate.add_argument('-dataset', type=str,
            default='valid', help="Dataset for generating post modifier")
    parser_generate.add_argument('-model', type=str, required=True,
            help="Path to model .pt file")
    parser_generate.add_argument('-out', type=str, default="pred.txt",
            help="Path to output the prediction")
    parser_generate.set_defaults(func=generate)

    return parser

def data_preparation(args):

    dataset = ['train', 'valid']
    wiki_kb = {}
    src = {}
    tgt = {}

    arguments = ""
    for set_info in dataset:
        wiki_kb[set_info] = load_kb(os.path.join(args.data_dir, "{}.wiki".format(set_info)))
        src[set_info], tgt[set_info] = generate_tmp_file(os.path.join(args.data_dir, "{}.pm".format(set_info)), wiki_kb[set_info])
        arguments += "-{}_src {} -{}_tgt {} ".format(set_info, src[set_info], set_info, tgt[set_info])

    script = "python {}/preprocess.py {}-save_data {} -src_seq_length 1000".format(OpenNMT_dir, arguments, args.data_out)

    print(script)
    os.system(script)
    for set_info in dataset:
        unlink_tmp_file(src[set_info])
        unlink_tmp_file(tgt[set_info])

def train(args):

    rnn_type = "brnn"
    batch_size = 32
    attention = "general"

    script = "python {}/train.py -data {} -save_model {} -gpuid 0 \
            -global_attention {} -batch_size {} -encoder_type {}".format(OpenNMT_dir, args.data, args.model, attention, batch_size, rnn_type)

    print(script)
    os.system(script)

def generate(args):

    wiki_kb = load_kb(os.path.join(args.data_dir, "{}.wiki".format(args.dataset)))
    src, tgt = generate_tmp_file(os.path.join(args.data_dir, "{}.pm".format(args.dataset)), wiki_kb)

    script = "python {}/translate.py -model {} -src {} -output {} -replace_unk -verbose".format(OpenNMT_dir, args.model, src, args.out)

    os.system(script)

    unlink_tmp_file(src)
    unlink_tmp_file(tgt)

def main(argv):
    if len(argv) < 2:
        print("Please provide command:\n\t python pm_generation.py [prepare|train|generate]")
        exit()

    arg_parser = build_arg_parser()
    in_args = sys.argv[1:]
    args = arg_parser.parse_args(in_args)
    args.func(args)

if __name__ == "__main__":
    main(sys.argv)
