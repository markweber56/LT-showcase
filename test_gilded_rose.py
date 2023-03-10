# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        print("test foo")
        items = [Item("foo", 0, 0)]
        GildedRose(items).update_quality()
        self.assertEqual("foo", items[0].name)

    def test_update_generic_item(self):
        print("test update generic item")
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(19, items[0].quality)

    def test_update_item_quality_must_be_positive(self):
        print("test update item quantity cannot become negative")
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=0)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_update_generic_after_sellby(self):
        print("test item quality decreases twice as fast after sell by day")
        items = [
            Item(name="+5 Dexterity Vest", sell_in=-1, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(-2, items[0].sell_in)
        self.assertEqual(8, items[0].quality)

    def test_aged_brie_appreciates(self):
        print("test aged brie quality increases")
        items = [
            Item(name="Aged Brie", sell_in=2, quality=0)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(1, items[0].quality)

    def test_quality_does_not_exceed_max(self):
        print("test quality for appreciating item does not exceed 50")
        items = [
            Item(name="Aged Brie", sell_in=5, quality=50)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(50, items[0].quality)

    def test_quality_goes_to_zero_after_sellby(self):
        print("test quality still decreases if above zero after sell by")
        items = [
            Item(name="+5 Dexterity Vest", sell_in=-2, quality=3)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(-3, items[0].sell_in)
        self.assertEqual(1, items[0].quality)

        GildedRose(items).update_quality()
        self.assertEqual(-4, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_update_backstage_pass_15_days(self):
        print("quality of concert 15 days away should increase by 1")
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=16, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(15, items[0].sell_in)
        self.assertEqual(11, items[0].quality)

    def test_update_backstage_pass_10_days(self):
        '''
        NOTE: the old logic is bad for this. "Backstage pass" quality is updated
        based on previous sell_in value rather than updated one
        '''
        print("quality of concert 10 days away should increase by 2")
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(12, items[0].quality)

    def test_update_backstage_pass_5_days(self):
        print("quality of concert 10 days away should increase by 2")
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(13, items[0].quality)

    def test_backstage_pass_quality_is_zero_after_concert(self):
        print("quality of concert should go to zero when sell by less than 0")
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_backstage_pass_quality_cannot_exceed_max(self):
        print("quality of concert passes should not exceed 50")
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=3, quality=48)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(50, items[0].quality)

    def test_conjured_quality_decreases_by_two(self):
        print("quality of conjured item should decrease by 2 if not expired")
        items = [
            Item(name="Conjured Mana Cake", sell_in=5, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(8, items[0].quality)

    def test_conjured_quality_decreases_by_four_once_expired(self):
        print("quality of conjured item should decrease by 4 once expired")
        items = [
            Item(name="Conjured Mana Cake", sell_in=-3, quality=10)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(-4, items[0].sell_in)
        self.assertEqual(6, items[0].quality)

    def test_conjured_item_quality_does_not_become_negative(self):
        print("quality of conjured item should not become negative")
        items = [
            Item(name="Conjured Mana Cake", sell_in=-3, quality=2)
        ]
        GildedRose(items).update_quality()
        self.assertEqual(-4, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

if __name__ == '__main__':
    unittest.main()
