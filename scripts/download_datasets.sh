#!/usr/bin/env bash

gather_dataset () {
    # $1: url, $2: zip file name, $3: inner folder name to remove
    download_unzip $1 $2
    rearrange_folder ${2%.*}
}

download_unzip () { 
    # Downloads from url ($1) and unzips to folder (${2%.*}) before removing the original zip file ($2)
    wget $1 -O $2
    unzip $2 -d "${2%.*}"
    rm -rf $2
}

rearrange_folder () {
    # Removes "__MACOSX" folder and .DS_Store files, and shift all the files to the root folder
    cd $1
    rm -rf "__MACOSX"
    inner_folders=`ls -d */` # Track the original folder names (to be removed later)

    # We remove the .DS_Store files in 2 separate steps to demonstrate how to use the find command (ofc, this can be optimised into 1 line)
    mv `find ./ -maxdepth 2 ! -path "*.DS_Store" -path "./*/*"` .
    rm -f `find ./ -path "*.DS_Store"`

    # Iterate through all the inner folders and remove them
    for inner_folder_name in $inner_folders; do
        rm -rf $inner_folder_name
    done
    cd ..
}


# Start of the script
cd "data"

# Download and rearrange the train_data / normal data
gather_dataset "https://cloud.tsinghua.edu.cn/f/7eece510dc784e70a083/?dl=1" "train_data.zip"

# Download and rearrange the test_data / data with failure
gather_dataset "https://cloud.tsinghua.edu.cn/f/0593e1aa85144cf2b745/?dl=1" "test_data.zip"