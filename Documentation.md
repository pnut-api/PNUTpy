Note: all examples assume module `pnutpy` has been imported!
Generally `meta` will contain the response metadata
# Authentication
    pnutpy.api.add_authorization_token(<Auth_Token>)

# Posting

# Users

# Files

**All file operations require authentication!**
`pnut_file` will contain the file object(s). File IDs can be strings or integers.

**TODO:** FILE_PARAMS

## Creating a file

Upload a new file to the user's storage

    #The file itself
    file = open('/path/to/file', 'r')
    
    #Required metadata
    file_type = 'com.example.filetype'
    file_name = 'filename.ext'
    file_kind = 'other' #Can be 'image' or 'other'
    
    #Optional metadata (include it in file_data)
    is_public = False
    mime_type = 'text/plain'
    sha256 = <sha256 hash> #API will reject if it doesn't match with the actual sha256 hash
    
    file_data = {'type': file_type, 'kind': file_kind, 'name': file_name}
    
    #Creating the file
    pnut_file, meta = pnutpy.api.create_file(files={'content':file}, data=file_data)

## Updating a file

Update an existing file. Only *name*, *is_public*, and *raw* can be updated

    file_name = 'new_filename.ext'
    is_public = True
    file_data = {'name':file_name, 'is_public': is_public}
    file_id = 1234567890
    pnut_file, meta = pnutpy.api.update_file(file_id, data=file_data)

## Getting a file

Retrieves a file.

    file_id = 1234567890
    pnut_file, meta = pnutpy.api.get_file(file_id)

## Getting multiple files

Retrieves multiple files

    file_ids = [12345, 67890] #Alternative: file_ids = '12345,67890'
    pnut_file, meta = pnutpy.api.get_files(ids=file_ids)

## Get my files

Retrieves all files of the authorized user

    pnut_file, meta = pnutpy.api.get_my_files()




    

