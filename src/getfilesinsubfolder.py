import math

import mfclient

# variables to change
base_folder = '/projects/proj-5070_prescient-1128.4.380/'
subfolders = ['PrescientBM','PrescientAD']
file_formats = ['.wav','.WAV','.mp4','.MP4']

domain = 'unimelb'
user = 'auser'
password = 'password'
if __name__ == '__main__':
    # create connection object (NOTE: You need to substitute with your server details.)
    connection = mfclient.MFConnection(host='mediaflux.researchsoftware.unimelb.edu.au', port=443, transport='https', domain=domain,
                                       user=user, password=password)
    try:
        total_count = 0
        connection.open()
        format_string = ""
        for format_i in file_formats:
            strf = "name ends with '{}' or ".format(format_i)
            format_string += strf
        format_string = format_string.strip("or ")
        for folder in subfolders:
            w = mfclient.XmlStringWriter('args')
            where = "namespace>='{}/{}_Interviews/PSYCHS' and ({})".format(base_folder+folder,folder,format_string)
            w.add('where',where)
            w.add('action','count')
            count = connection.execute('asset.query', w.doc_text())
            # print(count.value("value"))
            total_count += int(count.value("value"))
        print("Count is {}".format(total_count))
    except:
        raise
        pass
