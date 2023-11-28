import unittest

from arcimoto.user import User


class TestReset(unittest.TestCase):

    user_object_properties = [
        'username',
        'has_profile',
        'groups',
        'roles',
        'preferences',
        'abilities'
    ]
    user_profile_items = [
        'email',
        'phone',
        'display_name',
        'avatar',
        'avatar_file_type'
    ]

    # test successes
    def test_reset_success(self):
        UserObject = User(mock=True)
        try:
            UserObject.reset()
        except Exception as e:
            self.fail(f'test failed {e}')

        for user_object_property in self.user_object_properties:
            self.assertFalse(getattr(UserObject, user_object_property))

        for user_profile_item in self.user_profile_items:
            self.assertFalse(UserObject.profile.get(user_profile_item, 'no value found'))

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
