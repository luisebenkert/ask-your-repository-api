from expects import equal
from expects import expect
from googleapiclient.http import HttpMockSequence
from mamba import description, before, it, after

from application.teams.placeholder_drives.drive import Drive
from application.teams.placeholder_drives.sync import Sync
from specs.factories.image_recognition import mock_image_recognition
from specs.spec_helpers import Context
from specs.factories.drive_factory import DriveFactory
from neomodel import db


def file_content(path):
    asdf = open(path, "rb").read()
    return asdf


def build_http_mock_array_for_change(change_file):
    http = [
        ({"status": 200}, file_content("specs/fixtures/drive/drive-discovery.json")),
        ({"status": 200}, file_content("specs/fixtures/drive/drive-discovery.json")),
        ({"status": 200}, file_content("specs/fixtures/drive/start_page_token.json")),
        ({"status": 200}, file_content(f"specs/fixtures/drive/{change_file}")),
    ]
    return http


def build_http_mock_for_change(change_file):
    return HttpMockSequence(build_http_mock_array_for_change(change_file))


with description("drive") as self:
    with before.each:
        self.context = Context()

    with after.each:
        db.cypher_query("MATCH (a) DETACH DELETE a")

    # generating discovery file:
    #        with open("drive-discovery.json", "w") as f:
    #            f.write(_retrieve_discovery_doc("https://www.googleapis.com/discovery/v1/apis/drive/v3/rest", build_http(), cache_discovery=False))

    with description("Syncing drive changes"):
        with before.each:
            self.drive = DriveFactory.create_drive()

        with description("Change: nothing changed"):
            with before.each:
                with mock_image_recognition:
                    http = build_http_mock_for_change("changes_response_no_changes.json")
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("asdf"):
                pass

        with description("Change: new image in correct folder"):
            with before.each:
                with mock_image_recognition:
                    mock_array = build_http_mock_array_for_change("changes_response_new_file_correct_folder.json")
                    mock_array.append(({"status": 200}, file_content("specs/fixtures/drive/meh.png")))
                    http = HttpMockSequence(mock_array)
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("has an artifact connected"):
                print(self.drive.owner.single().teams.single().artifacts.all())
                expect(len(self.drive.files.all())).to(equal(1))

        with description("Change: new file wrong format"):
            with before.each:
                with mock_image_recognition:
                    http = build_http_mock_for_change("changes_response_new_file_wrong_format.json")
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("asdf"):
                pass

        with description("Change: new file incorrect folder"):
            with before.each:
                with mock_image_recognition:
                    http = build_http_mock_for_change("changes_response_new_file_incorrect_folder.json")
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("asdf"):
                pass

        with description("Change: deleted file correct folder"):
            with before.each:
                with mock_image_recognition:
                    http = build_http_mock_for_change("changes_response_deleted_file_correct_folder.json")
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("asdf"):
                pass

        with description("Change: deleted file incorrect folder"):
            with before.each:
                with mock_image_recognition:
                    http = build_http_mock_for_change("changes_response_deleted_file_wrong_format.json")
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("asdf"):
                pass

        with description("Change: deleted file wrong format"):
            with before.each:
                with mock_image_recognition:
                    http = build_http_mock_for_change("changes_response_deleted_file_wrong_folder.json")
                    sync = Sync(self.drive, http)
                    sync.sync_from_drive()

            with it("asdf"):
                pass

    # with it("Downloads a new image"):
    # with open("drive-discovery.json", "w") as f:
    #        f.write(_retrieve_discovery_doc("https://www.googleapis.com/discovery/v1/apis/drive/v3/rest", build_http(), cache_discovery=False))

    """
        sync to drive changes:
            # downloads new images
            # deletes deleted images
            # initializes sync if no sync started yet
        
        uploads changes:
            # Creating by artifact uploads file to google drive with correct name
            # Deleting af file by id deletes it on google drive and disconnects artifact
            
    """
