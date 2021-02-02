'''
    Author: Husnul

'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from dateutil.relativedelta import relativedelta
import glob, os, time
import util

def auth():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile('mycreds.txt')
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    return drive

def createFolder(root_id, drive, title):
    print(f'Creating folder: {title}')
    data = {
        'title': title,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': root_id}]
    }
    new_folder = drive.CreateFile(data)
    new_folder.Upload()

def getFolderId(root_id, drive, title):
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(root_id)}).GetList()
    for file in file_list:
        if title in file['title']:
            return file['id']
            break

def getSelfLink(root_id, drive, title):
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(root_id)}).GetList()
    for file in file_list:
        if title in file['title']:
            return file['alternateLink']
            break

def uploadPdf(path, drive, title):
    id = getFolderId(root_id, drive, title)
    for file_name in glob.glob(f'{path}/*.pdf'):
        exact_name = file_name.rsplit('/', 1)[1]
        data = {
            'title': exact_name,
            'parents': [{'id': id}]
        }
        drive = auth()
        file = drive.CreateFile(data)
        file.SetContentFile(file_name)
        print(f'uploading {exact_name}')
        file.Upload()

    print('All done, starting send mail\n')

if __name__ == '__main__':
    title = (datetime.today() - relativedelta(month=1)).strftime('%B %Y')
    root_id = '{root_id}'
    path = "{path}"

    drive = auth()
    createFolder(root_id, drive, title)
    uploadPdf(path, drive, title)

    link = getSelfLink(root_id, drive, title)
    util.sendMail(link)
    util.removeTemp(path)

