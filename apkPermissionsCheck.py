#encoding : utf-8

"""apk权限检查报告

反编译解析xml文件，检查其中是否存在不必要的权限声明...

使用前请配置必要权限集合:NECESSARYPERMISSIONSSET
需要将apktool.jar放置在同目录下

使用方法：
1. -path/--path 检查某个路径下的所有apk
2. -apkname/--apkname 检查若干当前路径下的apk文件
    
"""

import os
import re
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--path', '-path', required=False,
                    help='Optional, Directory path of a group of apk files')
parser.add_argument('--apkname', '-apkname', required=False,
                    help='Optional, Several apk files\' names', nargs='+')

NECESSARYPERMISSIONSSET = {'android.permission.RECEIVE_USER_PRESENT',
                           'android.permission.MOUNT_UNMOUNT_FILESYSTEMS',
                           'android.permission.CAMERA',
                           'android.permission.WRITE_EXTERNAL_STORAGE',
                           'android.permission.READ_EXTERNAL_STORAGE',
                           'android.permission.RECORD_AUDIO'}


def deCompile(filename):
    apktool_command = "java -jar apktool.jar d -f " + filename
    os.system(apktool_command)


def checkPermissionsList(filename):
    manifest_path = os.path.join("./" + filename + "/AndroidManifest.xml")
    ET.register_namespace(
        'android', 'http://schemas.android.com/apk/res/android')
    print(manifest_path)
    manifest_tree = ET.parse(manifest_path)
    manifest_root = manifest_tree.getroot()
    uses_permission_list = manifest_root.findall("uses-permission")

    warnings_permissions = []
    for permission in uses_permission_list:
        permission_name = permission.attrib['{http://schemas.android.com/apk/res/android}name']
        if(re.search(r'^(android\.permission)\..*', permission_name)):
            if permission_name not in NECESSARYPERMISSIONSSET:
                if(permission_name not in warnings_permissions):
                    warnings_permissions.append(permission_name)
    warnings_permissions.append(filename)
    return warnings_permissions


def reportPermissionsWarnings(warnings_permissions):
    warning_nums = len(warnings_permissions)-1
    if warning_nums == 0:
        print()
        print('========{}========'.format("Checking Result..."))
        print()
        print('**CLEAR ~**\n')
        print('There is 0 WARNING Android permission in : {}'.format(
            warnings_permissions[0]))
    else:
        print()
        print('========{}========'.format("Checking Result..."))
        print()
        print('**WARNING !**\n')
        print('{} unnecessary permissions founded in : {}'.format(
            warning_nums, warnings_permissions[warning_nums]))
        for i in range(warning_nums):
            print('        {}\n'.format(warnings_permissions[i]))
    return


if __name__ == '__main__':
    args = parser.parse_args()
    if not(args.path) and not(args.apkname):
        parser.print_help()
        exit(0)
    if args.path:
        for apks in os.listdir(args.path):
            if(re.search(r'apk$', apks)):
                print()
                deCompile(apks)
                folder_name = re.sub(r'\.apk$', '', apks)
                warnings_permissions = checkPermissionsList(folder_name)
                reportPermissionsWarnings(warnings_permissions)
    elif args.apkname:
        for apks in args.apkname:
            deCompile(apks)
            folder_name = re.sub(r'\.apk$', '', apks)
            warnings_permissions = checkPermissionsList(folder_name)
            reportPermissionsWarnings(warnings_permissions)