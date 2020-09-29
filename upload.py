from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys

job_id = sys.argv[1]
today = sys.argv[2]

gauth = GoogleAuth(f'{your_dir_loc}/client_secrets.json')
gauth.LoadCredentialsFile(f'{your_dir_loc}/mycreds.txt')
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

file = f'{file_dir_loc}'
filename = f'{filename_in_drive}'
file1= drive.CreateFile({'title': filename,'mimetype':'text/csv','parents': [{'id': '{your_folder_id}'}]})
file1.SetContentFile(file)
file1.Upload()
