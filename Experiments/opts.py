



def parse_args_main():
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument("--txt_path",default='histc_dirs.txt')
    parser.add_argument("--depth_txt_path",default='depth_map_dirs.txt')


    return parser.parse_args()