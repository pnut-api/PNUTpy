import re
import requests

from pnutpy.consts import (PAGINATION_PARAMS, CHANNEL_PARAMS, MESSAGE_PARAMS, FILE_PARAMS, POST_PARAMS, POST_SEARCH_PARAMS,
    USER_PARAMS, USER_SEARCH_PARAMS, CHANNEL_SEARCH_PARAMS, MESSAGE_SEARCH_PARAMS)
from pnutpy.errors import (PnutAuthAPIException, PnutPermissionDenied, PnutMissing, PnutRateLimitAPIException,
                          PnutInsufficientStorageException, PnutAPIException, PnutError, PnutBadRequestAPIException)
from pnutpy.models import (SimpleValueModel, SimpleValueDictListMode, APIModel, Post, User, Channel, Message, ExploreStream, File, Interaction, Token, APIMeta)
from pnutpy.utils import json_encoder


class API(requests.Session):
    """
    The root API method

    Example::

        # To get an unauthenticated api object
        import pnutpy

        # pnutpy.api is an unauthenticated instance of the API object
        pnutpy.api.get_post(1)

        # To authenticate the API object, add an authorization token
        pnutpy.api.add_authorization_token(access_token='<access_token>')

        # Otherwise, you can construct an an authenticated api object
        my_api = pnutpy.API.build_api(access_token='<access_token>')

    """
    @classmethod
    def build_api(cls, api_root='https://api.pnut.io/v0', access_token=None, verify_ssl=True, extra_headers=None):
        api = cls()
        api.api_root = api_root
        if access_token:
            api.add_authorization_token(access_token)

        api.verify_ssl = verify_ssl
        api.headers.update(extra_headers if extra_headers else {})

        return api

    def request(self, method, url, raw_response=False, *args, **kwargs):
        if url:
            url = self.api_root + url

        kwargs['verify'] = self.verify_ssl
        headers = {}
        headers.update(self.headers)
        headers.update(kwargs.get('headers', {}))

        kwargs['headers'] = headers

        response = super(API, self).request(method, url, *args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            pass
        except Exception:
            raise PnutError()

        if response.status_code == 204 or raw_response:
            return response

        response = APIModel.from_string(response.content, self)

        if response.meta.code == 400:
            raise PnutBadRequestAPIException(response)

        if response.meta.code == 401:
            raise PnutAuthAPIException(response)

        if response.meta.code == 403:
            raise PnutPermissionDenied(response)

        if response.meta.code == 404:
            raise PnutMissing(response)

        if response.meta.code == 429:
            raise PnutRateLimitAPIException(response)

        if response.meta.code != 200 and response.meta.code != 201:
            raise PnutAPIException(response)

        return response

    def add_authorization_token(self, token):
        self.headers.update({
            'Authorization': 'Bearer %s' % (token),
        })

    def request_json(self, method, *args, **kwargs):
        kwargs.setdefault('headers', dict())
        kwargs['headers'].update({'Content-Type': 'application/json'})
        if kwargs.get('data'):
            kwargs['data'] = json_encoder(kwargs['data'])

        return self.request(method, *args, **kwargs)


re_path_template = re.compile('{\w+}')


def bind_api_method(func_name, path, payload_type=None, payload_list=False, allowed_params=None,
                    method='GET', require_auth=True, raw_response=False, content_type='JSON', extra_doc='', link='#'):
    allowed_params = allowed_params or []

    def run(self, *args, **kwargs):
        parameters = {}
        for key, val in list(kwargs.items()):
            if key in allowed_params:
                value = kwargs.pop(key)
                if value is True:
                    value = 1

                if value is False:
                    value = 0

                parameters[key] = value

        proccessed_path = path
        path_args = re_path_template.findall(path)
        for variable in path_args:
            args = list(args)
            try:
                value = args.pop(0)
            except IndexError:
                raise Exception('Not enough positional arguments expects: %s' % (path_args))

            value = str(getattr(value, 'id', value))
            proccessed_path = proccessed_path.replace(variable, value)

        resp_method = self.request
        if method in ('POST', 'PUT', 'PATCH') and content_type == 'JSON' and kwargs.get('data'):
            resp_method = self.request_json

        resp = resp_method(method, proccessed_path, params=parameters, raw_response=raw_response, **kwargs)

        if raw_response:
            return resp

        # If the status code is 204 there won't be any JSON to parse
        if getattr(resp, 'status_code', None) == 204:
            return None

        if payload_list:
            resp.data = [payload_type.from_response_data(x, api=self) for x in resp.data]
        else:
            resp.data = payload_type.from_response_data(resp.data, api=self)

        resp.meta = APIMeta.from_response_data(resp.meta, api=self)

        return resp.data, resp.meta

    return_type = ':class:`%s.%s`' % (payload_type.__module__, payload_type.__name__)
    if payload_list:
        return_type = 'list of %s' % (return_type)

    params_string = ''
    params = re_path_template.findall(path)
    params = [x.replace('{', '').replace('}', '') for x in params]
    if params:
        params_string += '\n'
        for param in params:
            params_string += ':param %s:' % (param)

    arguments = ['*args', '**kwargs']
    if params:
        arguments = params + ['%s=None' % x for x in allowed_params] + arguments

    arguments = ', '.join(arguments)
    method_sig = '%s(%s)' % (func_name, arguments)
    doc = """%s
    %s
    **API Endpoint**: `%s %s`

    **Returns**: %s
    %s
    """ % (method_sig, extra_doc, method, path, return_type, params_string)

    run.__doc__ = doc

    setattr(API, func_name, run)

# Post methods

bind_api_method('create_post', '/posts', payload_type=Post, method='POST',
                allowed_params=POST_PARAMS, require_auth=True)


bind_api_method('get_post', '/posts/{post_id}', payload_type=Post,
                allowed_params=POST_PARAMS, require_auth=False)


bind_api_method('delete_post', '/posts/{post_id}', payload_type=Post, method='DELETE',
                allowed_params=POST_PARAMS, require_auth=True)


bind_api_method('repost_post', '/posts/{post_id}/repost', payload_type=Post, method='PUT',
                allowed_params=POST_PARAMS, require_auth=True)


bind_api_method('unrepost_post', '/posts/{post_id}/repost', payload_type=Post, method='DELETE',
                allowed_params=POST_PARAMS, require_auth=True)


bind_api_method('bookmark_post', '/posts/{post_id}/bookmark', payload_type=Post, method='PUT',
                allowed_params=POST_PARAMS, require_auth=True)


bind_api_method('unbookmark_post', '/posts/{post_id}/bookmark', payload_type=Post, method='DELETE',
                allowed_params=POST_PARAMS, require_auth=True)


bind_api_method('get_posts', '/posts', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS + ['ids'], require_auth=True)


bind_api_method('users_posts', '/users/{user_id}/posts', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=True)


bind_api_method('users_bookmarked_posts', '/users/{user_id}/bookmarks', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=True)


bind_api_method('users_mentioned_posts', '/users/{user_id}/mentions', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=True)


bind_api_method('posts_with_hashtag', '/posts/tag/{hashtag}', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=False)


bind_api_method('posts_thread', '/posts/{post_id}/thread', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=True)


bind_api_method('users_post_streams_me', '/posts/streams/me', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=True)


bind_api_method('users_post_streams_unified', '/posts/streams/unified', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=True)


bind_api_method('posts_streams_global', '/posts/streams/global', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=False)

bind_api_method('post_search', '/posts/search', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS + POST_SEARCH_PARAMS, require_auth=True)


# User methods

bind_api_method('get_user', '/users/{user_id}', payload_type=User,
                allowed_params=USER_PARAMS, require_auth=False)


bind_api_method('get_users', '/users', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS + ['ids'], require_auth=False)


bind_api_method('update_user', '/users/{user_id}', payload_type=User, method='PUT',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('patch_user', '/users/{user_id}', payload_type=User, method='PATCH',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('update_avatar', '/users/me/avatar', payload_type=User, method='POST',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('update_cover', '/users/me/cover', payload_type=User, method='POST',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('follow_user', '/users/{user_id}/follow', payload_type=User, method='PUT',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('unfollow_user', '/users/{user_id}/follow', payload_type=User, method='DELETE',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('mute_user', '/users/{user_id}/mute', payload_type=User, method='PUT',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('unmute_user', '/users/{user_id}/mute', payload_type=User, method='DELETE',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('block_user', '/users/{user_id}/block', payload_type=User, method='PUT',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('unblock_user', '/users/{user_id}/block', payload_type=User, method='DELETE',
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('users_following', '/users/{user_id}/following', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS, require_auth=True)


bind_api_method('users_followers', '/users/{user_id}/followers', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS, require_auth=True)


bind_api_method('users_muted_users', '/users/{user_id}/muted', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS, require_auth=True)


bind_api_method('users_muted_users_ids', '/users/{user_id}/muted', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS, require_auth=True)


bind_api_method('users_blocked_users', '/users/{user_id}/blocked', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS, require_auth=True)


bind_api_method('user_search', '/users/search', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + USER_PARAMS + USER_SEARCH_PARAMS, require_auth=True)


bind_api_method('user_presence', '/presence', payload_type=SimpleValueModel, payload_list=True,
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('get_users_presence', '/users/{user_id}/presence', payload_type=SimpleValueModel, payload_list=False,
                allowed_params=USER_PARAMS, require_auth=True)


bind_api_method('update_users_presence', '/users/{user_id}/presence', payload_type=SimpleValueModel, payload_list=False,
                allowed_params=USER_PARAMS + ['presence'], require_auth=True, method='PUT')


# Channels
bind_api_method('subscribed_channels', '/users/me/channels/subscribed', payload_type=Channel, payload_list=True,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS, require_auth=True)

bind_api_method('existing_pm', '/users/me/channels/existing_pm', payload_type=Channel, payload_list=False,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS + ['ids'], require_auth=True)

bind_api_method('create_channel', '/channels', payload_type=Channel, method='POST',
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('get_channel', '/channels/{channel_id}', payload_type=Channel,
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('get_channels', '/channels', payload_type=Channel, payload_list=True,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS + ['ids'], require_auth=True)


bind_api_method('users_channels', '/users/me/channels', payload_type=Channel, payload_list=True,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS, require_auth=True)


bind_api_method('num_unread_pm_channels', '/users/me/channels/num_unread/pm', payload_type=SimpleValueModel,
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('update_channel', '/channels/{channel_id}', payload_type=Channel, method='PUT',
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('subscribe_channel', '/channels/{channel_id}/subscribe', payload_type=Channel, method='PUT',
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('unsubscribe_channel', '/channels/{channel_id}/subscribe', payload_type=Channel, method='DELETE',
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('subscribed_users', '/channels/{channel_id}/subscribers', payload_type=User, payload_list=True,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS, require_auth=True)


bind_api_method('mute_channel', '/channels/{channel_id}/mute', payload_type=Channel, method='PUT',
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('unmute_channel', '/channels/{channel_id}/mute', payload_type=Channel, method='DELETE',
                allowed_params=CHANNEL_PARAMS, require_auth=True)


bind_api_method('muted_channels', '/users/me/channels/muted', payload_type=Channel, payload_list=True,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS, require_auth=True)


bind_api_method('channel_search', '/channels/search', payload_type=Channel, payload_list=True,
                allowed_params=PAGINATION_PARAMS + CHANNEL_PARAMS + CHANNEL_SEARCH_PARAMS, require_auth=True)


# Messages
bind_api_method('get_channel_messages', '/channels/{channel_id}/messages', payload_type=Message, payload_list=True,
                allowed_params=PAGINATION_PARAMS + MESSAGE_PARAMS, require_auth=True)


bind_api_method('create_message', '/channels/{channel_id}/messages', payload_type=Message, method='POST',
                allowed_params=MESSAGE_PARAMS, require_auth=True)


bind_api_method('get_message', '/channels/{channel_id}/messages/{message_id}', payload_type=Message,
                allowed_params=MESSAGE_PARAMS, require_auth=True)


bind_api_method('get_messages', '/channels/messages', payload_type=Message, payload_list=True,
                allowed_params=PAGINATION_PARAMS + MESSAGE_PARAMS + ['ids'], require_auth=True)


bind_api_method('users_messages', '/users/me/messages', payload_type=Message, payload_list=True,
                allowed_params=PAGINATION_PARAMS + MESSAGE_PARAMS, require_auth=True)


bind_api_method('delete_message', '/channels/{channel_id}/messages/{message_id}', payload_type=Message, method='DELETE',
                allowed_params=PAGINATION_PARAMS + MESSAGE_PARAMS + ['ids'], require_auth=True)


bind_api_method('message_search', '/channels/messages/search', payload_type=Message, payload_list=True,
                allowed_params=PAGINATION_PARAMS + MESSAGE_PARAMS + MESSAGE_SEARCH_PARAMS, require_auth=True)


bind_api_method('sticky_messages', '/channels/{channel_id}/sticky_messages', payload_type=Message, payload_list=True,
                allowed_params=PAGINATION_PARAMS + MESSAGE_PARAMS, require_auth=True)


bind_api_method('stick_message', '/channels/{channel_id}/messages/{message_id}/sticky', payload_type=Message, method='PUT',
                allowed_params=MESSAGE_PARAMS, require_auth=True)


bind_api_method('unstick_message', '/channels/{channel_id}/messages/{message_id}/sticky', payload_type=Message, method='DELETE',
                allowed_params=MESSAGE_PARAMS, require_auth=True)


# Files

bind_api_method('create_file', '/files', payload_type=File, method='POST',
                allowed_params=FILE_PARAMS, require_auth=True, content_type='multipart/form-data',)


bind_api_method('update_file', '/files/{file_id}', payload_type=File, method='PUT',
                allowed_params=FILE_PARAMS, require_auth=True)


bind_api_method('set_file_content', '/files/{file_id}/content', payload_type=File, method='PUT',
                allowed_params=FILE_PARAMS, require_auth=True, content_type='multipart/form-data',)


bind_api_method('get_file_content', '/files/{file_id}/content', payload_type=File, method='GET',
                allowed_params=FILE_PARAMS, raw_response=True, require_auth=True)


bind_api_method('get_file', '/files/{file_id}', payload_type=File, method='GET',
                allowed_params=FILE_PARAMS, require_auth=True)


bind_api_method('get_files', '/files', payload_type=File, method='GET', payload_list=True,
                allowed_params=FILE_PARAMS + ['ids'], require_auth=True)


bind_api_method('delete_file', '/files/{file_id}', payload_type=File, method='DELETE',
                allowed_params=FILE_PARAMS, require_auth=True)


bind_api_method('get_my_files', '/users/me/files', payload_type=File, method='GET', payload_list=True,
allowed_params=FILE_PARAMS + PAGINATION_PARAMS, require_auth=True)


# Interactions
bind_api_method('interactions_with_user', '/users/me/actions', payload_type=Interaction, payload_list=True,
                allowed_params=PAGINATION_PARAMS, require_auth=True)


# Text Process
bind_api_method('text_process', '/text/process', payload_type=APIModel, method='POST', require_auth=True)


# Token
bind_api_method('get_token', '/token', payload_type=Token, require_auth=True)


# Config
bind_api_method('get_config', '/sys/config', payload_type=APIModel, require_auth=True)

# Stats
bind_api_method('get_stats', '/sys/stats', payload_type=APIModel, require_auth=True)


# Explore Streams
bind_api_method('get_explore_streams', '/posts/streams/explore', payload_type=ExploreStream, payload_list=True,
                require_auth=False)

bind_api_method('get_explore_stream', '/posts/streams/explore/{slug}', payload_type=Post, payload_list=True,
                allowed_params=PAGINATION_PARAMS + POST_PARAMS, require_auth=False)
