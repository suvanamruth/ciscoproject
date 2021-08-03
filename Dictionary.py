'''
Created on Jul 18, 2021

@author: suvanamruth
'''

import os.path
import tarfile
import shlex
import os
import shutil
import gzip
import magic


results = []

def getListOfFiles(dirName):
    '''
        For the given directory path, get list of all files in the directory tree 
    '''
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = []
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


def readDictionary(dir):
    myDictionary = {}
    textFile = open(dir)
    for line in textFile:   
        fields = shlex.split(line.rstrip())
        myDictionary[fields[2]] = fields[1], fields[0]
    
    return myDictionary

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
    cmd = 'gunzip -f {}'.format(infile)
    os.system(cmd)
    return 

def check_if_text_file(infile):
    filetype = magic.from_file(infile)
    if 'ASCII' in filetype:
        if 'long lines' in filetype:
            return False
        else:
            return True
    else:
        return False

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
            continue
        if is_tgz_file(file):
            dirname = os.path.dirname(file)
            if "decode" in file or "ctrace" in file:
                continue
            #   uncompress_gz_file(file)
            #  x = file.rindex(".")
            # Tfile = file[0:x] + ".tar"
                #untar(Tfile
            extractTarFile(file, dirname)
            os.unlink(file)
            
        elif is_gz_file(file):
            uncompress_gz_file(file)
        elif is_tar_file(file):
            untar(file)
            os.unlink(file)



def search(filename, dictionary):     
    with open(filename,"r") as file:
        text = file.read()
        for searchKey in dictionary.keys():
            if searchKey in text:
                #print('String {} found in {}: Metadata: {}'.format(searchKey, filename, dictionary[searchKey]))
                #results.append('String {} found in {}: Metadata: {}'.format(searchKey, filename, dictionary[searchKey]))
                tuple = (dictionary[searchKey][1], searchKey, filename, dictionary[searchKey][0])
                results.append(tuple)
            
            






def mainFunction(inputFileDir, dictionary):
    searchDictionary = readDictionary(dictionary)
    index = inputFileDir.rindex("/")
    outputDir = inputFileDir[0:index + 1] + "temp"
    shutil.rmtree(outputDir, ignore_errors=True)
    os.mkdir(outputDir)
    extractTarFile(inputFileDir, outputDir)
    print("finished extracting")
    files = getListOfFiles(outputDir)
    print("starting scan")
    for file in files:
        if os.path.isdir(file):
            # if this is a directory, skip and move to next file
            continue
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
    
    
    print("done scanning")
    