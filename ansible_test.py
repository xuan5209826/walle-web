#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 一  1/ 2 19:15:58 2017
# @Description:
import ansible.runner
import sys

# construct the ansible runner and execute on all hosts
results = ansible.runner.Runner(
    pattern='*', forks=10,
    module_name='command', module_args='/usr/bin/uptime',
).run()

if results is None:
   print "No hosts found"
   sys.exit(1)

print "UP ***********"
for (hostname, result) in results['contacted'].items():
    if not 'failed' in result:
        print "%s >>> %s" % (hostname, result['stdout'])

print "FAILED *******"
for (hostname, result) in results['contacted'].items():
    if 'failed' in result:
        print "%s >>> %s" % (hostname, result['msg'])

print "DOWN *********"
for (hostname, result) in results['dark'].items():
    print "%s >>> %s" % (hostname, result)
