import pysftp
import ftplib
import os
mysftpHostname = os.environ['mysftpHostname']
mysftpUsername = os.environ['mysftpUsername']
mysftpPassword = os.environ['mysftpPassword']
mysftpPort = 22
myftpHostname = os.environ['myftpHostname']
myftpUsername = os.environ['myftpUsername']
myftpPassword = os.environ['myftpPassword']

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


def lambda_handler(event, context):
    session = ftplib.FTP(myftpHostname, myftpUsername, myftpPassword)

    with pysftp.Connection(host=mysftpHostname, username=mysftpUsername, password=mysftpPassword, port=mysftpPort, cnopts=cnopts) as sftp:
        sftp.cwd('/directory/')
        directory_structure = sftp.listdir_attr()
        for attr in directory_structure:
            os.chdir('/tmp/')

            if (attr.filename).endswith('.xml'):
                print("Downloading SFTP:" + attr.filename)
                sftp.get(attr.filename)
                file = open(attr.filename, 'rb')
                session.storbinary("STOR " + attr.filename, file)
                file.close()
                os.remove(attr.filename)
                sftp.remove(attr.filename)
    session.quit()
    sftp.close()
