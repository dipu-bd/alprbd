"""
A generic module to read data.
"""
import numpy as np

class Dataset(object):
    """Dataset class object."""

    def __init__(self, images, labels):
        """Initialize the class."""
        self._images = images
        self._num_examples = images.shape[0]
        self._labels = labels
        self._epochs_completed = 0
        self._index_in_epoch = 0
    # end __init__

    @property
    def images(self):
        return self._images
    # end property

    @property
    def labels(self):
        return self._labels
    # end property

    @property
    def num_examples(self):
        return self._num_examples
    # end property

    @property
    def epochs_completed(self):
        return self._epochs_completed
    # end property

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = np.arange(self._num_examples)
            np.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch

        return self._images[start:end], self._labels[start:end]
    # end function
# end class
