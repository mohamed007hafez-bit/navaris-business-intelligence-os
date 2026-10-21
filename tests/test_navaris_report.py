import tempfile, unittest
from pathlib import Path
from navaris_report import LinkParser, build_report, contains_keyword, load_seen, save_seen, stable_id
class Tests(unittest.TestCase):
 def test_keywords(self):
  self.assertTrue(contains_keyword('Tender Notice')); self.assertTrue(contains_keyword('مناقصة جديدة')); self.assertFalse(contains_keyword('About company'))
 def test_parser(self):
  p=LinkParser(); p.feed('<a href="/tenders/1">Tender Notice</a><a href="/about">About</a>'); self.assertEqual(p.links[0],('/tenders/1','Tender Notice')); self.assertEqual(len(p.links),2)
 def test_stable_id(self): self.assertEqual(stable_id('GASCO','https://e.com/t#x','Tender'),stable_id('GASCO','https://e.com/t','Tender'))
 def test_state(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'state.json'; save_seen(p,{'a','b'}); self.assertEqual(load_seen(p),{'a','b'})
 def test_report(self):
  r=build_report([{'company':'GASCO','source':'https://example.com','status':'ok','items':[]}],[],'2026-10-21T00:00:00+00:00'); self.assertIn('غير متاح',r); self.assertIn('لا تُحسب درجة رقمية',r)
if __name__=='__main__': unittest.main()
