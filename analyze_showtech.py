#! /usr/local/bin/python3

'''
Created on Jul 18, 2021

@author: suvanamruth
'''

import os.path
import tarfile
import argparse
import mimetypes
import shlex
import os
import shutil
import gzip
import zipfile
import magic



def createSrchDictionary(file):
    '''
        Create a local python dictionary from user given text file
    '''
    myDictionary = {}
    textFile = open(file)
    for line in textFile:   
        fields = shlex.split(line.rstrip())
        myDictionary[fields[2]] = (fields[1], fields[0])
    if args.verbosity > 0:
        print('Dictionary built: {}'.format(myDictionary))
    return myDictionary


def getListOfFiles(dirName):
    '''
        For the given directory path, get list of all files in the directory tree 
    '''
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


def search(filename, searchDictionary):
    if args.verbosity > 2:
        print('Searching file {}'.format(filename))
    with open(filename,"r") as file:
        text = file.read()
        for searchKey in searchDictionary.keys():
            if searchKey in text:
                print('String [{:20s}] found in {:120s}: Metadata: {}'.format(searchKey, filename, searchDictionary[searchKey]))

            
def is_tgz_file(infile):
    # For now, we'll rely of file extension to figure out the type of file
    # If there is a better way, this function can be replaced

    split_name = os.path.splitext(infile)
    file_ext = split_name[1]
    if file_ext == '.tgz':
        return True
    else:
        return False

def is_gz_file(infile):
    # For now, we'll rely of file extension to figure out the type of file
    # If there is a better way, this function can be replaced

    split_name = os.path.splitext(infile)
    file_ext = split_name[1]
    if file_ext == '.gz':
        return True
    else:
        return False

def is_tar_file(infile):
    filetype = magic.from_file(infile)
    if 'tar archive' in filetype:
        return True
    else:
        return False

def uncompress_gz_file(infile):
    cmd = 'gunzip {}'.format(infile)
    os.system(cmd)
    return

def untar(infile):
    dirname = os.path.dirname(infile)
    tar = tarfile.open(infile, "r:")
    tar.extractall(dirname)
    tar.close()

def extractTarFile(inputFile, outputDir):
    filelist = []
    tar = tarfile.open(inputFile, "r:*")
    filenames = tar.getnames()
    tar.extractall(outputDir)
    tar.close()
    for i in filenames:
        abspath = outputDir + '/' + i
        filelist.append(abspath)

    for file in filelist:
        if os.path.isdir(file):
            # if this is a directory, skip and move to next file
            if args.verbosity > 1:
                print('Skipping directory {}'.format(file))
            continue
        if is_tgz_file(file):
            if args.verbosity > 1:
                print('Extracting tgz file {}'.format(file))
            dirname = os.path.dirname(file)
            extractTarFile(file, dirname)
        elif is_gz_file(file):
            if args.verbosity > 1:
                print('Uncompressing gz file {}'.format(file))
            uncompress_gz_file(file)
        elif is_tar_file(file):
            if args.verbosity > 1:
                print('Untar file {}'.format(file))
            untar(file)


def check_if_text_file(infile):
    filetype = magic.from_file(infile)
    if 'ASCII' in filetype:
        return True
    else:
        if args.verbosity > 1:
            print('Non-ASCII file {} [filetype: {}]'.format(infile,filetype))
        return False
    

def main_entry(args):
    inputFile = args.showtech
    dictFile = args.searchDict

    # first create a search python dictionary from text file
    searchDictionary = createSrchDictionary(dictFile)

    # Create a temporary destination director to untar the inputFile
    # Note that the inputFile is a tar file can contain nested files
    # of directories
    output_dir = "./extract_showtech"

    # Remove if there is any stale directory from past runs
    # And then create a new directory
    shutil.rmtree(output_dir, ignore_errors=True)
    os.mkdir(output_dir)

    # This will recursively unzip, untar files into output_dir
    extractTarFile(inputFile, output_dir)

    # At this point, all the gz files should have been uncompressed
    # we should not see any files with gz extenstions. If there are
    # any gz or tgz files, we'll skip them
    files = getListOfFiles(output_dir)
    for file in files:
       if is_tgz_file(file):
           print('Ignoring tgz file {}'.format(file))
           continue
       elif is_gz_file(file):
           print('Ignoring gz file {}'.format(file))
           continue
       elif (os.path.isfile(file) is False):
           print('Skipping non-file {}'.format(file))
           continue
       elif check_if_text_file(file):
           search(file, searchDictionary)
       else:
           continue


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbosity", action="store", type = int, dest="verbosity", default=1)
    parser.add_argument("-s", "--showtechfile", action="store", type = str, dest="showtech", default='enter_showtech_file')
    parser.add_argument("-d", "--search_dict", action="store", type = str, dest="searchDict", default='enter_search_dict_file')

    args = parser.parse_args()

    file_exists = os.path.exists(args.showtech)

    if file_exists is False:
        print('File {} does not exist'.format(args.showtech))
        exit()

    if is_tgz_file(args.showtech) is False:
        print('File {} should be a tgz file'.format(args.showtech))
        exit()

    main_entry(args)


