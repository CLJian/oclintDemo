#!/bin/bash -il
source ~/.bashrc

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

myworkspace=demo.xcworkspace
myscheme=demo

# clean cache
rm -rf ~/Library/Developer/Xcode/DerivedData/;
rm compile_commands.json;
rm oclint_result.html;

# clean -- build -- OCLint analyse
echo 'start analyse';
xcodebuild -workspace $myworkspace -scheme $myscheme clean&&
xcodebuild -workspace $myworkspace -scheme $myscheme \
-configuration Release \
| xcpretty -r json-compilation-database -o compile_commands.json&&
oclint-json-compilation-database -e Pods -e node_modules -e PPAutoPackageScript -e scripts -e build -- \
-report-type pmd >> oclint_result.xml \
echo 'end analyse';
