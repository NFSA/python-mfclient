import mfclient

if __name__ == '__main__':
    # create connection object (NOTE: You need to substitute with your token and your mediaflux server details.)
    connection = mfclient.MFConnection(host='mediaflux.your-domain.org', port=443, transport='https', token='XXX_YOUR_TOKEN_XXX')
    try:
        # connect to mediaflux server
        connection.open()

        # run server.version service
        result = connection.execute('server.version')

        # print result xml
        print(result)

        # print server version
        print(result.value('version'))
    finally:
        connection.close()