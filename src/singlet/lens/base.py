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

from gi.repository import GLib, GObject, Gio
from gi.repository import Dee
# FIXME: Some weird bug in Dee or PyGI makes Dee fail unless we probe
#        it *before* we import the Unity module... ?!
_m = dir(Dee.SequenceModel)
from gi.repository import Unity


class LensBuilder(type):
    '''
    MetaClass for building Lens classes and subclasses
    '''

    def __new__(cls, name, bases, attrs):
        #import pdb; pdb.set_trace()
        super_new = super(LensBuilder, cls).__new__
        parents = [b for b in bases if isinstance(b, LensBuilder)]
        if not parents:
            # If this isn't a subclass of LensBuilder, don't do anything special.
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})

        attr_meta = attrs.pop('Meta', None)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        base_meta = getattr(new_class, '_meta', None)

        setattr(new_class, '_meta', LensMeta(meta))

        for aName, a in attrs.items():
            if isinstance(a, Unity.Scope):
                new_class._meta.scope_dict[aName] = a
                if not hasattr(meta, 'scope_order'):
                    new_class._meta.scope_order.append(aName)

            elif isinstance(a, Unity.Category):
                new_class._meta.category_dict[aName] = a
                if not hasattr(meta, 'category_order'):
                    new_class._meta.category_order.append(aName)
                setattr(new_class, aName, new_class._meta.category_order.index(aName))

            elif isinstance(a, Unity.Filter):
                new_class._meta.filter_dict[aName] = a
                if not hasattr(meta, 'filter_order'):
                    new_class._meta.filter_order.append(aName)

            else:
                setattr(new_class, aName, a)

        return new_class


class LensMeta(object):
    '''
    Metadata object for a Lens
    '''

    def __init__(self, meta):
        self.name = getattr(meta, 'name', '')

        self.bus_name = getattr(meta, 'bus_name', 'unity.singlet.lens.%s' % self.name)
        self.bus_path = getattr(meta, 'bus_path', '/'+str(self.bus_name).replace('.', '/'))

        self.category_dict = dict()
        self.category_order = getattr(meta, 'category_order', [])
        self.filter_dict = dict()
        self.filter_order = getattr(meta, 'filter_order', [])
        self.scope_dict = dict()
        self.scope_order = getattr(meta, 'scope_order', [])

        self.search_on_blank = getattr(meta, 'search_on_blank', False)

        self.description = getattr(meta, 'description', '%s Lens' % self.name.title())
        self.search_hint = getattr(meta, 'search_hint', '%s Search' % self.name.title())
        self.icon = getattr(meta, 'icon', '/usr/share/icons/Humanity/mimes/24/unknown.svg')

    @property
    def categories(self):
        return [self.category_dict[c] for c in self.category_order]

    @property
    def scopes(self):
        return [self.scope_dict[s] for s in self.scope_order]

    @property
    def filters(self):
        return [self.filter_dict[f] for f in self.filter_order]


class Lens(object):
    __metaclass__ = LensBuilder
    
    def __init__(self):
        self._lens = Unity.Lens.new (self._meta.bus_name, self._meta.name)

        self._lens.props.search_hint = "Define Scope"
        self._lens.props.visible = True;
        self._lens.props.search_in_global = False;

        # Populate categories
        self._lens.props.categories = self._meta.categories
        
        # Populate filters
        self._lens.props.filters = self._meta.filters

        # Populate scopes
        for scope in self._meta.scopes:
            self._lens.add_local_scope (scope);
            
        self._lens.export ()


class SingleScopeLens(Lens):

    def __init__(self):
        self._lens = Unity.Lens.new (self._meta.bus_path, self._meta.name)

        self._lens.props.search_hint = "%s Lens" % self._meta.name.title()
        self._lens.props.visible = True;
        self._lens.props.search_in_global = True;

        # Populate categories
        self._lens.props.categories = self._meta.categories
        
        # Populate filters
        self._lens.props.filters = self._meta.filters

        # Populate scopes
        self._scope = Unity.Scope.new ("%s/main" % self._meta.bus_path)
        self._scope.connect ("notify::active-search", self.on_search_changed)
        self._scope.connect ("filters-changed", self.on_search_changed);
        self._scope.connect ("notify::active", self.on_search_changed);
        if hasattr(self, 'handle_uri'):
            self._scope.connect('activate-uri', self.handle_uri)
        self._scope.export()
        self._lens.add_local_scope (self._scope);
        
        self._lens.export ()

    def thaw(self, entry):
        entry.thaw_notify()
        return False

    def on_search_changed (self, entry, *args):
        # Prevent concurrent searches and concurrent updates of our models,
        # by preventing any notify signals from propagating to us.
        # Important: Remember to thaw the notifys again! 
        entry.freeze_notify ()
        
        search = self._scope.props.active_search or None
        if search:
            search_string = search.props.search_string
        else:
            search_string = None

        if self._meta.search_on_blank or (search_string is not None and search_string != ''):
            results = self._scope.props.results_model
            results.clear()
            self.search(search_string, results)

        GObject.idle_add(self.thaw, entry)

    def hide_dash_response(self, uri=''):
        return Unity.ActivationResponse(handled=Unity.HandledType.HIDE_DASH, goto_uri=uri)
        
    def update_dash_response(self, uri=''):
        return Unity.ActivationResponse(handled=Unity.HandledType.SHOW_DASH, goto_uri=uri)
        
    def search(self, phrase, results):
        pass
