#!/usr/bin/env python3
import os
import argparse
import subprocess
import boto.ec2
import json
import time
import datetime

from misc import get_instances_states, get_instances_to_start, \
                get_instances_off_schedule, get_instances_to_stop

##################################################
# instances.conf contains the instance id and the 
# corresponding start and stop times
##################################################

with open('instances.conf') as json_data:
    schedule_instances = json.load(json_data)


##################################################
# check input, raise an error if necessary
##################################################


###########
# Settings
###########
conn = boto.ec2.connect_to_region("eu-west-1")
os.environ['TZ'] = 'Europe/Paris'
time.tzset()

current_time = datetime.datetime.now().time()

##############################
# get current state for each
# instance declared
##############################

current_state_instances = get_instances_states(conn, format='dict')
#print('all instances', current_state_instances, '\n\n')

####################
#instances to start 
####################

instances_ids_to_start = get_instances_to_start(current_state_instances, schedule_instances, current_time)

if len(instances_ids_to_start) > 0:    
    conn.start_instances(instance_ids=instances_ids_to_start)
    print('Instances to be started at', datetime.datetime.now(), ' :' , instances_ids_to_start)

#####################
#instances to stop a
#####################

instances_ids_to_stop = get_instances_to_stop(current_state_instances, schedule_instances,current_time)

if len(instances_ids_to_stop) > 0:
    conn.stop_instances(instance_ids=instances_ids_to_stop)
    print('Instances to be stopped at', datetime.datetime.now(), ' :' , instances_ids_to_stop)

#######################################
# It's 9PM, let's turn off the instance
# that were running after scheduled time
#######################################

if current_time.hour == 21:

    instances_off_schedule = list(set(get_instances_off_schedule()))

    if len(instances_off_schedule) > 0:
        conn.stop_instances(instance_ids= instances_off_schedule)
        print("Stopping off scheduled instances " + ','.join(instances_off_schedule) + " at", datetime.datetime.now() )
        os.remove('instance_off_schedule.tmp')



