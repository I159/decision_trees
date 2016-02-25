"""Binary ID3 decision tree.

All the features including a target feature is binary."""

import collections
import itertools
import math


class Tree(object):
    """Decision tree controller object.

    Control nodes. Maintain learning process and making decisions process."""

    parts = collections.namedtuple('DataParts', ('left', 'right'))

    def __init__(self, learning_data, target):
        """Sort a training data relatively to a target feature.

        Sort a training data relatively to a target feature to determine
        the most bound features: the smaller entropy at the data sorted
        relative to the target feature, the more bound the feature to the
        target."""

        self.target = target
        self.keys = self.get_verified_keys(learning_data)
        self.learning_data = self.get_verified_data(learning_data)
        self.root_node = None
        self.learn()
        self.cleanup()

    def get_verified_data(self, data):
        """Check is data consistent."""
        if len(set(itertools.chain(*(i.itervalues() for i in data)))) != 2:
            raise ValueError(
                    'Inconsistent data: data is not binary.')
        return sorted(data, key=lambda x: x[self.target])

    def get_verified_keys(self, learning_data):
        """Check for data consistency and return keys."""
        keys = set(tuple(i.keys()) for i in learning_data)
        if len(keys) == 1:
            keys = list(keys.pop())
            keys.remove(self.target)
            return keys
        raise ValueError('Inconsistent data: the items have different keys.')

    def get_probability(self, key, from_=None, to=None):
        """Get probability for a different values of a key on a slice."""
        if from_ or to:
            the_slice = self.learning_data[from_:to]
        else:
            the_slice = self.learning_data
        for i in (0, 1):
            by_key = filter(lambda x: x[key] == i, the_slice)
            yield len(by_key) / float(len(the_slice))

    def count_entropy(self, key, from_, to):
        """Count entropy for a key on a slice."""
        probs = list(self.get_probability(key, from_, to))
        try:
            return sum(map(lambda p: -(p * math.log(p, 2)), probs))
        except ValueError:
            return None

    @staticmethod
    def min_entp_key(x):
        """Common filtering key."""
        return x[0]

    def average_entropy(self, key, from_, to):
        """Average entropy for on a slice for a key."""
        def count(delimeter):
            entropy = filter(None,
                    (self.count_entropy(key, from_, delimeter),
                     self.count_entropy(key, delimeter, to))
                    )
            if len(entropy) == 1:
                return entropy[0], delimeter
            elif not entropy:
                return 0, delimeter
            else:
                return sum(entropy) / 2.0, delimeter
        return count

    def min_entpy_idx(self, from_, to):
        """Count average entropy for all allowed slices.

        Returns a minimum average entropy index and a prevailing
        values of the right and left side by the target key."""

        def count(key):
            ave_entropy = map(
                    self.average_entropy(key, from_, to),
                    xrange(from_+1, to-1))
            entp_dlm = min(ave_entropy, key=self.min_entp_key)
            return entp_dlm + (key, )
        return count

    def min_key_index(self, from_, to):
        """Key with a minimal entropy for a slice."""
        keys_by_entp = map(self.min_entpy_idx(from_, to), self.keys)
        return min(keys_by_entp, key=self.min_entp_key)

    def min_entropy_leaf(self, leaf):
        """leaf node with a minimal entropy."""
        return self.min_key_index(leaf['from'], leaf['to']) + (leaf, )

    def get_feature_values(self, key, from_, to, index):
        """The most probable value for a key on a node."""
        left = collections.Counter(
                [i[key] for i in self.learning_data[from_: index]])
        right = collections.Counter(
                [i[key] for i in self.learning_data[index: to]])
        left_val = max(left, key=lambda k: left[k])
        right_val = max(right, key=lambda k: right[k])

        if left_val == right_val:
            left_prob = left[left_val] / float(left[0] + left[1])
            right_prob = right[right_val] / float(right[0] + right[1])
            if left_prob > right_prob:
                right_val = abs(right_val - 1)
            elif right_prob > left_prob:
                left_val = abs(left_val - 1)

        return left_val, right_val

    def learn(self):
        """Learn process itself."""
        self.root_node = {'from': 0, 'to': len(self.learning_data)}
        leafs = [self.root_node]

        while self.keys:
            index, key, leaf = max(
                    map(self.min_entropy_leaf, leafs),
                    key=self.min_entp_key)[1:]
            leaf['key'] = key
            leaf['left'] = {'from': leaf['from'], 'to': index}
            leaf['right'] = {'from': index, 'to': leaf['to']}
            leaf['left_val'], leaf['right_val'] = self.get_feature_values(
                key, leaf['from'], leaf['to'], index)

            for branch in ('left', 'right'):
                if leaf[branch]['to'] - leaf[branch]['from'] > 3:
                    leafs.append(leaf[branch])

            leafs.remove(leaf)
            self.keys.remove(key)
            del leaf['left']
            del leaf['right']

        for leaf in leafs:
            leaf_data = self.learning_data[leaf['from']: leaf['to']]
            target_value = collections.Counter(
                i[self.target] for i in leaf_data)
            leaf[self.target] = target_value

    def make_decision(self, unclassified, node=None):
        """Decision process itself."""
        node = node or self.root_node
        try:
            if unclassified[node['key']] == node['left']:
                return self.make_decision(unclassified, node['left_child'])
            elif unclassified[node['key']] == node['right']:
                return self.make_decision(unclassified, node['right'])
            raise ValueError('Invalid predicate value.')
        except KeyError:
            return node[self.target]

    def cleanup(self):
        """Cleanup memory."""
        delattr(self, 'keys')
        delattr(self, 'learning_data')
