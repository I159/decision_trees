class Tree(object):
    """Decision tree controller object.

    Control nodes. Maintain learning process and making decisions process."""

    def __init__(self, learning_data):
        self.learn(learning_data)

    def learn(self, learning_data):
        if learning_data.count(learning_data[0]) == len(learning_data):
            keys = learning_data[0].keys()
        else:
            raise ValueError("Inconsistence learning data.")

        # TODO: check entropy for a target feature and for unknown feature
        # to determine a real (or at least closer to reality) entropy value.
