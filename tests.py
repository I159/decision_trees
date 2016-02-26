import mock
import random
import string
import unittest

import tree


class BaseTestCase(unittest.TestCase):
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


class TestBuildTree(BaseTestCase):
    def gen_inconsistence_data(self, num_items):
        return list(self.gen_data(num_items))[0].pop('a')

    def test_tree_health(self):
        self.assertIsNotNone(self.tree.root_node['left'])
        self.assertIsNotNone(self.tree.root_node['right'])

    def test_inconsistence_data_init(self):
        learning_data = self.gen_data(1000, incons=True)
        self.assertRaises(ValueError, tree.Tree, learning_data, 'p')

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
        self.assertEqual(sorted(keys), sorted(self.keys))


class TestDecide(BaseTestCase):
    def setUp(self):
        super(TestDecide, self).setUp()
        self.test_data = list(self.gen_data(100))

    def test_correct_desision(self):
        predictions = map(self.tree.make_decision, self.test_data)
        results = [i['result'] for i in self.test_data]
        # Random generated data doesn't guarantee a good prediction. Use assert
        # for a real data.
        print len([i for i in zip(predictions, results) if i[0] == i[1]])


class TestMethods(unittest.TestCase):
    # TODO: test all the methods for correctness.
    pass
