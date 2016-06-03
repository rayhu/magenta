"""Tests to ensure correct reading and writing of NoteSequence record files."""

import tempfile

import tensorflow as tf

from magenta.lib import note_sequence_io
from magenta.protobuf import music_pb2


class NoteSequenceIoTest(tf.test.TestCase):

  def testGenerateId(self):
    sequence_id_1 = note_sequence_io.generate_id(
        '/my/file/name', 'my_collection', 'midi')
    self.assertEquals('/id/midi/my_collection/', sequence_id_1[0:23])
    sequence_id_2 = note_sequence_io.generate_id(
        '/my/file/name', 'your_collection', 'abc')
    self.assertEquals('/id/abc/your_collection/', sequence_id_2[0:24])
    self.assertEquals(sequence_id_1[23:], sequence_id_2[24:])

    sequence_id_3 = note_sequence_io.generate_id(
        '/your/file/name', 'my_collection', 'abc')
    self.assertNotEquals(sequence_id_3[22:], sequence_id_1[23:])
    self.assertNotEquals(sequence_id_3[22:], sequence_id_2[24:])

  def testNoteSequenceRecordWriterAndIterator(self):
    sequences = []
    for i in xrange(4):
      sequence = music_pb2.NoteSequence()
      sequence.id = str(i)
      sequence.notes.add().pitch = i
      sequences.append(sequence)

    temp_file = tempfile.NamedTemporaryFile(prefix='NoteSequenceIoTest')
    with tempfile.NamedTemporaryFile(prefix='NoteSequenceIoTest') as temp_file:
      with note_sequence_io.NoteSequenceRecordWriter(temp_file.name) as writer:
        for sequence in sequences:
          writer.write(sequence)

      for i, sequence in enumerate(
          note_sequence_io.note_sequence_record_iterator(temp_file.name)):
        self.assertEquals(sequence, sequences[i])

if __name__ == '__main__':
  tf.test.main()
