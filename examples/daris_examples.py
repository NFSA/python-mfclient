import mfclient

MF_HOST = 'mediaflux.researchsoftware.unimelb.edu.au'
MF_PORT = 443
MF_TRANSPORT = 'https'
MF_DOMAIN = 'aaf'
MF_USER = 'unimelb:_USERNAME_'
MF_PASSWORD = '_PASSWORD_'

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


if __name__ == '__main__':
    find_scan_by_date('1-May-2018')
