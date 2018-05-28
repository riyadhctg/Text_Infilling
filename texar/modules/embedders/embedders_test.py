#
"""
Unit tests for embedders.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# pylint: disable=no-member

import tensorflow as tf

from texar.modules.embedders.embedders import WordEmbedder
from texar.modules.embedders.position_embedders import PositionEmbedder
from texar.context import global_mode

class EmbedderTest(tf.test.TestCase):
    """Tests parameterized embedder.
    """

    def _test_word_embedder(self, hparams):
        """Tests :class:`texar.modules.WordEmbedder`.
        """
        embedder = WordEmbedder(
            vocab_size=100, hparams=hparams)
        inputs = tf.ones([64, 16], dtype=tf.int32)
        outputs = embedder(inputs)

        emb_dim = embedder.dim
        if not isinstance(emb_dim, (list, tuple)):
            emb_dim = [emb_dim]

        hparams_dim = hparams["dim"]
        if not isinstance(hparams["dim"], (list, tuple)):
            hparams_dim = [hparams["dim"]]

        self.assertEqual(outputs.shape, [64, 16] + emb_dim)
        self.assertEqual(emb_dim, hparams_dim)
        self.assertEqual(embedder.vocab_size, 100)
        self.assertEqual(len(embedder.trainable_variables), 1)

        with self.test_session() as sess:
            sess.run(tf.global_variables_initializer())
            outputs_ = sess.run(
                outputs,
                feed_dict={global_mode(): tf.estimator.ModeKeys.TRAIN})
            self.assertEqual(outputs_.shape, (64, 16) + tuple(emb_dim))

    def _test_position_embedder(self, hparams):
        """Tests :class:`texar.modules.PositionEmbedder`.
        """
        pos_size = 100
        embedder = PositionEmbedder(
            position_size=pos_size, hparams=hparams)
        inputs = tf.ones([64, 16], dtype=tf.int32)
        outputs = embedder(inputs)

        emb_dim = embedder.dim
        if not isinstance(emb_dim, (list, tuple)):
            emb_dim = [emb_dim]

        hparams_dim = hparams["dim"]
        if not isinstance(hparams["dim"], (list, tuple)):
            hparams_dim = [hparams["dim"]]

        self.assertEqual(outputs.shape, [64, 16] + emb_dim)
        self.assertEqual(emb_dim, hparams_dim)
        self.assertEqual(embedder.position_size, 100)
        self.assertEqual(len(embedder.trainable_variables), 1)

        seq_length = tf.random_uniform([64], maxval=pos_size, dtype=tf.int32)
        outputs = embedder(sequence_length=seq_length)
        with self.test_session() as sess:
            sess.run(tf.global_variables_initializer())
            outputs_, max_seq_length = sess.run(
                [outputs, tf.reduce_max(seq_length)],
                feed_dict={global_mode(): tf.estimator.ModeKeys.TRAIN})
            self.assertEqual(outputs_.shape,
                             (64, max_seq_length) + tuple(emb_dim))


    def test_embedder(self):
        """Tests various embedders.
        """
        # no dropout
        hparams = {"dim": 1024, "dropout_rate": 0}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024], "dropout_rate": 0}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024, 10], "dropout_rate": 0}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        # dropout with default strategy
        hparams = {"dim": 1024, "dropout_rate": 0.3}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024], "dropout_rate": 0.3}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024, 10], "dropout_rate": 0.3}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        # dropout with different strategies
        hparams = {"dim": 1024, "dropout_rate": 0.3,
                   "dropout_strategy": "item"}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024], "dropout_rate": 0.3,
                   "dropout_strategy": "item"}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024, 10], "dropout_rate": 0.3,
                   "dropout_strategy": "item"}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": 1024, "dropout_rate": 0.3,
                   "dropout_strategy": "item_type"}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024], "dropout_rate": 0.3,
                   "dropout_strategy": "item_type"}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

        hparams = {"dim": [1024, 10], "dropout_rate": 0.3,
                   "dropout_strategy": "item_type"}
        self._test_word_embedder(hparams)
        self._test_position_embedder(hparams)

if __name__ == "__main__":
    tf.test.main()
