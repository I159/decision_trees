import mock
import random
import string
import unittest

import tree


class TestBuildTree(unittest.TestCase):
    def gen_data(self, num_items, incons=False):
        keys = [string.ascii_lowercase[i] for i in xrange(2**4)]
        while num_items:
            item = {k: random.randint(0, 1) for k in keys}
            item['result'] = sum(item.values()) % 2
            if incons:
                del item['b']
                incons = False
            num_items -= 1
            yield item

    def gen_inconsistence_data(self, num_items):
        return list(self.gen_data(num_items))[0].pop('a')

    def test_init_tree(self):
        learning_data = list(self.gen_data(1000))
        tree_ = tree.Tree(learning_data, 'p')
        import pdb; pdb.set_trace()

    def test_inconsistence_data_init(self):
        learning_data = self.gen_data(1000, incons=True)
        self.assertRaises(ValueError, tree.Tree, learning_data, 'p')

    def test_ninimum_enthropy(self):
        unittest.skip("Not implemented.")

    def test_all_predicates_used(self):
        unittest.skip("Not implemented.")


class TestDecide(unittest.TestCase):
    def test_is_correct_desision(self):
        unittest.skip("Not implemented.")
