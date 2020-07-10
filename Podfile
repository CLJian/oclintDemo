platform :ios, '9.0'

source 'https://github.com/CocoaPods/Specs.git'
source 'https://github.com/aliyun/aliyun-specs.git'

post_install do |installer|
  installer.pods_project.targets.each do |target|
      target.build_configurations.each do |config|
          config.build_settings['COMPILER_INDEX_STORE_ENABLE'] = "NO"
      end
  end
end

target 'demo' do
  use_frameworks!
  inhibit_all_warnings!

  pod 'AFNetworking', '~> 4.0.0'
end
