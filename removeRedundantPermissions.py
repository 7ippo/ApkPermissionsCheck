#encoding : utf-8

"""AndroidManifest权限去重

解析xml文件，去掉重复的权限声明

使用方法：
-xml/--xml 参数为若干AndroidManifest.xml
    
"""

import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--xml', '-xml', required=True,
                    help='Several XML files', nargs='+')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.xml:
        for xml in args.xml:
            ET.register_namespace(
                'android', 'http://schemas.android.com/apk/res/android')
            manifest_tree = ET.parse(xml)
            manifest_root = manifest_tree.getroot()
            uses_permission_list = manifest_root.findall("uses-permission")
            permission_list = []
            for permission in uses_permission_list:
                permission_name = permission.attrib['{http://schemas.android.com/apk/res/android}name']
                if permission_name not in permission_list:
                    permission_list.append(permission_name)
                else:
                    manifest_root.remove(permission)
            manifest_tree.write(xml)
