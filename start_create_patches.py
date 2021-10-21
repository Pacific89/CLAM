import json
import sys
import os
import argparse

# open config file for "RUN-COMMAND"
with open("/usr/local/config/clam_command_config.json") as json_file:
    clam_config = json.loads(json_file.read())

def call_create_patches(args):

    if args.config:
        # try to read dict from json string and update default values
        try:
            config_dict = json.loads(args.config)
            clam_config.update(config_dict)
        except:
            print("Not a valid json config string. Using default")

    file_name = sys.argv[1]

    patch_size = clam_config["patch_size"] # set patch size (128 needed for ARA-NET / 224 needed for VGG16 feature extraction)
    seg = "--seg" if json.loads(clam_config["seg"].lower()) else ""
    patch = "--patch" if json.loads(clam_config["patch"].lower()) else ""
    stitch = "--stitch" if json.loads(clam_config["stitch"].lower()) else ""
    no_auto_skip = "--no_auto_skip" if json.loads(clam_config["no_auto_skip"].lower()) else ""
    preset = "--preset preset.csv"
    patch_level = "--patch_level {0}".format(int(clam_config["patch_level"])) # downsample level for patch calculation
    process_list = "--process_list process_list.csv"
    output_path = clam_config["output_path"] + "/{0}/data/clam".format(file_name.split(".svs")[0]) # set output folder

    print("CONFIG:")
    print(clam_config)
    # get filename from command line arguments:
    # create input path:
    input_path = "/usr/local/data/{0}".format(file_name)
    # create correct command to create patch coordinates using CLAM:
    clam_command = "python usr/local/src/clam/create_patches_fp.py --source {0} --save_dir {1} --patch_size {2} {3} {4} {5}".format(input_path, output_path, patch_size, seg, patch, stitch)
    # start CLAM:
    os.system(clam_command)
    print(clam_command)


def call_extract_features(args):
    print("Calling extract features...")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_pattern',
                help="one input file: example.svs",
                nargs=1)
    parser.add_argument('-c', '--config', help="json string with config parameters: \n Defaults: {0}".format(clam_config), type=str)
    parser.add_argument('-cp', '--create_patches', help="call create_patches.py", default=False, action="store_true")
    parser.add_argument('-ef', '--extract_features', help="call extract_features.py",default=False, action="store_true")

    args = parser.parse_args()
    print(args)

    if args.create_patches:
        call_create_patches(args)
    elif args.extract_features:   
        call_extract_features(args)