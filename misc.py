import datetime
import json
import pickle

def get_instances_states(conn, format=None):

    if format=='dict':
        states_instances = {}
        for res in conn.get_all_instances():
            for inst in res.instances:
                states_instances[inst.id] = inst.state
        #print(states_instances)
        return states_instances

    else:
        for res in conn.get_all_instances():
            for inst in res.instances:
                if 'Name' in inst.tags:
                    print("{} ({}) [{}]".format(
                        inst.tags['Name'], inst.id, inst.state))
                else:
                    print("{} [{}]".format(inst.id, inst.state))


def get_instances_to_start( current_state_instances, schedule_instances, current_time):
    
    resu = []

    ignored_instances = get_ignored_instances()

    for instance_id in list(schedule_instances.keys()):

        try:
            current_state_instances[instance_id]
        except:
            #print('(start) Instance id ',instance_id, ' not found at ', current_time)
            continue

        if current_state_instances[instance_id]=='running':
            #print(instance_id, 'is running')
            pass

        elif(instance_id in  ignored_instances["ignored"]): 
            #print(instance_id, 'is ignored')
            pass
        else:
            start_time  = datetime.datetime.strptime(schedule_instances[instance_id]['start'],'%H:%M:%S').time()
            stop_time   = datetime.datetime.strptime(schedule_instances[instance_id]['stop'],'%H:%M:%S').time()
            
            if (start_time.hour == current_time.hour):
                resu.append(instance_id)
            #else:
                #print(schedule_instances[instance_id], 'not due')
                #pass
    return resu

def get_instances_to_stop(current_state_instances, schedule_instances, current_time):
    
    resu = []

    instances_off_schedule = get_instances_off_schedule()
    ignored_instances = get_ignored_instances()

    for instance_id in list(schedule_instances.keys()):

        try:
            current_state_instances[instance_id]
        except:            
            #print('(stop) Instance id ',instance_id, ' not found at ', current_time)
            continue

        if current_state_instances[instance_id]=='stopped':
            #print(instance_id, 'is stopped')
            pass

        elif(instance_id in  ignored_instances["ignored"]): 
            #print(instance_id, 'is ignored')
            pass

        else:
            start_time  = datetime.datetime.strptime(schedule_instances[instance_id]['start'],'%H:%M:%S').time()
            stop_time   = datetime.datetime.strptime(schedule_instances[instance_id]['stop'],'%H:%M:%S').time()
            
            if (current_time.hour == stop_time.hour):
                resu.append(instance_id)

            elif (current_time.hour > stop_time.hour):
                instances_off_schedule.append(instance_id)
                print(instance_id, 'is off scheduled at ', datetime.datetime.now())

            else:
                pass

    if len(instances_off_schedule) > 0:
        with open('instance_off_schedule.tmp','wb') as f:
            pickle.dump(instances_off_schedule,f)

    return resu

## AUXILIARY FUNCTIONS

def get_ignored_instances():

    try:
        with open('instances.ignore') as json_data:
            ignored_instances = json.load(json_data)
    except:
        ignored_instances=[]

    return ignored_instances

def get_instances_off_schedule():

    try:
        with open('instance_off_schedule.tmp','rb') as f:
            instances_off_schedule = pickle.load(f)
    except:
        instances_off_schedule = []

    return instances_off_schedule