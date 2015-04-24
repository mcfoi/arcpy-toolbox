################################################################################
# Copyright: ESRI Italia S.p.a.
# Authore: Marco Foi
# Date: 14 Jan 2015
# Version: 2.0
#
# Purpose: this script clones a source directory tree, not including content,
# into a new location identified by a target directory.
# The source folders are created in the new target tree just if they contain
# at least one files having any of the extensions specified in parameter
# 'soughtExts'.
# Usage: First the script must be edited with any text editor and desired values
# for the three parameters must be entered.
# Output: The script, beside creating the directory tree in the specified traget
# folder, also prints to screen the list of created dirs and the total size of
# the sought files.

# soughtExts List (e.g. [".shp",".dbf",".tif"])
# source_path String (e.g. "V:\source-datadir\path")
# dest_path String (e.g. "D:\target-datadir\path")

# Then thee script can be run by typying at command prompt (CMD) the command:
# python dupetree2.py
################################################################################

import os

# Put here the file extension that will control which folders will be recreated
soughtExts = [".shp",".dbf"]
# Put here path to the root folder of the to-be-recreated folder tree
# (no trailing slash)
source_path = "C:\Users\mfoi\Downloads"
# Put here the path to the folder where the source folder tree will be recreated
# (no trailing slash)
dest_path = "C:\Users\mfoi\Desktop\pic"

def seek_for_files_and_create_dir(printDir, printFileName):
    counter = 0
    #for root, dirs, files in os.walk('O:\Foto\Foto_DIGIT'):
    for root, dirs, files in os.walk(source_path):
        for file in files:
            currext = file[len(file)-4:]
            if currext in soughtExts:
                if printDir:
                    print root
                if printFileName:
                    print file
                counter += os.path.getsize(os.path.join(root, file))
                if root != source_path:
                    relativizedRoot = root[len(source_path)+1:]
                    detsDir = os.path.join(dest_path,relativizedRoot)
                    if not os.path.isdir(detsDir):
                        os.makedirs(detsDir)
    return counter

def format_bytes_value(value):
    if value < 1024:
        label = "Bytes found of"
        divider = 1
    if value >= 1024 and value < (1024*1024):
        label = "Kb found of"
        divider = 1024
    if value >= (1024*1024):
        label = "Mb found of"
        divider = (1024*1024)

    print ""
    if value > 0:
        print "Files with {} extensions were found in following dirs:".format(soughtExts)
    else:
        print "No files found with extensions {} in dir {}".format(soughtExts, source_path)

    result = "{} {} {} files".format((value/divider), label, soughtExts)
    return result

#print seek_for_files_and_crate_dir(True, False)/(1024*1024), "Mb found of",soughtExts, "files"
print format_bytes_value(seek_for_files_and_create_dir(True, False))