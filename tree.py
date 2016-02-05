"""Binary ID3 decision tree.

All the features including a target feature is binary."""

import math


class Tree(object):
    """Decision tree controller object.

    Control nodes. Maintain learning process and making decisions process."""

    def __init__(self, learning_data, target):
        # * Sort a training data relatively to a target feature to determine
        # the most bound features: the smaller entropy at the data sorted
        # relative to the target feature, the more bound the feature to the
        # target.
        self.learning_data = sorted(learning_data, key=lambda x: x[target])
        self.target = target
        self.learn()
        self.cleanup()

    def get_probs(self, key, from_, to):
        """Get probability for a different values of a key on a slice."""
        the_slice = self.learning_data[from_: to]
        # This example is binary. With non binary data it
        # could be much more complex.
        for i in (0, 1):
            by_key = filter(lambda x: x[key] == i, the_slice)
            yield len(by_key) / float(len(the_slice))

    def cnt_entp(self, key, from_, to):
        """Count entropy for a key on a slice."""
        probs = self.get_probability(key, from_, to)
        return sum(map(lambda p: -(p * math.log(p, 2)), probs))

    def min_ave_entropy_idx(self, key, from_, to):
        # * Conunt average entropy for all allowed slices
        # * Return a minimum average entropy index and a prevailing
        # values of the right and left side by the target key.
        delimeters = xrange(from_ + 1, to - 1)
        ave_entp = lambda i: (self.cnt_entp(key, from_, i), self.cnt_entp(key, i, to))
        map(ave_entp, delimeters)
        raise NotImplementedError

    def get_predicate(self, from_, to):
        # 1* Iterate through a keys:
        #     2* Iterate through a sequence to get minimum entropy item.
        # 3* Git minimum entropy key and item index
        # 4* Determine 1 0 direction and set an appropriate predicate function.
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
