import mock
import random
import string
import unittest

import tree


class TestBuildTree(unittest.TestCase):
    def setUp(self):
        self.keys = [string.ascii_lowercase[i] for i in xrange(2**4)]
        learning_data = list(self.gen_data(1000))
        self.tree = tree.Tree(learning_data, 'result')

    def gen_data(self, num_items, incons=False):
        while num_items:
            item = {k: random.randint(0, 1) for k in self.keys}
            item['result'] = sum(item.values()) % 2
            if incons:
                del item['b']
                incons = False
            num_items -= 1
            yield item

    def gen_inconsistence_data(self, num_items):
        return list(self.gen_data(num_items))[0].pop('a')

    def test_init_tree(self):
        self.assertIsNotNone(self.tree.root_node['left'])
        self.assertIsNotNone(self.tree.root_node['right'])

    def test_inconsistence_data_init(self):
        learning_data = self.gen_data(1000, incons=True)
        self.assertRaises(ValueError, tree.Tree, learning_data, 'p')

    def test_minimum_enthropy(self):
        unittest.skip("Not implemented.")

    def test_all_predicates_used(self):
        keys = []
        leafs = []
        leafs.append(self.tree.root_node)
        while leafs:
            for i in leafs:
                if 'key' in i:
                    keys.append(i['key'])
                for j in ('left', 'right'):
                    if j in i:
                        leafs.append(i[j])
                leafs.remove(i)
        print keys, self.keys
        self.assertEqual(sorted(keys), sorted(self.keys))


class TestDecide(unittest.TestCase):
    def test_is_correct_desision(self):
        unittest.skip("Not implemented.")
