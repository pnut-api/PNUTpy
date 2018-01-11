PAGINATION_PARAMS = [
    'since_id',
    'before_id',
    'count',
]


POST_PARAMS = [
    'include_deleted',
    'include_client',
    'include_counts',
    'include_html',
    'include_post_html',
    'include_bookmarked_by',
    'include_reposted_by',
    'include_directed_posts',
    'include_copy_mentions',
    'include_muted',
    'include_raw',
    'include_post_raw',
    'include_user',
    'include_user_html',
    'include_presence',
    'include_user_raw',
]


USER_PARAMS = [
    'include_html',
    'include_user_html',
    'include_counts',
    'include_user',
    'include_presence',
    'include_raw',
    'include_user_raw',
]


USER_SEARCH_PARAMS = [
    'q',
    'order',
    'locale',
    'timezone',
    'types'
]


POST_SEARCH_PARAMS = [
    'order',
    'q',
    'tags',
    'mentions',
    'leading_mentions',
    'links',
    'link_domains',
    'is_directed',
    'is_revised',
    'is_nsfw',
    'is_reply',
    'client_id',
    'creator_id',
    'reply_to',
    'thread_id',
    'user_types',
    'raw_types'
]


CHANNEL_PARAMS = [
    'include_read',
    'channel_types',
    'exclude_channel_types',
    'include_marker',
    'include_inactive',
    'include_raw',
    'include_channel_raw',
    'include_recent_message',
    'include_limited_users',
    'include_message_raw',
    'include_html',
    'include_user_html',
    'include_counts',
    'include_user',
    'include_presence',
    'include_user_raw',
    
]


CHANNEL_SEARCH_PARAMS = [
    'order',
    'categories',
    'channel_types',
    'raw_types',
    'exclude_channel_types',
    'is_private',
    'is_public',
    'owner_id'
]


MESSAGE_PARAMS = [
    'include_deleted',
    'include_html',
    'include_message_html',
    'include_raw',
    'include_message_raw',
    'include_client',
    'include_user_html',
    'include_counts',
    'include_user',
    'include_presence',
    'include_user_raw',
]


MESSAGE_SEARCH_PARAMS = [
    'channel_ids',
    'order',
    'q',
    'tags',
    'mentions',
    'leading_mentions',
    'links',
    'link_domains',
    'is_nsfw',
    'is_reply',
    'is_sticky',
    'client_id',
    'creator_id',
    'reply_to',
    'thread_id',
    'user_types',
    'raw_types'
]


FILE_PARAMS = [
    'file_types',
    'include_incomplete',
    'include_private',
    'include_raw',
    'include_file_raw',
    'include_html',
    'include_user_html',
    'include_counts',
    'include_user',
    'include_presence',
    'include_user_raw',
]


# PLACE_SEARCH_PARAMS = [
    # 'latitude',
    # 'longitude',
    # 'q',
    # 'radius',
    # 'count',
    # 'remove_closed',
    # 'altitude',
    # 'horizontal_accuracy',
    # 'vertical_accuracy',
# ]

# APP_STREAM_PARAMS = [
    # 'key',
# ]
