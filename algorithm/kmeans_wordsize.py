# -*- coding: utf-8 -*-
# coding=utf-8

class KmeansWordSize:
    """
    clustering the word size for 3 class
    """

    def cluster(self, item, chart_item):
        # 0. result content
        word_level_1 = ''
        word_level_2 = ''
        word_level_3 = ''
        center_list = []
        # 1. compute the word size
        word_size = []
        for text in chart_item['text_info']:
            t = text['text']
            length = len(t)
            bbox_size = text['bbox'][1]
            width = bbox_size[0]
            hight = bbox_size[1]
            size = width*hight/length

            word_size.append(size)

        # 2. sort the word size
        word_size.sort()
        word_size.reverse()
        # 3. initialize 3 class center
        length = len(word_size)
        if length <= 3 and length >=1:
            center_1 = word_size[0]
            center_list.append(center_1)
            if length >= 2:
                center_2 = word_size[1]
                center_list.append(center_2)
            if length >= 3:
                center_3 = word_size[2]
                center_list.append(center_3)

        elif length > 3:
            mod = length % 2
            div = length / 2
            center_1 = word_size[0]
            center_list.append(center_1)

            if mod == 0:
                center_2 = (word_size[div-1] + word_size[div])/2
                center_list.append(center_2)
            else:
                center_2 = word_size[div]
                center_list.append(center_2)

            center_3 = word_size[-1]
            center_list.append(center_3)

        # 4. classification to 3 class
        for text in chart_item['text_info']:
            t = text['text']
            length = len(t)
            bbox_size = text['bbox'][1]
            width = bbox_size[0]
            hight = bbox_size[1]
            size = width*hight/length

            result = self.judgeNeighborClass(center_list, size)

            if result == 1:
                word_level_1 = word_level_1 + t
            elif result == 2:
                word_level_2 = word_level_2 + t
            elif result == 3:
                word_level_3 = word_level_3 + t

        item['word_imp_level_1'] = word_level_1
        item['word_imp_level_2'] = word_level_2
        item['word_imp_level_3'] = word_level_3
        return item


    def judgeNeighborClass(self, center_list, sample):
        result = 0
        index = 0
        distance = center_list[0]
        for center in center_list:
            index = index + 1
            n_dis = abs(sample - center)
            if n_dis < distance:
                result = index
                distance = n_dis
        return result