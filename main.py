#!/usr/bin/env python
#coding:utf-8

import zipfile, config, os, sys, shutil, time

def write_channel(apk_path, channel, prefix = 'channel'):
    """docstring for write_channel"""
    try:
        tmp = 'tmp'
        zipped = zipfile.ZipFile(apk_path, 'a', zipfile.ZIP_DEFLATED)
        empty_channel_file = "META-INF/{0}_{1}".format(prefix, channel)

        if os.path.exists(tmp) is False:
            os.system('touch ' + tmp)

        zipped.write(tmp, empty_channel_file)
        zipped.close()
    except Exception as e:
        print e

        return False
    else:
        return True

def main():
    """docstring for main"""

    channels = []

    print '='*30
    print '你好,欢迎使用快速打包工具!'
    print '='*30
    print

    if os.path.exists(config.ORIGIN_APK_NAME) is False:
        print config.ORIGIN_APK_NAME, '不存在,请添加原始包;若已经添加,请更名为', config.ORIGIN_APK_NAME
        print '='*60
        sys.exit()

    if os.path.exists(config.CHANNEL_FILE) is False:
        print config.CHANNEL_FILE, '不存在,请添加渠道文件;若已经添加,请更名为', config.CHANNEL_FILE
        print '='*60
        sys.exit()
    else:
        with open(config.CHANNEL_FILE, 'r') as f:
            channels = [ line.strip() for line in f.readlines() if line.strip()]

        if len(channels) == 0:
            print '渠道文件不能为空, 请在', config.CHANNEL_FILE , '文件里添加渠道名字'
            print '='*60
            sys.exit()

    print '当前设置的version值', config.VERSION
    version = raw_input(">>>input version eg:3.3.1 or ''\n>>>version = ") or config.VERSION

    print '正在复制原始包'
    print

    t = time.strftime('%Y-%m-%d-%H_%M_%S')
    if os.mkdir(config.APK_DIR+t) is False:
        print config.APK_DIR+t, '创建失败'
        print '='*60
        sys.exit()

    #单线程复制&添加渠道
    try:

        start = time.time()
        for channel in channels:

            print '='*20, channel, '='*20

            new_channel_name = '_'.join([config.APK_PREFIX, channel, version]) + config.APK_EXT

            print 'copy', config.ORIGIN_APK_NAME, ' -> ', new_channel_name
            shutil.copy(config.ORIGIN_APK_NAME, new_channel_name)

            if write_channel(new_channel_name, channel) is False:
                print '添加channel失败'
                print '='*60
                sys.exit()
            else:
                print 'write channel', channel, 'is successful'

                print 'move', new_channel_name, ' -> ', config.APK_DIR + t
                shutil.move(new_channel_name, config.APK_DIR + t)

            print '='*20, channel, '='*20
            print

        end = time.time()
        print '复制了', len(channels), '个包'
        print '复制耗时', end-start, 's'
    except Exception as e:
        print e
    else:
        print '复制完毕'


if __name__ == '__main__':
    main()
