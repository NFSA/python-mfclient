import mfclient
import unittest
import tempfile
import os

_HOST = 'mediaflux-test.researchsoftware.unimelb.edu.au'
_PORT = 8443
_TRANSPORT = 'https'
_DOMAIN = 'system'
_USER = 'manager'
_PASSWORD = 'PASSWORD'
_FILE_SIZE = 1024


class ServerConnectionTest(unittest.TestCase):
    def setUp(self):
        self._connection = mfclient.MFConnection(host=_HOST, port=_PORT, transport=_TRANSPORT, domain=_DOMAIN,
                                                 user=_USER, password=_PASSWORD)
        self._connection.open()

        # create temp dir
        self._tmp_dir = tempfile.mkdtemp(prefix='python-mfclient.')

        # generate temp input file
        self._input_file_descriptor, self._input_file_path = tempfile.mkstemp(prefix='test-upload.', dir=self._tmp_dir)
        with open(self._input_file_path, "wb") as f:
            f.write(os.urandom(_FILE_SIZE))

        print('Generated input file: ' + self._input_file_path)

        # compute crc32
        self._input_file_crc32 = mfclient._crc32(self._input_file_path)

        print('CRC32 of input file: ' + str(self._input_file_crc32))

        # generate temp output file
        self._output_file_descriptor, self._output_file_path = tempfile.mkstemp(prefix='test-download.', dir=self._tmp_dir)

    def test_asset_create(self):
        # print server version
        mf_server_version = self._connection.execute('server.version').value('version')
        print('Server version: ' + mf_server_version)

        # upload (asset.create)
        asset_id = self._connection.execute('asset.create', args=None,
                                            inputs=[mfclient.MFInput(self._input_file_path)]).value('id')
        print('Created asset: ' + asset_id)

        # download (asset.get)
        ae = self._connection.execute('asset.get', '<args><id>' + asset_id + '</id></args>', None,
                                      mfclient.MFOutput(self._output_file_path)).element('asset')

        print('Asset content CRC32: ' + ae.value("content/csum[@base='10']"))

        # compute crc32 of downloaded file
        self._output_file_crc32 = mfclient._crc32(self._output_file_path)

        print('CRC32 of output file: ' + str(self._output_file_crc32))

        # delete the asset (on the server)
        self._connection.execute('asset.destroy', '<args><id>' + asset_id + '</id></args>')
        print('Deleted asset: ' + asset_id)

    def tearDown(self):
        os.close(self._input_file_descriptor)
        os.close(self._output_file_descriptor)
        os.remove(self._input_file_path)
        os.remove(self._output_file_path)
        os.rmdir(self._tmp_dir)
        self._connection.close()


if __name__ == '__main__':
    unittest.main()
