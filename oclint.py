#!usr/bin/python

# -*- coding: utf-8 -*-

import json
import sys
import math
import os
import xml.etree.cElementTree as ET

maxCountPerFile = 2
reversed_json_file_name = 'compile_commands'


def split_json(all_json_objects):
    total_count = len(all_json_objects)
    sub_file_count = int(math.ceil(float(total_count) / float(maxCountPerFile)))

    sub_files = []

    for i in range(sub_file_count):
        start = i*maxCountPerFile
        end = min((i+1)*maxCountPerFile, total_count)
        sub_json_objects = all_json_objects[start:end]
        file_name = 'compile_commands%02d.json' %(i+1)
        sub_files.append(file_name)

        with open(file_name, 'w') as outputHandler:
            outputHandler.write(json.dumps(sub_json_objects, indent=4))

    return sub_files


def lint_jsonfiles(jsonfiles):
    i = 0
    lenth = len(jsonfiles)
    result_files = []
    for file_name in jsonfiles:
        print 'linting ... %s' %file_name
        echoCommand = '''
        echo 'linting progress: %d / %d'
        ''' % (i, lenth)
        os.system(echoCommand)
        input_file = rename(file_name, 'compile_commands.json')
        out_file = 'oclint%02d.xml' %i
        lint(out_file)
        result_files.append(out_file)
        i += 1
        input_file = rename('compile_commands.json', file_name)
#        os.remove(input_file)
    return result_files


def lint(out_file):
    lint_command = '''oclint-json-compilation-database -e Pods \
    -e node_modules -e PPAutoPackageScript -e scripts -e build -- \
    --verbose \
    --report-type pmd \
    -o %s''' % (out_file)
    os.system(lint_command)


def combine_outputs(output_files):
    # first file
    base_tree = ET.ElementTree(file=output_files[0])
    base_root = base_tree.getroot()

    left_files = output_files[1:len(output_files)]
    for left_file in left_files:
        tree = ET.ElementTree(file=left_file)
        root = tree.getroot()
        
        for child in root:
            base_root.append(child)

    base_tree.write('pmd.xml', encoding='utf-8', xml_declaration=True)


def rename(file_path, new_name):
    paths = os.path.split(file_path)
    new_path = os.path.join(paths[0], new_name)
    os.rename(file_path, new_path)
    return new_path

if __name__ == "__main__":
    lint_command = '''
    source ~/.bashrc
    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8
    rm -rf ~/Library/Developer/Xcode/DerivedData/;
    rm compile_commands.json;
    rm pmd.xml;
    myworkspace=demo.xcworkspace
    myscheme=demo
    xcodebuild -workspace $myworkspace -scheme $myscheme clean&&
    xcodebuild -workspace $myworkspace -scheme $myscheme \
    -configuration Debug COMPILER_INDEX_STORE_ENABLE=NO \
    | xcpretty -r json-compilation-database -o compile_commands.json
    '''
    os.system(lint_command)

    with open('compile_commands.json', 'r') as r_handler:
        json_objects = json.loads(r_handler.read())
    if len(json_objects) <= maxCountPerFile:
        lint('pmd.xml')
    else:
        json_file = rename('compile_commands.json', 'input.json')
        json_files = split_json(json_objects)
        xml_files = lint_jsonfiles(json_files)
        combine_outputs(xml_files)
#        for xml_file in xml_files:
#            os.remove(xml_file)
        rename(json_file, 'compile_commands.json')
    
    judgeCommand = '''
    if [ -f ./pmd.xml ];
    then echo 'done'
         exit 0
    else echo 'failed'
         exit -1
    fi
    '''
    os.system(judgeCommand)
