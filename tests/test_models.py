import time
import unittest

from tests.config import PnutpyTestCase

test_post_id = 1


class PnutpyModelTests(PnutpyTestCase):
    """Unit tests"""

    def test_post(self):
        text = u'Testing posts indvidually'
        post, meta = self.api.create_post(data={'text': text})
        post.bookmark()
        post.unbookmark()
        post.delete()
        post, meta = self.api.get_post(257434)
        post.repost()
        post.unrepost()

    def test_user(self):
        new_display_name = u'tester %s' % (time.time())
        user, meta = self.api.get_user('me')

        user.name = new_display_name
        user.update_user()
        self.assertEquals(user.name, new_display_name)

        user, meta = self.api.get_user(9)
        user.follow_user()
        user.unfollow_user()

        user.mute_user()
        user.unmute_user()

        user.block_user()
        user.unblock_user()


if __name__ == '__main__':
    unittest.main()
