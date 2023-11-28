import unittest

from arcimoto.note import Note

from arcimoto.tests import test_vin_get


class TestPostNote(unittest.TestCase):

    message = f'{__name__}_unit_test created'

    # test successes
    def test_post_note_success_input_minimum(self):
        try:
            Note(
                'Vehicle',
                test_vin_get(),
                self.message
            )
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
