import math

import mfclient
import pandas as pd

# expects csv file of format:
# users
# usera.name@unimelb.edu.au


# num of rows in the csv file to skip at start if needed
SKIP_ROWS = 0
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
        users = pd.read_csv("/Users/rajaramans/Documents/users.csv",skiprows=SKIP_ROWS)
        usernames = []
        for row in range(users.shape[0]):
            w = mfclient.XmlStringWriter('args')
            w.add('email', users["users"][row])
            user = connection.execute('unimelb.user.search', w.doc_text())
            domain = user.value('user/@domain')
            username = user.value('user/@user')
            usernames.append(username)
        df = pd.DataFrame(usernames, columns=["colummn"])
        df.to_csv("/Users/rajaramans/Documents/usernames.csv")

    finally:
        connection.close()