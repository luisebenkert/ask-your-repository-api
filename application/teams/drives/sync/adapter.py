import io

import magic
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from werkzeug.datastructures import FileStorage


class DriveAdapter:
    def __init__(self, credentials, http=None):
        self.service = self.drive_service(credentials, http)

    def drive_service(self, credentials, http=None):
        if http:
            return build("drive", "v3", http=http)
        else:
            return build("drive", "v3", credentials=credentials)

    def list_images(self, drive_id):
        result = (
            self.service.files().list(q=f"mimeType contains 'image' and parents='{drive_id}'", fields="*").execute()
        )
        return result.get("files")

    def download_file(self, file_id, filename):
        request = self.service.files().get_media(fileId=file_id)
        file = FileStorage(io.BytesIO(), filename=filename)
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        file.seek(0)
        return file

    def start_page_token(self):
        result = self.service.changes().getStartPageToken().execute()
        return result.get("startPageToken")

    def get(self, file_id):
        result = self.service.files().get(file_id).execute()
        return result

    def upload_file(self, filename, parent_folder):
        file_metadata = {"name": filename, "parents": [parent_folder]}
        filepath = f"uploads/{filename}"
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(filepath)
        media = MediaFileUpload(f"uploads/{filename}", mimetype=mime_type)
        file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return file["id"]

    def add_properties_to_file(self, file_id, **properties):
        file_metadata = {"appProperties": properties}
        self.service.files().update(fileId=file_id, body=file_metadata).execute()

    def delete_file(self, drive_file_id):
        try:
            self.service.files().delete(fileId=drive_file_id).execute()
        except Exception:
            pass
            # probably just a 404 that doesn't matter

    def compute_changes(self, initial_page_token, handle_change):
        page_token = initial_page_token
        i = 0
        while page_token is not None:
            response = self.service.changes().list(pageToken=page_token, fields="*", spaces="drive").execute()
            i += 1
            changes = response.get("changes")
            page_token = response.get("nextPageToken")
            for change in changes:
                handle_change(change)

            if "newStartPageToken" in response:
                return response.get("newStartPageToken")
