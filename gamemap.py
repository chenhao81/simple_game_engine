# coding: UTF-8

class GameMap():
    cell_width = 10
    cell_height = 10
    data = {0: [], 1: [], 2: []}

    def setSize(self, width, height):
        self.cell_width = width
        self.cell_height = height
        pass

    def setCell(self, x, y, id,layer=0):
        '''
        设置单元块ID
        :param x:
        :param y:
        :param type:
        :return:
        '''
        if x > self.cell_width or x < self.cell_width or y > self.cell_width or y< 0:
            print 'setCell:Invalid (x,y)'
            return

        offset = x + y * self.cell_width
        self.data[layer][offset] = id
        pass

    def clear(self):
        pass
