import os
import dropbox
from io import BytesIO
from zipfile import ZipFile

dbx = dropbox.Dropbox("wkDhUoxQ_rcAAAAAAAAAAS5CFpq4aIPxMWfKCKnlsSnjRUs8qw9Zim73ooJ2Ihbc")
#dbx.users_get_current_account()

# with open("C:\\Users\\libor\\Downloads\\00104065_504665_20210325_084908_Faktura.PDF","rb") as f:
#                 dbx.files_upload(f.read(), "/test_fa.pdf", mute=True)


# Tohle taky funguje
# with open(r"C:\Users\libor\Dropbox\python\InvoiceApp\Data\testFA.pdf","wb") as w:
#     metadata, res = dbx.files_download(path="/test_fa.pdf")
#     w.write(res.content)

# dbx.files_download_to_file(r"C:\Users\libor\Dropbox\python\InvoiceApp\Data\testFA1.pdf","/test_fa.pdf")

filePath = "C:\\Users\\libor\\Downloads\\B2LEDN01_T_N.csv.zip"
with open(filePath,"rb") as f:
    with ZipFile(BytesIO(f.read())) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            dropBoxPath = "/" + contained_file
            dbx.files_upload(my_zip_file.open(contained_file).read(),dropBoxPath, mute=True)
            # with open(("C:\\Users\\libor\\Downloads\\unzipped_and_read_" + contained_file), "wb") as output:
            #         output.write(my_zip_file.open(contained_file).read())

# with open(("unzipped_and_read_" + contained_file + ".file"), "wb") as output:
        # for line in my_zip_file.open(contained_file).readlines():
        #     print(line)
            # output.write(line)