"""Binary ID3 decision tree.

All the features including a target feature is binary."""

import math


class Tree(object):
    """Decision tree controller object.

    Control nodes. Maintain learning process and making decisions process."""

    def __init__(self, learning_data, target):
        """Sort a training data relatively to a target feature.

        Sort a training data relatively to a target feature to determine
        the most bound features: the smaller entropy at the data sorted
        relative to the target feature, the more bound the feature to the
        target."""

        self.learning_data = sorted(learning_data, key=lambda x: x[target])
        self.keys = self.get_keys()
        self.target = target
        self.learn()
        self.cleanup()

    def get_keys(self):
        """Check for data consistency and return keys."""
        keys = set(i.keys() for i in self.learning_data)
        if len(keys) == 1:
            return keys.pop()
        raise ValueError('Inconsistence data: the items have different keys.')

    def get_probability(self, key, from_, to):
        """Get probability for a different values of a key on a slice."""
        the_slice = self.learning_data[from_: to]
        for i in (0, 1):
            by_key = filter(lambda x: x[key] == i, the_slice)
            yield len(by_key) / float(len(the_slice))

    def count_entropy(self, key, from_, to):
        """Count entropy for a key on a slice."""
        probs = self.get_probability(key, from_, to)
        return sum(map(lambda p: -(p * math.log(p, 2)), probs))

    @staticmethod
    def min_entp_key(x):
        return x[0]

    def average_entropy(self, key, from_, to):
        def count(delimeter):
            ave_entropy = sum(
                    self.count_entropy(key, from_, delimeter),
                    self.count_entropy(key, delimeter, to)) / 2.0
            return ave_entropy, delimeter
        return count

    def min_entpy_idx(self, from_, to):
        """Conunt average entropy for all allowed slices
        Return a minimum average entropy index and a prevailing
        values of the right and left side by the target key."""

        def count(key):
            delimeters = xrange(from_ + 1, to - 1)
            get_average_entropy = self.average_entropy(key, from_, to)
            entp_dlm = min(
                    map(get_average_entropy, delimeters),
                    key=self.min_entp_key)
            return entp_dlm += key
        return count

    def get_predicate(self, from_, to):
        keys_idxs = map(self.min_entpy_idx(key, from_, to), self.keys)
        index, key = min(keys_idxs, key=self.min_entp_key)
        left = collections.Counter(
                i[key] for i in self.learning_data[from_: index])
        right = collections.Counter(
                i[key] for i in self.learning_data[index: to])
        left_val = max(left, key=lambda k: left[k])
        right_val = max(right, key=lambda k: right[k])
        # Remove the key for the keys list.
        node = {'key': key,
                'left': left_val,
                'right': right_val}
        raise NotImplementedError

    def learn(self):
        # 1* Count average entropy for each item.
        # 2* Get minimum entropy item index
        # 3* Divide a dataset with the obtained element.
        # 4* Set an initial node with the minimum entropy element as predicate.
        # node = {feature_name: name, 'left': l_next_node, 'right': r_next_node}
        # leaf_node = the same but with predicted feature value

        # Keep slices for every node during a loop. Store in a node if it is
        # needed.
        # 5->1->2* For both parts.
        # 6->3* For both parts.
        # 7* Set leafs for a parent node (Parallel computation).
        # 8* Cleanup: remove a learning data and a slices.
        raise NotImplementedError

    def make_decision(self, unclassified):
        # * Iteratively compare all the features of an unclassified item with
        # a nodes. Use single rule: 1 - left, 0 - right.
        # * Return predicted value for an unknown feature.
        raise NotImplementedError

    def cleanup(self):
        # 8* Cleanup: remove a learning data and a slices.
        raise NotImplementedError
