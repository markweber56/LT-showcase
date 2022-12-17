# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if self.is_ordinary_item(item):
                reduce_by = 2 if item.sell_in - 1 < 0 else 1
                item.quality = self.validate_new_quality(item.quality - reduce_by)
            elif self.is_legendary(item):
                # quality and sell_in do not change for legendary items
                continue
            elif self.is_conjured(item):
                reduce_by = 4 if item.sell_in - 1 < 0 else 2
                item.quality = self.validate_new_quality(item.quality - reduce_by)
            elif self.is_backstage_pass(item):
                self.update_backstage_pass(item)
            elif self.is_aged_brie(item):
                increase_by = 2 if item.sell_in - 1 < 0 else 1
                item.quality = self.validate_new_quality(item.quality + increase_by)

            item.sell_in = item.sell_in - 1

    def update_backstage_pass(self, item):
        if item.sell_in - 1 < 0:
            # quality is 0 after concert
            item.quality = 0
            return
        if item.sell_in > 10:
            item.quality = self.validate_new_quality(item.quality + 1)
            return
        if item.sell_in > 5:
            item.quality = self.validate_new_quality(item.quality + 2)
            return
        # quality < 5
        item.quality = self.validate_new_quality(item.quality + 3)

    def is_conjured(self, item):
        return "conjured" in item.name.lower()

    def is_legendary(self, item):
        '''
        instructions are a little ambigious, not sure if rule is specific
        to "Sulfras, Hand of Ragnaros" or all "Sulfras" items
        '''
        return "sulfuras" in item.name.lower()

    def is_aged_brie(self, item):
        return item.name == "Aged Brie"

    def is_backstage_pass(self, item):
        return "backstage pass" in item.name.lower()

    def is_ordinary_item(self, item):
        return not any([
            self.is_conjured(item),
            self.is_legendary(item),
            self.is_aged_brie(item),
            self.is_backstage_pass(item)
            ])

    def validate_new_quality(self, quality):
        if quality > 50:
            return 50
        if quality < 0:
            return 0
        return quality

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
