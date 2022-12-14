#!/usr/bin/python
# -*- coding: utf-8 -*-

# from __future__ import absolute_import, division, print_function
# __metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'core'}

import os
import subprocess as sp
import math
from ansible.module_utils.basic import *

class AnsibleModuleError(Exception):
    def __init__(self, results):
        self.results = results

def main():
    module_args = dict(
        threshold=dict(required=True, type='str'),
        scale=dict(required=True, type='str'),
        replica=dict(required=True, type='str'),
        limitcpu=dict(required=True, type='str'),
        limitmem=dict(required=True, type='str')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    pthreshold = module.params['threshold']
    pscale = module.params['scale']
    preplica = module.params['replica']
    plimitcpu = module.params['limitcpu']
    plimitmem = module.params['limitmem']

    f = open('/tmp/scaleup/cpu.tmp','r')        
    lines = f.readlines()
    cpu = 0
    for x in lines:    
        cpu += int(x.replace('m', ''))
    f = open('/tmp/scaleup/mem.tmp','r')        
    lines = f.readlines()
    mem = 0
    for x in lines:    
        mem += int(x.replace('Mi', ''))        
    lc = plimitcpu
    limitcpu = int(lc.replace('m', ''))
    lm = plimitmem
    limitmem = int(lm.replace('Mi', ''))
    s = pscale
    scale = int(s)
    r = preplica                    
    replica = int(r)
    t = pthreshold
    threshold = int(t)
    thresholdcpu = limitcpu * replica * (threshold/100)
    thresholdmem = limitmem * replica * (threshold/100)
    triggerscale = 0
    if cpu >= thresholdcpu:
        newlimitcpu = limitcpu * (1 + (scale/100))
        sp.getoutput(f"sed -i 's/cpu: {limitcpu}m/cpu: {math.trunc(newlimitcpu)}m/g' /tmp/scaleup/dc.yml")
        triggerscale = 1
    if mem >= thresholdmem:
        newlimitmem = limitmem * (1 + (scale/100))
        sp.getoutput(f"sed -i 's/memory: {limitmem}Mi/memory: {math.trunc(newlimitmem)}Mi/g' /tmp/scaleup/dc.yml")
        triggerscale = 1
    
    if triggerscale == 1 :
        theReturnValue = {"triggerscale": "true","msg": "Trigger scaling up!"}
        module.exit_json(changed=True, meta=theReturnValue)
    else:
        theReturnValue = {"triggerscale": "false","msg": f"Nothing to scale up!"}
        module.exit_json(changed=False, meta=theReturnValue)

if __name__ == '__main__':
    main()