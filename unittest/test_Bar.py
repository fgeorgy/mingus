import sys
sys.path += ["../"]

from mingus.containers.Bar import Bar
from mingus.containers.Note import Note
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.mt_exceptions import MeterFormatError
import unittest

class test_Bar(unittest.TestCase):
	
	def setUp(self):
		self.b = Bar('C', (4, 4))
		self.c = Bar('E', (2, 2))
		self.meterless = Bar('C', (0, 0))

	
	def test_place_notes_types(self):
		self.assertEqual(True, self.meterless + NoteContainer(["A", "C"]))
		self.assertEqual(True, self.meterless + "A")
		self.assertEqual(True, self.meterless + Note("A"))
		self.assertEqual(True, self.meterless + ["A", "B"])
		self.assertEqual(True, self.meterless + [Note("A"), Note("B")])


	def test_get_range(self):
		self.b + NoteContainer(["C", "E"])
		self.assertEqual((Note("C"), Note("E")), self.b.get_range())

	def test_set_item(self):
		b = Bar()
		b + ["A", "C", "E"]
		c = Bar()
		c + ["A", "C", "E"]

		self.assertEqual(b, c)
		c[0] = NoteContainer(["A", "C", "E"])
		self.assertEqual(b, c)
		c[0] = ["A", "C", "E"]
		self.assertEqual(b, c)
		c[0] = Note("A")
		c[0] = c[0][2] + NoteContainer(["C", "E"])
		self.assertEqual(b, c)
		c[0] = Note("A")
		c[0] = c[0][2] + "C"
		c[0] = c[0][2] + "E"
		self.assertEqual(b, c)

	def test_key(self):
		self.assertEqual(self.b.key, Note("C"))
		self.assertEqual(self.c.key, Note("E"))


	def test_transpose(self):
		b = Bar()
		c= Bar()
		b + ["C", "E", "G"]
		c + ["E", "G#", "B"]
		b + ["F", "A", "C"]
		c + ["A", "C#", "E"]
		b.transpose("3", True)
		self.assertEqual(b, c)
		b.transpose("3", False)
		b.transpose("3")
		self.assertEqual(b, c)

	def test_augment(self):
		b = Bar()
		c = Bar()
		d = Bar()
		b + "A"
		c + "A#"
		d + "A##"
		b.augment()
		self.assertEqual(b, c)
		b.augment()
		self.assertEqual(b, d)
		c.augment()
		self.assertEqual(c, d)

	def test_diminish(self):
		b = Bar()
		c = Bar()
		b + "A"
		c + "Ab"
		b.diminish()
		self.assertEqual(b, c)

	def test_to_minor(self):
		b = Bar()
		c = Bar()
		b + "C"
		c + "A"
		b.to_minor()
		self.assertEqual(b, c)

	def test_to_major(self):
		b = Bar()
		c = Bar()
		b + "C"
		c + "A"
		c.to_major()
		self.assertEqual(b, c)

	def test_get_note_names(self):
		b = Bar()
		b + "C"
		b + "A"
		self.assertEqual(["C", "A"], b.get_note_names())

	def test_determine_chords(self):
		b = Bar()
		b + ["C", "E", "G"]
		b + ["F", "A", "C"]
		self.assertEqual([[0.0, ["C major triad"]], [0.25, ["F major triad"]]], b.determine_chords())

	def test_determine_progression(self):
		b = Bar()
		b + ["C", "E", "G"]
		b + ["F", "A", "C"]
		self.assertEqual([[0.0, ["I"]], [0.25, ["IV"]]], b.determine_progression(True))

	def test_tied_notes(self):
		b1, b2 = Bar(), Bar()
		n = Note('G')
		b1.place_notes('C', 4)
		b1.place_notes('C', 4)
		b1.place_notes('C', 4)
		b1.place_notes(n, 4)
		b2.place_notes(Note('G', tie_note=n), 4)
		b2.place_notes('C', 4)
		b2.place_notes('C', 4)
		b2.place_notes('C', 4)
		last_note_b1 = b1[-1][2][0]
		first_note_b2 = b2[0][2][0]
		self.assertTrue(last_note_b1.is_tied())
		self.assertTrue(first_note_b2.tie_note != None)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test_Bar)

