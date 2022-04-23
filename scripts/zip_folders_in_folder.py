'''This script goes through the folders within a directory and zips each folder.
    If you want to group more than 1 folder in a single zip file set the variable zipf_group_size to the number of folders you want in the zip file 

    How to run this script?
        Please run this script from the top-level of research_utils folder. 
        Run it as: python scripts/zip_folders_in_folder.py
'''

## Standard Library Imports
import os
import zipfile

## Library Imports
import numpy as np
from IPython.core import debugger
breakpoint = debugger.set_trace

## Local Imports
import io_ops

def add_dir_to_zipobj(zipobj, target_dir):
    # rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            arcname = os.path.join(os.path.basename(base), file)
            zipobj.write(fn, arcname)


# def zip_folders(zip_fname, target_dirs):            
#     zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)

if __name__=='__main__':
    # The folder containing all folders that will be zipped
    base_dirpath = '/home/felipe/repos/spatio-temporal-csph/data_gener/TrainData/processed'
    out_dirpath = '/home/felipe/repos/spatio-temporal-csph/data_gener/TrainData/processed_zipped'
    # out_dirpath = './zip_outputs'
    os.makedirs(out_dirpath, exist_ok=True)
    assert(os.path.exists(base_dirpath)), "Invalid input base_dirpath"

    # Flags
    overwrite_existing_zip = False
    zipf_group_size = 20
    group_fname_base = 'scene_group'

    # Remove trailing / if needed
    if(base_dirpath[-1] == '/'): base_dirpath = base_dirpath[0:-1] 

    # Get parent folder name
    parent_folder_name = os.path.split(base_dirpath)[-1]
    print(parent_folder_name)

    # Get all dirpaths
    folder_names = io_ops.get_dirnames_in_dir(base_dirpath)
    n_folders = len(folder_names)
    n_out_zipfiles = min((n_folders // zipf_group_size) + 1, n_folders)

    for i in range(n_out_zipfiles):
        # Get the current folder group
        start_idx = i*zipf_group_size
        end_idx = min(n_folders, start_idx + zipf_group_size)
        curr_folder_names_to_zip = folder_names[start_idx:end_idx]
        # If only one folder per zip, just use the name of the folder as the zip filenmae
        if(zipf_group_size == 1):
            zipobj_fname = curr_folder_names_to_zip[0] + '.zip'
        else:
            zipobj_fname = group_fname_base + '{}.zip'.format(i)
        # Compose the filepath
        zipobj_fpath = os.path.join(out_dirpath, zipobj_fname)
        if(os.path.exists(zipobj_fpath)):
            if(not overwrite_existing_zip):
                print("*****Skipping {} because it already exists*****".format(zipobj_fpath))
                continue
            else:
                print("*****Overwritting {}*****".format(zipobj_fpath))
        # Create zip object that we will add to
        zipobj = zipfile.ZipFile(zipobj_fpath, 'w', zipfile.ZIP_DEFLATED)
        for folder_name in curr_folder_names_to_zip:
            curr_dirpath = os.path.join(base_dirpath, folder_name)
            print("Zipping {} into {}".format(folder_name, zipobj_fpath))
            add_dir_to_zipobj(zipobj, curr_dirpath)
        zipobj.close()



    # for folder_name in folder_names:
    #     curr_dirpath = os.path.join(base_dirpath, folder_name)
    #     zipobj_fpath = os.path.join(out_dirpath, folder_name + '.zip')
        




