Note: all examples assume module `pnutpy` has been imported!
Generally `meta` will contain the response metadata
Some API calls are [paginated](https://pnut.io/docs/api/implementation/pagination)
Some calls accept additional parameters. See pnutpy.consts or [the official docs](https://pnut.io/docs/api/resources/posts#general-post-parameters). (A list like this exists for thr others too) For sample usage see [Retrieving posts](#retrieving-posts)

# Authentication
    pnutpy.api.add_authorization_token(<Auth_Token>)

# Posting

`post` will contain the post object(s). Post IDs can be strings or integers.

## Creating posts

For possible `post_data` entries see the [pnut.io docs](https://pnut.io/docs/api/resources/posts/lifecycle#post-posts)

    post_data = {'text':'Hello pnut.io from pnutpy!'}
    post, meta = pnutpy.api.create_post(data=post_data)

## Reposting and unreposting

    post_id = 12345
    #Repost it
    response, meta = pnutpy.api.repost_post(post_id)
    #Unrepost it
    response, meta = pnutpy.api.unrepost_post(post_id)

## Bookmarking and unbookmarking

    post_id = 12345
    #Bookmark it
    response, meta = pnutpy.api.bookmark_post(post_id)
    #Unbookmark it
    response, meta = pnutpy.api.unbookmark_post(post_id)

## Retrieving posts

    #A single post
    post_id = 12345
    post, meta = pnutpy.api.get_post(post_id, include_raw=True)
    
    #Multiple posts
    post_ids = [12345, 67890] #Alternative: post_ids = '12345,67890'
    post, meta = pnutpy.api.get_posts(post_id)
    
    user_id = 1

    #Posts by a given user
    post, meta = pnutpy.api.users_posts(user_id)

    #Posts bookmarked by a given user
    post, meta = pnutpy.api.users_bookmarked_posts(user_id)

    #Posts mentioning a given user
    post, meta = pnutpy.api.users_mentioned_posts(user_id)

    #Posts with a given hashtag
    hashtag = 'MondayNightDanceParty' #Don't include the '#'
    post, meta = pnutpy.api.posts_with_hashtag(hashtag)

    #Posts in the thread for the post with the ID post_id
    post, meta = pnutpy.api.posts_thread(post_id)
    
    #Posts in the authorized user's timeline, that is: Posts by themselves ad the users they follow
    post, meta = pnutpy.api.users_post_streams_me()

    #Unified stream: Timeline + posts mentioning them
    post, meta = pnutpy.api.users_post_streams_unified()

    #Global stream: All public posts (with a few exceptions regarding bots etc)
    post, meta = pnutpy.api.users_post_streams_global()

## Deleting posts

    post_id = 12345
    post, meta = pnutpy.api.delete_post(post_id, include_raw=True)

# Users

Note: `user_id` is either a string '@username' or their integer id

## Retrieving users

    #Get user profile data
    response, meta = pnutpy.api.get_user(user_id)
    
    #Get multiple users
    user_ids = ['@hutattedonmyarm', 1] #Types can be mixed
    response, meta = pnutpy.api.get_users(ids=user_ids)

## Edit profile

    #Replace user profile, anything not included is removed
    response, meta = pnutpy.api.update_user('me', data=userobj)

    #Update only the specified parts of the user profile (name, text, timezone, and locale only)
    response, meta = pnutpy.api.patch_user('me', data=userobj)

    #Update avatar image
    response, meta = pnutpy.api.update_avatar('me', files={'avatar': ('filename.png', open('filename.png', 'rb',), 'image/png')})

    #Update cover image
    response, meta = pnutpy.api.update_cover('me', files={'cover': ('filename.png', open('filename.png', 'rb',), 'image/png')})

## Following, muting, blocking

    #Follows and unfollows a user
    response, meta = pnutpy.api.follow_user(user_id)
    response, meta = pnutpy.api.unfollow_user(user_id)
    
    #Blocks and unblocks a user
    response, meta = pnutpy.api.block_user(user_id)
    response, meta = pnutpy.api.unblock_user(user_id)

    #Mutes and unmutes a user
    response, meta = pnutpy.api.mute_user(user_id)
    response, meta = pnutpy.api.unmute_user(user_id)

## Get following, follwers, muted users, blocked users

    #Get users user_id is following
    response, meta = pnutpy.api.users_following('@hutattedonmyarm')
    #Get users who follow user_id
    response, meta = pnutpy.api.users_followers('@hutattedonmyarm')
    #Get users user_id has muted
    response, meta = pnutpy.api.users_muted_users('@hutattedonmyarm')
    #Get user IDs of users user_id has muted
    response, meta = pnutpy.api.users_muted_users_ids('@hutattedonmyarm')
    #Get users user_id has blocked
    response, meta = pnutpy.api.users_blocked_users('@hutattedonmyarm')


# Channels and PMs

`channel_id` is always the ID of the channel as string like '1' or integer.

## Retrieving channels 

This uses `subscribed_channels` as an example, but other channel-retrieving functions work similarly. Here's an overview:

* `get_channel(1) #Gets channel with ID 1`
* `get_channels(ids=[1,2,3]) #Gets channels with IDs 1, 2, and 3`
* `users_channels() #Gets channels created by the authorized user`
* `muted_channels() #Gets channels muted by the authorized user`


This includes *all* types of channels: PMs, chat channels, and channels with user created types. However, you can request only certain types like this:

    response, meta = pnutpy.api.subscribed_channels(channel_types='io.pnut.core.pm,com.example.site')


    #Retrieve all channels the authorized user is subscribed to
    response, meta = pnutpy.api.subscribed_channels(include_raw=True)
    
    #Prints some info about the retrieved channels
    for channel in response:
    print("Channel " + channel['id'])
    channel_raw = channel.get('raw')
    if channel_raw is not None:
        #Iterate through raws (a channel can have multiple)
        for raw in channel_raw:
                raw_type = raw.get('type')
                print('Raw type: ' + str(raw_type))
                raw_value = raw.get('value')
                print('Raw value: ' + str(raw_value))
                #Print channel name if it exists
                if raw_value is not None and raw_type is 'io.pnut.core.chat-settings' and 'name' in raw_value:
                    channel_name = raw_value.get('name')
                    print('Name: ' + channel_name)
    print("")
    

## Creating channels

This is merely an example ACL, for full ACL (access control list) options see [the docs](https://pnut.io/docs/api/how-to/channels-acl). Note that `immutable:False` is default behaviour, but included anyways for demo purposes

    #ACL
    #Array of user_ids with full access (read, write, manage)
    full_users = ['@username']
    #ACL for full user access
    full = {'immutable':False, 'you':True, 'user_ids':full_users}
    #Array of user_ids with write access (read, write)
    write_users = ['@another_username']
    #ACL for full write access
    write = {'immutable':False, 'you':True, 'any_user':False, 'user_ids':write_users}
    #ACL for full read access
    read = {'immutable':False, 'public': True, 'any_user':True}
    #Final ACL dictionary
    acl = {'full':full, 'write':write, 'read':read}

    #'io.pnut.core.chat' (aka regular chat channels) need the channel name as additional info
    raw_value = {'name':'New users'}
    raw = [{'type':'io.pnut.core.chat-settings', 'value':raw_value}]

    #Everything pieced together
    channel_info = {'type':'io.pnut.core.chat' , 'acl':acl, 'raw': raw}

    response, meta = pnutpy.api.create_channel(data=channel_info)

## Editing/Updating channels

This removes @username as full user, and adds @username1 and @username2. Read and Write ACLs will not be modified.

    full_users = ['@username1', '@username2']
    full = {'immutable':False, 'you':True, 'user_ids':full_users}
    acl = {'full':full}

    channel_info = {'acl':acl}
    response, meta = pnutpy.api.update_channel(channel_id,data=channel_info)

## (Un-)Subscribing and (un-)muting

* `subscribe_channel(channel_id)` subscribes to a channel
* `unsubscribe_channel(channel_id)` unsubscribes from a channel
* `subscribed_users` gets all users subscribed to a channel
* `mute_channel(channel_id)` mutes a channel
* `unmute_channel(channel_id)` unmutes a channel
* `muted_channels()` gets all muted channels

## Private messages (PMs)

PMs are a bit different, yet similar. They are basically channels with a type of `io.pnut.core.pm`. Their creation is handled by pnut.io, they're immutable, and the owner is irrelevant.

The number of unread PM channels can be retrieved by calling `pnutpy.api.num_unread_pm_channels()`.

Sending PMs can be done in one of two ways: Either by creating a message in the appropriate channel, or by creating a special message in a channel with the ID 'pm' like this:

    #Note: You can send the same message to multiple recipients. 'destinations' is an array!
    message_info = {'text':'This is a message', 'destinations':[user_id]}
    response, meta = pnutpy.api.create_message('pm', data=message_info)

Channel info for existing PM channels can be retrieved via `response, meta = pnutpy.api.existing_pm(ids='1')`, but note that this is a recent addition to the library by me, so ids must be a comma-separated string of user ids.

Retrieving PMs is identical to retrieving messages in a regular channel.

## Messages

**TODO**

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

## Getting files

    #One file
    file_id = 1234567890
    pnut_file, meta = pnutpy.api.get_file(file_id)
    #Multiple files
    file_ids = [12345, 67890] #Alternative: file_ids = '12345,67890'
    pnut_file, meta = pnutpy.api.get_files(ids=file_ids)
    #Retrieves all files of the authorized user
    pnut_file, meta = pnutpy.api.get_my_files()




    

