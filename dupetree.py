################################################################################
# Copyright: ESRI Italia S.p.a.
# Authore: Marco Foi
# Date: 14 Jan 2015
# Version: 1.0
#
# Purpose: this script clones a source directory tree, not including content,
# into a new location identified by a target directory.
# The source folders are created in the new target tree just if they contain
# at least one files having the extension specified in parameter 'soughtExt'.
# Usage: First the script must be edited with any text editor and desired values
# for the three parameters must be entered.

# soughtExt String (e.g. "shp")
# source_path String (e.g. "V:\source-datadir\path")
# dest_path String (e.g. "D:\target-datadir\path")

# Then thee script can be run by typying at command prompt (CMD) the command:
# python dupetree.py
################################################################################

import os

# Put here the file extension that will control which folders will be recreated
soughtExt = ".exe"
# Put here path to the root folder of the to-be-recreated folder tree
# (no trailing slash)
source_path = "C:\Users\mfoi\Downloads"
# Put here the path to the folder where the source folder tree will be recreated
# (no trailing slash)
dest_path = "C:\Users\mfoi\Desktop\pic"

def seek_for_files_and_crate_dir(printDir, printFileName):
    counter = 0
    #for root, dirs, files in os.walk('O:\Foto\Foto_DIGIT'):
    for root, dirs, files in os.walk(source_path):
        if printDir:
            print root
        for file in files:
            if file.endswith(soughtExt):
                """or file.endswith(".exe"):"""
                if printFileName:
                    print file
                counter += os.path.getsize(os.path.join(root, file))
                if root != source_path:
                    relativizedRoot = root[len(source_path)+1:]
                    detsDir = os.path.join(dest_path,relativizedRoot)
                    if not os.path.isdir(detsDir):
                        os.makedirs(detsDir)
    return counter

print seek_for_files_and_crate_dir(True, False)/(1024*1024), "Mb found of",soughtExt, "files"