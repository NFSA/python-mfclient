import math

import mfclient
import pandas as pd

# expects csv file of format:
# email,	proj-a-1128.4.218,	proj-b-1128.4.217
# usera.name@unimelb.edu.au,	participant-acm,	participant-acm
# userb.name@unimelb.edu.au,	administrator,	administrator
# where admin, particiapnt-x are the roles, to remove the person REMOVE is used instead of role,
# None or nan indicates dont add person to proj, don't remove either

# num of rows in the csv file to skip at start if needed
SKIP_ROWS = 0
DELIMITER = ','
EMAIL =False
if __name__ == '__main__':
    # create connection object (NOTE: You need to substitute with your server details.)
    connection = mfclient.MFConnection(host='mediaflux.researchsoftware.unimelb.edu.au', port=443, transport='https', domain='system',
                                       user='rajaramans', password='')
    try:
        # connect to mediaflux server
        connection.open()

        # run server.version service
        result = connection.execute('server.version')

        # print result xml
        print(result)

        # print server version
        print(result.value('version'))
        users = pd.read_csv("/Users/rajaramans/PycharmProjects/python-mfclient/proj-add1.csv",skiprows=SKIP_ROWS,delimiter=DELIMITER)
        email_col = 'email'
        user_col = 'user'
        main_domain = 'unimelb'
        project_cols = []
        for i in list(users.columns):
            if i.startswith("proj"):
                project_cols.append(i)
        print(project_cols)
        for row in range(users.shape[0]):
            if EMAIL:
                w = mfclient.XmlStringWriter('args')
                w.add('email', users[email_col][row])
                user = connection.execute('unimelb.user.search', w.doc_text())
                domain = user.value('user/@domain')
                username = user.value('user/@user')
            else:
                username = users[user_col][row]
                domain = main_domain
            #print(user)
            print("{} {} {}".format(users[email_col][row],username,domain))
            if username is None:
                continue
            for proj in project_cols:
                role = users[proj][row]
                print("{} {}".format(proj, role))
                if type(role) == type(float('nan')) and math.isnan(role):
                    continue
                role = role.strip()
                role = role.strip("\n")

                if role == "None" or role is None or role == "":
                    pass
                if role == "REMOVE":
                    projadd = mfclient.XmlStringWriter('args')
                    projadd.add('domain', domain)
                    projadd.add('user', username)
                    projadd.add('project-id', proj)
                    remove = connection.execute('vicnode.project.user.remove',projadd.doc_text())
                    print(remove)
                else:
                    projadd = mfclient.XmlStringWriter('args')
                    projadd.add('domain',domain)
                    projadd.add('user',username)
                    projadd.add('project-role',role,{"replace":True})
                    projadd.add('project-id',proj)
                    role = connection.execute('vicnode.project.user.add',projadd.doc_text())
                    #print(role)

        print(users)
    finally:
        connection.close()