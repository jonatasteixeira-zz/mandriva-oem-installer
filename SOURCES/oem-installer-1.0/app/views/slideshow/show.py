# Copyright (C) 2011 - Jonatas Teixeira <jonatast@mandriva.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SlideShow(QGraphicsView):
	def __init__(self, path):
		QGraphicsView.__init__(self)

		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.image_list = []
		self.image_index = 0

		self.get_images(path)

		self.scene = QGraphicsScene()
		self.setScene(self.scene)

		self.picture = QTimer()
		self.picture.start(120000)
		
		self.effect = QTimeLine(500)
		self.effect.setFrameRange(0, 1000)

		self.picture_update()

		self.connect_signals()
		self.show()

	def get_images(self, path):
		import os
		files = os.listdir(path)
		for file in files:
			if os.path.isfile(path + "/" + file):
				# TODO - Use a generic function to get the parent widgets size
				image = QPixmap(path + "/" + file).scaled(480, 365)
				self.image_list.append(image)

	def connect_signals(self):
		QObject.connect(self.picture, SIGNAL("timeout()"), self.picture_update)
		QObject.connect(self.effect, SIGNAL("frameChanged(int)"), self.effect_update)
		QObject.connect(self.effect, SIGNAL("finished()"), self.effect_finished)

	def effect_update(self, alpha):
		pixmap = QPixmap(self.current_image().size())
		pixmap.fill(Qt.transparent)
		 
		p = QPainter(pixmap)
		p.setCompositionMode(QPainter.CompositionMode_Source)
		p.drawPixmap(0, 0, self.current_image())
		p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
		p.fillRect(pixmap.rect(), QColor(0, 0, 0, 30))
		p.end()

		self.scene.addPixmap(pixmap)

	def effect_finished(self):
		self.scene.addPixmap(self.current_image())

	def picture_update(self):
		if self.image_index == len(self.image_list) - 1:
			self.image_index = 0
		else:
			self.image_index += 1

		self.effect.start()

	def current_image(self):
		return self.image_list[self.image_index]
		
