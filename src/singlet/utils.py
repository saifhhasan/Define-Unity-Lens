#! /usr/bin/python

#    Copyright (c) 2011 David Calle <davidc@framli.eu>
#    Copyright (c) 2011 Michael Hall <mhall119@gmail.com>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import shutil

from gi.repository import GLib, GObject, Gio


def run_lens(lens_class, args=None):
    if args and len(args) > 1 and args[1] == 'make':
        build_lens_files(lens_class, args)
    elif args and len(args) > 1 and args[1] == 'install':
        install_lens_files(lens_class, args)
    elif args and len(args) > 1 and args[1] == 'uninstall':
        uninstall_lens_files(lens_class, args)
    else:
        run_lens_daemon(lens_class)

def build_lens_files(lens_class, args):
    service_file = open('./unity-%s-lens.service' % lens_class._meta.name, 'w')
    service_file.write('''[D-BUS Service]
Name=%s
Exec=/usr/lib/singlet/%s
''' % (lens_class._meta.bus_name, args[0]))
    service_file.close()

    lens_file = open('./%s.lens' % lens_class._meta.name, 'w')
    lens_file.write('''[Lens]
DBusName=%(bus_name)s
DBusPath=%(bus_path)s
Name=%(title)s Lens
Icon=/usr/share/unity/lenses/%(name)s/%(icon_name)s
Description=%(description)s
SearchHint=%(search_hint)s
#Shortcut=c

[Desktop Entry]
X-Ubuntu-Gettext-Domain=%(name)s
''' % {
        'name': lens_class._meta.name,
        'title': lens_class._meta.name.title(),
        'description': lens_class._meta.description,
        'search_hint': lens_class._meta.search_hint,
        'icon_name': os.path.basename(lens_class._meta.icon),
        'bus_path': lens_class._meta.bus_path,
        'bus_name': lens_class._meta.bus_name })
    lens_file.close()

def install_lens_files(lens_class, args):
    if not os.path.exists('/usr/share/unity/lenses/%s' % lens_class._meta.name):
        os.mkdir('/usr/share/unity/lenses/%s' % lens_class._meta.name)
    shutil.copy('./unity-%s-lens.service' % lens_class._meta.name, '/usr/share/dbus-1/services/')
    shutil.copy('./%s.lens' % lens_class._meta.name, '/usr/share/unity/lenses/%s' % lens_class._meta.name)
    shutil.copy(lens_class._meta.icon, '/usr/share/unity/lenses/%s' % lens_class._meta.name)

    if not os.path.exists('/usr/lib/singlet'):
        os.mkdir('/usr/lib/singlet')
    shutil.copy(args[0], '/usr/lib/singlet/')
    
def uninstall_lens_files(lens_class, args):
    os.remove(os.path.join('/usr/share/dbus-1/services/', 'unity-%s-lens.service' % lens_class._meta.name))
    os.remove(os.path.join('/usr/share/unity/lenses/%s' % lens_class._meta.name, '%s.lens' % lens_class._meta.name))
    os.remove(os.path.join('/usr/share/unity/lenses/%s' % lens_class._meta.name, os.path.basename(lens_class._meta.icon)))
    os.rmdir('/usr/share/unity/lenses/%s' % lens_class._meta.name)
    
    os.remove(os.path.join('/usr/lib/singlet/', args[0]))
    
def run_lens_daemon(lens_class):
    session_bus_connection = Gio.bus_get_sync (Gio.BusType.SESSION, None)
    session_bus = Gio.DBusProxy.new_sync (session_bus_connection, 0, None,
                                          'org.freedesktop.DBus',
                                          '/org/freedesktop/DBus',
                                          'org.freedesktop.DBus', None)
    result = session_bus.call_sync('RequestName',
                                   GLib.Variant ("(su)", (lens_class._meta.bus_name, 0x4)),
                                   0, -1, None)
                                   
    # Unpack variant response with signature "(u)". 1 means we got it.
    result = result.unpack()[0]
    
    if result != 1 :
        print >> sys.stderr, "Failed to own name %s. Bailing out." % lens_class._meta.bus_name
        raise SystemExit (1)
    
    lens = lens_class()
    GObject.MainLoop().run()
