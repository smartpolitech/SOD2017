#Reader for RethinkDB based sensors

from PySide.QtCore import *
import rethinkdb as rdb
from tornado import ioloop, gen
import datetime as dt

class RDBReader(QThread):
	signalVal = Signal(str, dict)
	def __init__(self, connData):
		super(RDBReader, self).__init__()
		rdb.set_loop_type('tornado')
		#self.conn = rdb.connect(host=connData["host"], port=connData["port"], db=connData["db"], auth_key=connData["auth_key"])
		self.conn = rdb.connect(host=connData["host"], port=connData["port"], db=connData["db"])

	def addTable(self, ident):
		ioloop.IOLoop.current().add_callback(self.changes, self.conn, ident)

	@gen.coroutine
	def changes(self, conn, ident):
		connection = yield conn
		feed = yield rdb.table(ident).changes().run(connection)
		while (yield feed.fetch_next()):
			change = yield feed.next()
			self.signalVal.emit(ident, change["new_val"])

	def run(self):
		ioloop.IOLoop.current().start()
