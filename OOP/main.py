import json
from datetime import datetime
from functools import cmp_to_key
import argparse
import os
import sys

class HealthIns:

    def __init__(self, current_health=0, max_sev=0):
        self.current_health = current_health
        self.max_sev = max_sev
        self.display_health = "Healthy" if int(self.current_health) == 100 else "Unhealthy"

class CloudCtx:

    def __init__(self, name='', tenant_name='',
                 description='', name_alias='',
                 ctx_profile_name='', health_ins=HealthIns(),
                 mod_ts = ''):

        CloudCtx.no_instances += 1
        self.name = name
        self.tenant_name = tenant_name
        self.description = description
        self.name_alias = name_alias
        self.ctx_profile_name = ctx_profile_name
        self.health_ins = health_ins
        self.mod_ts = mod_ts

    def non_empty(self, name):
        '''returns '-' if the string is empty'''
        if name == "":
            return '-'
        else:
            return name

    def __repr__(self):
        return '\n CloudCtx:\n' + ' name: ' + self.non_empty(self.name) + \
              '\n tenant_name: ' + self.non_empty(self.tenant_name) + \
              '\n description: ' + self.non_empty(self.description) + \
              '\n name_alias: ' + self.non_empty(self.name_alias) + \
              '\n ctx_profile_name: ' + self.non_empty(self.ctx_profile_name) + \
              '\n mod_ts: ' + self.non_empty(self.mod_ts) + \
              '\n \n HealthInst:\n' + ' current_health: ' + str(self.health_ins.current_health) + \
              '\n max_sev: ' + str(self.health_ins.max_sev) + \
              '\n display_health: ' + self.non_empty(self.health_ins.display_health)

    @staticmethod
    def compare_health(obj1, obj2):
        first = int(obj1.health_ins.current_health)
        second = int(obj2.health_ins.current_health)
        if first < second:
            return -1
        elif first > second:
            return 1
        return 0


    @staticmethod
    def modify_date(mod_ts):
        date = mod_ts[:mod_ts.find("T")]
        time = mod_ts[mod_ts.find("T") + 1:mod_ts.find(".")]

        date_modified = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        date_modified += datetime.strptime(time, '%H:%M:%S').strftime(' %I:%M:%S %p')
        return date_modified

    @staticmethod
    def compare_dates(obj1, obj2):
        first_date = obj1.mod_ts
        second_date = obj2.mod_ts
        formatted_date1 = datetime.strptime(first_date, "%d-%m-%Y %I:%M:%S %p")
        formatted_date2 = datetime.strptime(second_date, "%d-%m-%Y %I:%M:%S %p")
        if formatted_date1 < formatted_date2:
            return 1
        elif formatted_date1 > formatted_date2:
            return -1
        return 0

    @staticmethod
    def create_instance(no, file):
        f = open(file,)
        data = json.load(f)
        objects = []

        if no > int(data['totalCount']):
            print("There are not enough!")

        for i in range(no):
            name = data['imdata'][i]['hcloudCtx']['attributes']['name']
            tenant_name = data['imdata'][i]['hcloudCtx']['attributes']['tenantName']
            description = data['imdata'][i]['hcloudCtx']['attributes']['description']
            name_alias = data['imdata'][i]['hcloudCtx']['attributes']['nameAlias']
            ctx_profile_name = data['imdata'][i]['hcloudCtx']['attributes']['ctxProfileName']
            mod_ts = data['imdata'][i]['hcloudCtx']['attributes']['modTs']
            mod_ts = CloudCtx.modify_date(mod_ts)

            if len(data['imdata'][i]['hcloudCtx']['children']) > 0:
                current_health = data['imdata'][i]['hcloudCtx']['children'][0]['healthInst']['attributes']['cur']
                max_sev = data['imdata'][i]['hcloudCtx']['children'][0]['healthInst']['attributes']['maxSev']
                child = HealthIns(current_health, max_sev)
            else:
                child = HealthIns()

            obj = CloudCtx(name, tenant_name, description, name_alias, ctx_profile_name, child, mod_ts)
            # print(obj.name, obj.tenant_name, obj.health_ins.display_health)
            objects.append(obj)

        return objects



if __name__ == '__main__':

    my_parser = argparse.ArgumentParser(description='The path to the json file')

    # Add the arguments
    my_parser.add_argument('Path',
                           metavar='path',
                           type=str,
                           help='the path to json file')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    input_path = args.Path

    if not os.path.isfile(input_path):
        print('The path specified does not exist')
        sys.exit()

    CloudCtx.no_instances = 0
    no = 6
    #instantiate the objects from json
    instances = CloudCtx.create_instance(no, input_path)
    # print(instances)

    # sort after health parameter
    print("Sorted after health parameter:")
    instances = sorted(instances, key=cmp_to_key(CloudCtx.compare_health))
    print(instances)

    print(CloudCtx.no_instances)

    # sorted after most recently modified
    print("Sorted after most recently modified parameter:")
    instances = sorted(instances, key=cmp_to_key(CloudCtx.compare_dates))
    print(instances)
