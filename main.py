import gtk 
import webkit 
import os

directory=os.getcwd();

view = webkit.WebView() 

sw = gtk.ScrolledWindow() 
sw.add(view) 

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
win.fullscreen(); 
win.add(sw) 
win.show_all() 

view.open(directory+"/index.html"); 
gtk.main()
