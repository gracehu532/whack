# collects resumes from a csv of names, emails and resumes
# for use of WHACK Fall 2015

import csv
import urllib
from apiclient import errors
from apiclient import http

def print_file_metadata(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  try:
    file = service.files().get(fileId=file_id).execute()

    print 'Title: %s' % file['title']
    print 'MIME type: %s' % file['mimeType']
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def print_file_content(service, file_id):
  """Print a file's content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file.

  Returns:
    File's content if successful, None otherwise.
  """
  try:
    print service.files().get_media(fileId=file_id).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def download_file(service, file_id, local_fd):
  """Download a Drive file's content to the local filesystem.

  Args:
    service: Drive API Service instance.
    file_id: ID of the Drive file that will downloaded.
    local_fd: io.Base or file object, the stream that the Drive file's
        contents will be written to.
  """
  request = service.files().get_media(fileId=file_id)
  media_request = http.MediaIoBaseDownload(local_fd, request)

  while True:
    try:
      download_progress, done = media_request.next_chunk()
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      return
    if download_progress:
      print 'Download Progress: %d%%' % int(download_progress.progress() * 100)
    if done:
      print 'Download Complete'
      return

resumeFileName = 'resumes.csv'

with open('resumes.csv', 'rb') as openresumes:
  resumereader = csv.DictReader(openresumes)
  for row in resumereader:
    name = row['Name']
    comboName = name.replace(' ', '')
    email = row['Email']
    resumelink = row['Link to resume']

    if 'http' in resumelink:
    	if 'google' in resumelink:
    		idx_id_start = '/d/'.find(resumelink) + 3
    		idx_id_end = '/'.find(resumelink[idx_id_start:])
    		g_id = resumelink[idx_id_start:idx_id_end]

    		download_file(file_id=g_id)
    	else: 
    		urllib.urlretrieve(row['Link to resume'], comboName + ".pdf")


