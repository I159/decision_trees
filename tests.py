import mock
import random
import string
import unittest

import tree


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.keys = [string.ascii_lowercase[i] for i in xrange(2**4)]
        self.target = 'result'
        self.learning_data = list(self.gen_data(1000))
        self.inconsistance_data = list(self.gen_data(1000, True))
        self.tree = tree.create_tree(self.learning_data, self.target)

    def gen_data(self, num_items, incons=False):
        while num_items:
            item = {k: random.randint(0, 1) for k in self.keys}
            item[self.target] = sum(item.values()) % 2
            if incons:
                del item['b']
                incons = False
            num_items -= 1
            yield item


class TestBuildTree(BaseTestCase):
    def test_tree_health(self):
        self.assertIsNotNone(self.tree.root_node['left'])
        self.assertIsNotNone(self.tree.root_node['right'])

    def test_inconsistence_data_init(self):
        self.assertRaises(ValueError,
                tree.create_tree, inconsistence_data, self.target)


class TestDecide(BaseTestCase):
    def setUp(self):
        super(TestDecide, self).setUp()
        self.test_data = list(self.gen_data(100))

    def test_correct_desision(self):
        predictions = map(self.tree.make_decision, self.test_data)
        results = [i[self.target] for i in self.test_data]
        # Random generated data doesn't guarantee a good prediction. Use assert
        # for a real data.
        print len([i for i in zip(predictions, results) if i[0] == i[1]])

    def test_inconsistence_data_prediction(self):
        # TODO: determine an error case.
        inconst_test = self.gen_data(100, True)
        predictions = map(self.tree.make_decision, inconst_test)
        results = [i[self.target] for i in self.test_data]


class TestCreationMethods(BaseTestCase):
    def setUp(self):
        super(TestCreationMethods, self).setUp()
        self.ct = tree.create_tree.__decorated__(
                self.learning_data, self.target)
        self.not_binary_data = self.learning_data[:]
        self.not_binary_data[1]['a'] = 3

    def test_verify_data(self):
        vd = self.ct._get_verified_data(self.learning_data)
        self.assertEqual(
                vd, sorted(self.learning_data, key=lambda x: x[self.target]))

    def test_fail_data_verification(self):
        import pdb; pdb.set_trace()
        self.assertRaises(
                ValueError,
                self.ct._get_verified_data,
                self.not_binary_data)

    def test_verify_keys(self):
        unittest.skip("Not implemented")

    def test_probability(self):
        unittest.skip("Not implemented")

    def test_entropy(self):
        unittest.skip("Not implemented")

    def test_average_entropy(self):
        unittest.skip("Not implemented")

    def test_index(self):
        unittest.skip("Not implemented")

    def test_key(self):
        unittest.skip("Not implemented")

    def test_leaf(self):
        unittest.skip("Not implemented")

    def test_feature(self):
        unittest.skip("Not implemented")

    def test_learn(self):
        unittest.skip("Not implemented")


class TestDecisionMethod(BaseTestCase):
    def test_make_decision(self):
        unittest.skip("Not implemented error.")
