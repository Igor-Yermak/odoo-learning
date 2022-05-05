import xmlrpc.client
import yaml

config = yaml.safe_load(
    open("/opt/odoo15/pjts/learn/repo/open_academy/rpc/connection_conf.yml"))

base_db_url = 'http://%s:%d/' % (config['host'], config['port'])

common_endpoint_url = base_db_url + 'xmlrpc/2/common'
common = xmlrpc.client.ServerProxy(common_endpoint_url)
common.version()

uid = common.authenticate(config['db'], config['user'], config['pass'], {})

models_url = base_db_url + 'xmlrpc/2/object'
models = xmlrpc.client.ServerProxy(models_url)

sessions = models.execute_kw(config['db'], uid, config['pass'], 'open_academy.session', 'search_read', [
                             []], {'fields': ['name', 'number_of_seats']})
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
        courses = models.execute_kw(
            config['db'], uid, config['pass'], 'open_academy.course', 'search_read', [[]], {'fields': ['name']})
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

        new_session_id = models.execute_kw(config['db'], uid, config['pass'], 'open_academy.session', 'create',
                                           [{'name': new_session_name, 'number_of_seats': new_session_number_of_seats, 'course_id': course_id}])

        new_sessions_read = models.execute_kw(config['db'], uid, config['pass'], 'open_academy.session', 'read', [new_session_id],
                                              {'fields': ['name', 'number_of_seats', 'course_id']})
        print('New session created')
        print(new_sessions_read)
else:
    print("Creating of session cancelled")
