import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys

class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        # Gtk.Window.__init__(self, title="Potato trainer", application=app)
        super(Gtk.Window, self).__init__(title="Potato trainer", application=app)
        self.set_default_size(200, 100)

        # add a label
        label = Gtk.Label()
        label.set_text("hello world")
        self.add(label)


class MyApplication(Gtk.Application):

    def __init__(self):
        super(Gtk.Application, self).__init__()

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


if __name__ == '__main__':
    app = MyApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
