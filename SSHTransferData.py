import paramiko
import argparse
import os
from tqdm import tqdm

########################################################################
class transfer_data(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, host, username, password, port=22):
        """Initialize and setup connection"""
        self.sftp = None
        self.sftp_open = False
 
        # open SSH Transport stream
        self.transport = paramiko.Transport((host, port))
 
        self.transport.connect(username=username, password=password)
 
    #----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True
 
    #----------------------------------------------------------------------
    def get(self, remote_path, local_path=None):
        """
        Copies a file from the remote host to the local host.
        """
        self._openSFTPConnection()        
        self.sftp.get(remote_path, local_path)        
 
    #----------------------------------------------------------------------
    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)
 
    #----------------------------------------------------------------------
    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()

 

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-p','--origin',help='pathdir file origin',required=True)
    ap.add_argument('-pp','--dst',help='pathdir file transfer',required=True)
    ap.add_argument('-host','--hostname',help='hostname',required=False)
    ap.add_argument('-file','--filename',help='filename',required=True,default='all')

    arg = ap.parse_args()
    filename = arg.filename
    host = arg.hostname
    ssh = transfer_data(host, 'your_username', 'password')
    ori=arg.origin
    ds=arg.dst
    origin = '{}/{}'.format(ori,filename)
    dst = '{}/{}'.format(ds,filename)

    print('transfer file from {} to hostname: {} {}'.format(origin,host,dst))
	
    if filename=='all':
        for file in tqdm(os.listdir(ori)):
            try:
                ssh.put('{}/{}'.format(ori,file), '{}/{}'.format(ds,file))
            except:
                print ('\n {} cant be transfer, because that is folder'.format(file))
        print ('\nall data has been transferred')
		
    else :
        ssh.put(origin, dst)
        print('\n{} has been transferred'.format(filename))
    
    ssh.close()

