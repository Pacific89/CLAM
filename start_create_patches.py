import json
import sys
import os
import argparse

# open config file for "RUN-COMMAND"
with open("usr/local/config/clam_command_config.json") as json_file:
    clam_config = json.loads(json_file.read())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_pattern',
                help="one input file: example.svs",
                nargs=1)
    parser.add_argument('-c', '--config', help="json string with config parameters", default="{0}".format(clam_config), type=str)

    args = parser.parse_args()

    if args.config:
        # try to read dict from json string and update default values
        try:
            config_dict = json.loads(args.config)
            hqc_config.update(config_dict)
        except:
            print("Not a valid json config string. Using default")

    patch_size = clam_config["patch_size"] # set patch size (128 needed for ARA-NET / 224 needed for VGG16 feature extraction)
    seg = "--seg" if json.loads(clam_config["seg"].lower()) else ""
    patch = "--patch" if json.loads(clam_config["patch"].lower()) else ""
    stitch = "--stitch" if json.loads(clam_config["stitch"].lower()) else ""
    no_auto_skip = "--no_auto_skip" if json.loads(clam_config["no_auto_skip"].lower()) else ""
    preset = "--preset preset.csv"
    patch_level = "--patch_level {0}".format(int(clam_config["patch_level"])) # downsample level for patch calculation
    process_list = "--process_list process_list.csv"
    output_path = clam_config["output_path"] # set output folder

    print("CONFIG:")
    print(clam_config)
    # get filename from command line arguments:
    file_name = sys.argv[1]
    # create input path:
    input_path = "usr/local/data/{0}".format(file_name)
    # create correct command to start HQC:
    clam_command = "python usr/local/src/clam/create_patches_fp.py --source {0} --save_dir {1} --patch_size {2} {3} {4} {5}".format(input_path, output_path, patch_size, seg, patch, stitch)
    # start HQC:
    os.system(clam_command)
    print(clam_command)