import json
import random
import urllib.request
import yaml


def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type": "application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]


def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})


config = yaml.safe_load(
    open("/opt/odoo15/pjts/learn/repo/open_academy/rpc/connection_conf.yml"))

url = 'http://%s:%d/jsonrpc' % (config['host'], config['port'])

uid = call(url, "common", "login",
           config['db'], config['user'], config['pass'])


sessions = call(url, "object", "execute", config['db'], uid, config['pass'],
                "open_academy.session", 'search_read', [], ['name', 'number_of_seats'])
for cur_session in sessions:
    print(cur_session)

create_new_session = input('For creating new session, type Y\n')

new_session_name = ''
new_session_number_of_seats = 0

if create_new_session == 'Y':
    while new_session_name == '':
        new_session_name = input('Enter sessions name\n')
        if new_session_name == '':
            print('Incorrect name, try again please!')
            continue

        new_session_number_of_seats = input('Enter the number of seats\n')
        if new_session_number_of_seats == '':
            new_session_number_of_seats = 0
        else:
            new_session_number_of_seats = int(new_session_number_of_seats)

        courses_list_id = []
        print('Evaliable courses!')
        courses = call(url, "object", "execute", config['db'], uid, config['pass'], "open_academy.course", 'search_read', [],
                       ['name'])
        for cur_course in courses:
            courses_list_id.append(cur_course['id'])
            print(cur_course)

        in_course_id = False
        course_id = 0
        while not in_course_id:
            course_id = int(
                input('Enter the course id, you are interested \n'))
            if course_id in courses_list_id:
                in_course_id = True
            else:
                print('Course id is incorrect, try again')

        args = [
            {'name': new_session_name,
             'course_id': course_id,
             'number_of_seats': new_session_number_of_seats
             }
        ]

        new_session_id = call(
            url, 'object', 'execute', config['db'], uid, config['pass'], 'open_academy.session', 'create', args)

        print('New session created')

else:
    print("Creating of session cancelled")
