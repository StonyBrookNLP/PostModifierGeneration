import os
import tempfile
import json

OpenNMT_dir = "../OpenNMT-py"

def load_kb(infile, verbose=False):
    wiki_kb = {}
    with open(infile, "r") as fin:
        for lid, line in enumerate(fin):
            row = line.strip().split("\t")
            wiki_kb[row[0]] = {}
            wiki_kb[row[0]]['label'] = row[1]
            wiki_kb[row[0]]['aliases'] = row[2].split(",")
            wiki_kb[row[0]]['description'] = row[3].split(",")
            wiki_kb[row[0]]['claims'] = {}
            for claims in json.loads(row[4]):
                for k, v in claims.items():
                    if k == "property":
                        key = v[0]
                        if key in wiki_kb[row[0]]['claims']:
                            wiki_kb[row[0]]['claims'][key].append(v[1])
                        else:
                             wiki_kb[row[0]]['claims'][key] = [v[1]]
            if verbose:
                for k,v in wiki_kb[row[0]].items():
                    print("{}:\t{}".format(k, v))

    return wiki_kb

def generate_tmp_file(infile, wiki_kb, verbose=False):
    _, src_path = tempfile.mkstemp(suffix='.tmp')
    _, tgt_path = tempfile.mkstemp(suffix='.tmp')
    #src_path = "{}.src".format(infile)
    #tgt_path = "{}.tgt".format(infile)
    with open(infile, "r") as fin, open(src_path, "w") as src_out, open(tgt_path, "w") as tgt_out:
        for line in fin:
            row = line.strip().split("\t")
            source = row[0]
            claims = []
            for k, v in wiki_kb[row[4]]['claims'].items():
                claims.append("<rel> {} </rel> <value> {} </value>".format(k, " <and> ".join(v)))

            source += " " + " ".join(claims)
            src_out.write(source + "\n")
            tgt_out.write(row[2] + "\n")
            if verbose:
                print("Sent_Wo_PM: {}".format(row[0]))
                print("Entity: {}".format(row[1]))
                print("PM: {}".format(row[2]))
                print("Sent: {}".format(row[3]))
                print("Wiki_ID: {}".format(row[4]))
                print("Prev_Sent: {}".format(row[5]))

    return src_path, tgt_path

def unlink_tmp_file(file_path):
    os.unlink(file_path)
