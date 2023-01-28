# Usage:
# python build_file_list.py --dataset gms --frame_path gms_frames --out_list_path settings

import argparse
import os
import glob
import random
import fnmatch

def parse_directory(path, rgb_prefix='img_', flow_x_prefix='flow_x_', flow_y_prefix='flow_y_'):
    """
    Parse directories holding extracted frames from standard benchmarks
    """
    print('parse frames under folder {}'.format(path))
    frame_folders = glob.glob(os.path.join(path, '*'))

    def count_files(directory, prefix_list):
        lst = os.listdir(directory)
        # print("lst", len(lst))
        # print("directory", directory)
        cnt_list = [len(fnmatch.filter(lst, x+'*')) for x in prefix_list]
        return cnt_list

    rgb_counts = {}
    flow_counts = {}
    for i,f in enumerate(frame_folders):
        # print("i", i)
        # print("f", f)
        lst = os.listdir(f)
        for each in lst:
            each = str(f)+ '\\' + each
            # print("each", each)
            all_cnt = count_files(each, (rgb_prefix, flow_x_prefix, flow_y_prefix))
            # print("all_cnt", all_cnt)
            k = each.split('/')[-1]
            #print("k", k)
            rgb_counts[k] = all_cnt[0]
            x_cnt = all_cnt[1]
            y_cnt = all_cnt[2]
            if x_cnt != y_cnt:
                raise ValueError('x and y direction have different number of flow images. video: '+f)
            flow_counts[k] = x_cnt
            # if i % 200 == 0:
                # print('{} videos parsed'.format(i))

    print('frame folder analysis done')
    # print('rgb_counts', rgb_counts)
    # print('flow_counts', flow_counts)
    return rgb_counts, flow_counts


def build_split_list(split_tuple, frame_info, split_idx, shuffle=False):
    split = split_tuple[split_idx]

    def build_set_list(set_list):
        rgb_list, flow_list = list(), list()
        # print("set_list", set_list)
        # print("frame_info[0]", frame_info[0])
        for item in set_list:
            # print("item[0]", item[0])
            rgb_cnt = frame_info[0]["gms_frames\\" + item[0].rsplit('_',1)[0]+ '\\' + item[0]]
            flow_cnt = frame_info[1]["gms_frames\\" + item[0].rsplit('_',1)[0]+ '\\'+ item[0]]
            rgb_list.append('{} {} {}\n'.format(item[0], rgb_cnt, item[1]))
            flow_list.append('{} {} {}\n'.format(item[0], flow_cnt, item[1]))
        if shuffle:
            random.shuffle(rgb_list)
            random.shuffle(flow_list)
        return rgb_list, flow_list

    train_rgb_list, train_flow_list = build_set_list(split[0])
    test_rgb_list, test_flow_list = build_set_list(split[1])
    return (train_rgb_list, test_rgb_list), (train_flow_list, test_flow_list)


def parse_gms_splits():
    class_ind = [x.strip().split() for x in open('gms_splits/classInd.txt')]
    class_mapping = {x[1]:int(x[0])-1 for x in class_ind}

    def line2rec(line):
        # print("line", line.strip())
        items = line.strip().rsplit('/',1)[1]
        label = class_mapping[items.rsplit('_',1)[0]]
        vid = items.split('.')[0]
        # print("vid", vid)
        # print("label", label)
        return vid, label

    splits = []
    for i in range(1, 4):
        train_list = [line2rec(x) for x in open('gms_splits/trainlist_{:d}.txt'.format(i))]
        test_list = [line2rec(x) for x in open('gms_splits/testlist_{:d}.txt'.format(i))]
        splits.append((train_list, test_list))
    return splits

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='gms', choices=['gms', 'other'])
    parser.add_argument('--frame_path', type=str, default='./gms_frames',
                        help="root directory holding the frames")
    parser.add_argument('--out_list_path', type=str, default='./settings')
    parser.add_argument('--rgb_prefix', type=str, default='img_',
                        help="prefix of RGB frames")
    parser.add_argument('--flow_x_prefix', type=str, default='flow_x_',
                        help="prefix of x direction flow images")
    parser.add_argument('--flow_y_prefix', type=str, default='flow_y_',
                        help="prefix of y direction flow images", )
    parser.add_argument('--num_split', type=int, default=3,
                        help="number of split building file list")
    parser.add_argument('--shuffle', action='store_true', default=False)

    args = parser.parse_args()

    dataset = args.dataset
    frame_path = args.frame_path
    rgb_p = args.rgb_prefix
    flow_x_p = args.flow_x_prefix
    flow_y_p = args.flow_y_prefix
    num_split = args.num_split
    out_path = args.out_list_path
    shuffle = args.shuffle

    out_path = os.path.join(out_path, dataset)
    if not os.path.isdir(out_path):
        print("creating folder: "+out_path)
        os.makedirs(out_path)

    # operation
    print('processing dataset {}'.format(dataset))
    if dataset=='gms':
        split_tp = parse_gms_splits()
    f_info = parse_directory(frame_path, rgb_p, flow_x_p, flow_y_p)
    # print("f_info", f_info)


    print('writing list files for training/testing')
    for i in range(max(num_split, len(split_tp))):
        lists = build_split_list(split_tp, f_info, i, shuffle)
        open(os.path.join(out_path, 'train_rgb_split{}.txt'.format(i + 1)), 'w').writelines(lists[0][0])
        open(os.path.join(out_path, 'val_rgb_split{}.txt'.format(i + 1)), 'w').writelines(lists[0][1])
        open(os.path.join(out_path, 'train_flow_split{}.txt'.format(i + 1)), 'w').writelines(lists[1][0])
        open(os.path.join(out_path, 'val_flow_split{}.txt'.format(i + 1)), 'w').writelines(lists[1][1])
