# python-mfclient
Python Mediaflux Client.

### 1. Quick Start

  - 1) Check out [mfclient.py](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/raw/master/src/mfclient.py) from [GitLab](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient)

  - 2) import mfclient module into your python code and use the API to communicate with Mediaflux server.

  - 3) a simple example below shows how to
    - import the module, 
    - log into Mediaflux server using domain, username and password, 
    - execute a mediaflux service: server.uuid, which returns the Mediaflux server's UUID.


```python

import mfclient

if __name__ == '__main__':
    # create connection object
    connection = mfclient.MFConnection(host='mediaflux.your.org', port=443, transport='https', domain='your-domain',
                                       user='your-username', password='your-password')
    try:
        # connect to mediaflux server
        connection.open()

        # run server.version service
        result = connection.execute('server.version')

        # print result xml
        print(result)

        # print Mediaflux server version
        print(result.value('version'))
    finally:
        connection.close()

```

### 2. Examples

  - 1) [quick-start example](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/blob/master/examples/quick_start.py)
  - 2) [authenticate with token](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/-/blob/master/examples/connect_with_token.py)
  - 3) [create asset with metadata](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/blob/master/examples/manage_asset_metadata.py)
  - 4) [get asset metadata](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/blob/master/examples/manage_asset_metadata.py)
  - 5) [change asset metadata](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/blob/master/examples/manage_asset_metadata.py)
  - 6) [create asset with content (upload a file as an asset)](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/blob/master/examples/manage_asset_with_content.py)
  - 7) [get asset content (download asset content to local file system)](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/blob/master/examples/manage_asset_with_content.py)
  
  * See [more exmamples](https://gitlab.unimelb.edu.au/resplat-mediaflux/python-mfclient/tree/master/examples)

### 3. API Documentation
  * See [API documentation on readthedocs.io](http://python-mfclient.readthedocs.io/en/latest/source/mfclient.html#module-mfclient)
