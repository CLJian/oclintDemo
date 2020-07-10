# Type a script or drag a script file from your workspace to insert its path.

export LC_CTYPE=en_US.UTF-8
set -euo pipefail # 脚本只要发生错误，就终止执行
# 删除DerivedData的build文件
#echo $(dirname ${BUILD_DIR})
rm -rf $(dirname ${BUILD_DIR})

# 1. 环境配置，判断是否安装oclint，没有则安装
if which oclint 2>/dev/null; then
echo 'oclint already installed'
else # install oclint
brew tap oclint/formulae
brew install oclint
fi

# 2.0 使用xcodebuild构建项目，并且使用xcprretty将便于产物转换为json
prettyPath="/usr/local/bin/xcpretty" # 替换为你安装的本地路径
#echo ${prettyPath}
projectName="demo" # 替换为你的project name
xcodebuild -scheme ${projectName} -workspace ${projectName}.xcworkspace clean && xcodebuild clean && xcodebuild -scheme ${projectName} -workspace ${projectName}.xcworkspace -configuration Debug -sdk iphonesimulator COMPILER_INDEX_STORE_ENABLE=NO | ${prettyPath} -r json-compilation-database  -o compile_commands.json

# 3.0 判断json是否
if [ -f ./compile_commands.json ]; then echo "compile_commands.json 文件存在";
else echo "-----compile_commands.json文件不存在-----"; fi

# 4.0 oclint分析json
oclint-json-compilation-database -e Pods -- -report-type xcode
