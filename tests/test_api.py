import os
import time
import unittest

from pnutpy.cursor import cursor
from pnutpy.utils import get_app_access_token

from tests.config import PnutpyTestCase

test_post_id = 1


class PnutpyAPITests(PnutpyTestCase):
    """Unit tests"""

    def test_posts_stream_global(self):
        self.api.posts_streams_global()

    def test_post(self):
        text = u'awesome'
        post, meta = self.api.create_post(data={'text': text})
        self.assertEquals(post.content.text, text)

        post, meta = self.api.get_post(post)

        post, meta = self.api.delete_post(post)
        post, meta = self.api.create_post(data={'text': text})
        post, meta = post.delete()

        post, meta = self.api.repost_post(257434)
        post, meta = self.api.unrepost_post(257434)

        post, meta = self.api.bookmark_post(257434)
        post, meta = self.api.unbookmark_post(257434)

        posts, meta = self.api.get_posts(ids='1,2,3')
        self.assertEquals(len(posts), 3)

        posts, meta = self.api.users_posts(9)
        posts, meta = self.api.users_bookmarked_posts(9)
        posts, meta = self.api.users_mentioned_posts(9)

        posts, meta = self.api.posts_with_hashtag('awesome')
        posts, meta = self.api.posts_with_hashtag(1)

        posts, meta = self.api.users_post_streams_me()
        posts, meta = self.api.users_post_streams_unified()
        posts, meta = self.api.posts_streams_global()

        posts, meta = self.api.post_search(tags='MondayNightDanceParty')

    def test_user(self):
        display_name = u'tester %s' % (time.time())
        user, meta = self.api.get_user('me')
        self.assertEquals(self.username, user.username)
        old_name = user.name
        user.name = display_name
        cwd = os.path.dirname(__file__)
        del user.content['entities']
        user, meta = self.api.update_user('me', data=user)
        self.assertEquals(display_name, user.name)

        user, meta = self.api.patch_user('me', data={'name': old_name})
        self.assertEquals(old_name, user.name)

        users, meta = self.api.get_users(ids='1,2,3')
        self.assertEquals(len(users), 3)

        with open(cwd + '/data/avatar.png', 'rb') as avatar:
            user, meta = self.api.update_avatar('me', files={'avatar': ('avatar.png', avatar, 'image/png')})

        with open(cwd + '/data/cover.png', 'rb') as cover:
            user, meta = self.api.update_cover('me', files={'cover': ('cover.png', cover, 'image/png')})

        user, meta = self.api.follow_user(9)
        user, meta = self.api.unfollow_user(9)

        user, meta = self.api.mute_user(9)
        user, meta = self.api.unmute_user(9)

        user, meta = self.api.block_user(9)
        user, meta = self.api.unblock_user(9)

        users, meta = self.api.users_following(9)
        users, meta = self.api.users_followers(9)

        users, meta = self.api.users_muted_users('me')
        users, meta = self.api.users_muted_users_ids('me')

        users, meta = self.api.users_blocked_users('me')

        users, meta = self.api.user_search(q='news',types='feed')

    def test_channel(self):

        channels, meta = self.api.subscribed_channels()

        channel, meta = self.api.create_channel(data={
            'type': 'com.example.channel',
            'acl': {
                'full': {
                    'immutable': False,
                    'you': True,
                    'user_ids': []
                },
                'write': {
                    'any_user': True,
                    'immutable': False,
                    'you': True,
                    'user_ids': []
                },
                'read': {
                    'any_user': True,
                    'immutable': False,
                    'you': True,
                    'user_ids': []
                }
            }
        })

        channel_fetched, meta = self.api.get_channel(channel)
        self.assertEquals(channel.id, channel_fetched.id)

        channels, meta = self.api.get_channels(ids=channel_fetched.id)

        channels, meta = self.api.users_channels()

        num_unread, meta = self.api.num_unread_pm_channels()

        channel_update = {
            'id': channel.id,
            'acl': {
                'full': {
                    'immutable': False,
                    'you': True,
                    'user_ids': []
                },
                'write': {
                    'any_user': False,
                    'immutable': False,
                    'you': True,
                    'user_ids': ['9']
                },
                'read': {
                    'any_user': True,
                    'immutable': False,
                    'you': True,
                    'user_ids': []
                }
            }
        }

        channel, meta = self.api.update_channel(channel, data=channel_update)
        self.assertEquals(channel_update['acl']['write']['user_ids'], channel.acl.write.user_ids)

        channel, meta = self.api.subscribe_channel(951)
        channel, meta = self.api.unsubscribe_channel(951)
        users, meta = self.api.subscribed_users(951)

        channel, meta = self.api.mute_channel(951)
        channels, meta = self.api.muted_channels()
        channel, meta = self.api.unmute_channel(951)

        channels, meta = self.api.channel_search(is_public=1,channel_types='io.pnut.core.chat',categories='tech')

    def test_message(self):

        message1, meta = self.api.create_message(178, data={'text': "awesome 1"})
        message2, meta = self.api.create_message(178, data={'text': "awesome 2"})
        message3, meta = self.api.create_message(1001, data={'text': "awesome sticky test"})
        message, meta = self.api.get_message(178, message1)
        messages, meta = self.api.get_messages(ids='%s, %s' % (message1.id, message2.id))
        messages, meta = self.api.users_messages()
        messages, meta = self.api.get_channel_messages(178)

        message, meta = self.api.delete_message(178, message1)
        message, meta = self.api.delete_message(178, message2)

        messages, meta = self.api.message_search(channel_ids='600,18')

        messages, meta = self.api.sticky_messages(1001)
        message, meta = self.api.stick_message(1001, message3)
        message, meta = self.api.unstick_message(1001, message3)
        message, meta = self.api.delete_message(1001, message3)

    # TODO: sort out this test case and account permissions needed
    # def test_file(self):
    #     cwd = os.path.dirname(__file__)
    #     ids = []
    #     with open(cwd + '/data/avatar.png') as avatar:
    #         file_, meta = self.api.create_file(files={'content': avatar}, data={'type': 'com.adnpy.testing'})

    #     ids += [file_.id]
    #     file_, meta = self.api.get_file(file_.id)

    #     # Partial file
    #     partial_file, meta = self.api.create_file(data={'type': 'com.adnpy.testing'})
    #     ids += [file_.id]
    #     self.api.update_file(file_.id, data={
    #         'annotations': [{
    #             'type': 'net.adnpy.testing',
    #             'value': {
    #                 'test': 'test'
    #             }
    #         }]
    #     })

    #     self.api.create_custom_derived_file(partial_file.id, 'custom', data={'type': 'com.adnpy.testing'})

    #     with open(cwd + '/data/cover.png') as cover:
    #         self.api.set_custom_derived_file_content(partial_file.id, 'custom', data=cover, headers={'Content-Type': 'image/png'})

    #     with open(cwd + '/data/avatar.png') as avatar:
    #         self.api.set_file_content(partial_file.id, data=avatar, headers={'Content-Type': 'image/png'})

    #     file_, meta = self.api.get_file(partial_file.id)

    #     files, meta = self.api.get_files(ids=','.join(ids))

    #     self.assertEquals(len(files), 2)
    #     files, meta = self.api.get_my_files()
    #     self.assertGreaterEqual(len(files), 2)

    #     self.api.get_file_content(partial_file.id)
    #     self.api.get_custom_derived_file_content(partial_file.id, 'custom')

    def test_interactions(self):
        interactions, meta = self.api.interactions_with_user()

    def test_text_process(self):
        text, meta = self.api.text_process(data={'text': "#awesome @thrrgilag"})

    def test_token(self):
        token, meta = self.api.get_token()
        self.assertIsNotNone(token.get('user'))

    def test_config(self):
        config, meta = self.api.get_config()

    def test_explore_stream(self):
        explore_streams, meta = self.api.get_explore_streams()
        posts, meta = self.api.get_explore_stream(explore_streams[0])

    # TODO: implement app streams
    # def test_app_stream(self):
    #     app_access_token, token = get_app_access_token(self.client_id, self.client_secret)
    #     self.api.add_authorization_token(app_access_token)
    #     # Reset
    #     self.api.delete_all_streams()

    #     stream_def = {
    #         "object_types": [
    #             "post"
    #         ],
    #         "type": "long_poll",
    #         "key": "rollout_stream"
    #     }

    #     app_stream, meta = self.api.create_stream(data=stream_def)
    #     app_stream, meta = self.api.get_stream(app_stream)

    #     stream_def['object_types'] += ["star"]

    #     app_stream, meta = self.api.update_stream(app_stream, data=stream_def)
    #     self.assertEquals(len(app_stream.object_types), 2)
    #     app_stream, meta = self.api.delete_stream(app_stream)
    #     app_stream, meta = self.api.create_stream(data=stream_def)
    #     stream_def['key'] = "rollout_stream_2"
    #     app_stream, meta = self.api.create_stream(data=stream_def)
    #     app_streams, meta = self.api.get_streams()
    #     self.assertEquals(len(app_streams), 2)
    #     app_streams, meta = self.api.delete_all_streams()
    #     app_streams, meta = self.api.get_streams()
    #     self.assertEquals(len(app_streams), 0)

    def test_cursor(self):
        iterator = cursor(self.api.posts_streams_global, count=1)
        post1 = next(iterator)
        post2 = next(iterator)
        self.assertNotEquals(post1.id, post2.id)


if __name__ == '__main__':
    unittest.main()
