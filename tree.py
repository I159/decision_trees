"""Binary ID3 decision tree.

All the features including a target feature is binary."""


class Tree(object):
    """Decision tree controller object.

    Control nodes. Maintain learning process and making decisions process."""

    def __init__(self, learning_data, target):
        # * Sort a training data relatively to a target feature to determine
        # * the most bound features: the smaller entropy at the data sorted
        # relative to the target feature, the more bound the feature to the
        # target.
        self.learning_data = sorted(learning_data, key=target)
        self.target = target
        self.learn()
        self.cleanup()

    def count_entropy(self, from_, to):
        # * Count entropy of a left part relatively to a target key
        # * Count entropy of a right part relatively to a target key
        # * Count entropy of a left part relatively to an unknown key
        # * Count entropy of a right part relatively to an unknown key
        # * Count average entropy.
        # * return slice and entropy
        raise NotImplementedError

    def get_predicate(self, from_, to):
        # 1* Iterate through a keys:
        #     2* Iterate through a sequence to get minimum entropy item.
        # 3* Return minimum entropy key and item index
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
