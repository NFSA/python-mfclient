import mfclient

# MF_HOST = 'mediaflux.researchsoftware.unimelb.edu.au'
# MF_PORT = 443
# MF_TRANSPORT = 'https'
# MF_DOMAIN = 'aaf'
# MF_USER = 'unimelb:_USERNAME_'
# MF_PASSWORD = '_PASSWORD_'

MF_HOST = 'localhost'
MF_PORT = 8086
MF_TRANSPORT = 'http'
MF_DOMAIN = 'system'
MF_USER = 'manager'
MF_PASSWORD = 'change_me'

DARIS_WEB_URL = MF_TRANSPORT.lower() + '://' + MF_HOST.lower() + ':' + str(MF_PORT) + '/daris-web/'


def find_scan_by_date(date):
    """ Prints the DICOM studies scanned on the specified date.
    :param date: the scan date, in the format of 'dd-MMM-yyyy', e.g. '31-Jan-2017'
    :type date: str
    :return:
    """
    with mfclient.MFConnection(MF_HOST, MF_PORT, MF_TRANSPORT, domain=MF_DOMAIN, user=MF_USER,
                               password=MF_PASSWORD) as cxn:
        # the query string
        where = "xpath(mf-dicom-study/sdate)='" + date + "'"

        # the service arguments
        w = mfclient.XmlStringWriter('args')
        w.add('where', where)
        w.add('action', 'get-cid')
        w.add('size', 'infinity')

        # execute the query service
        re = cxn.execute('asset.query', w.doc_text())
        cids = re.values('cid')
        if cids:
            print('Found ' + str(len(cids)) + ' DICOM studies:')
            for cid in cids:
                print('\tDICOM study: ' + cid)
                print('\t\tView: ' + DARIS_WEB_URL + '/#view_' + cid)
        return cids


def download(cid, output_file_path, format='zip'):
    with mfclient.MFConnection(MF_HOST, MF_PORT, MF_TRANSPORT, domain=MF_DOMAIN, user=MF_USER,
                               password=MF_PASSWORD) as cxn:
        w = mfclient.XmlStringWriter('args')
        w.add('cid', cid)
        w.add('parts', 'content')
        w.add('format', format)
        output = mfclient.MFOutput(path=output_file_path)
        cxn.execute('daris.collection.archive.create', w.doc_text(),None, output);

def get_asset():
    with mfclient.MFConnection(MF_HOST, MF_PORT, MF_TRANSPORT, domain=MF_DOMAIN, user=MF_USER,
                               password=MF_PASSWORD) as cxn:
        w = mfclient.XmlStringWriter('args')
        w.add('id', 1084)
        output = mfclient.MFOutput(path='/tmp/1084.aar')
        cxn.execute('asset.get', w.doc_text(),None, output);


if __name__ == '__main__':
    # find_scan_by_date('1-May-2018')
    # get_asset()
    download('39.1.1.1.1.1', '/tmp/39.1.1.1.1.1.zip')

