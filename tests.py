import mock
import random
import string
import unittest

import tree


class TestBuildTree(unittest.TestCase):
    def gen_data(self, num_items):
        keys = (string.ascii_lowercase[i] for i in xrange(2**4))
        while num_items:
            item = {k: random.randrange(i) for i, k in enumerate(keys)}
            item['result'] = sum(item.values()) % 2
            yield item

    def gen_inconsistence_data(self, num_items):
        return list(self.gen_data(num_items))[0].pop('a')

    @mock.patch.object(tree, 'Tree', autospec=True)
    def test_init_tree(self, Tree):
        learning_data = self.gen_data(1000)
        tree_ = Tree(learning_data)

    def test_inconsistence_data_init(self):
        self.assertRaises(ValueError, self.gen_inconsistence_data, 1000)

    def test_ninimum_enthropy(self):
        unittest.skip("Not implemented.")

    def test_all_predicates_used(self):
        unittest.skip("Not implemented.")


class TestDecide(unittest.TestCase):
    def test_is_correct_desision(self):
        unittest.skip("Not implemented.")
