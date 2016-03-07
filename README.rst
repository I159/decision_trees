Important ins which are not in a common articles.
=================================================

1. You can sort a learning data set as you wish. So what? Hm... For different
   orders you will get different entropy at each key on the set. Those
   prediction realized by a tree could be very different depending on the order
   of elements in the training data set. So what the order to choose? It is
   simple. We have at least one attribute on the learning data which is absent
   on a predicting data set. We need to sort a learning data by a target
   feature values. Those we will have respectful to a predicting feature
   entropy by each key in the learning set. It has sense. The more existing
   feature dependent to the predicting feature the lesser entropy it produces
   because for the predicting feature we have an index with guaranteed 0
   entropy.

2. Tree degeneration with recursion. The problem is that we have limited
   number of feature-keys and in common case we have much more
   (possibly unlimited) number of items in the learning data set. If an
   algorithm recursively started a branch building it will recursively build
   single branch at each node. The keys be used before all the data will be
   analysed. In this way the tree is becoming a linked list.
   Same thing occurs with multi-threading (with Python). To solve the issue
   it is possible to store a leafs during all the learning process.

