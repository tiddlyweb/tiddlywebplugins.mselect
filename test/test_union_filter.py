from tiddlyweb import control
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.config import config
from tiddlywebplugins.mselect import init
from tiddlyweb.filters import FilterError

from tiddlywebplugins.utils import get_store

import py.test
import shutil


tiddlers = [Tiddler('1'), Tiddler('c'), Tiddler('a'), Tiddler('b')]

def setup_module(module):
    init(config)
    from tiddlywebplugins.mselect import test_mselect as tm
    module.test_mselect = tm
    try:
        shutil.rmtree('store')
    except:
        pass

def test_simple_mselect():
    selected_tiddlers = test_mselect('title:1,title:c', tiddlers)
    assert ['1','c'] == [tiddler.title for tiddler in selected_tiddlers]

def test_bad_format():
    selected_tiddlers = test_mselect('title:1,funk', tiddlers)
    py.test.raises(FilterError, 'list(selected_tiddlers)')

def test_mselect_separator():
    selected_tiddlers = test_mselect('title:1|title:c', tiddlers)
    assert [] == [tiddler.title for tiddler in selected_tiddlers]
    selected_tiddlers = test_mselect('title:1|title:c', tiddlers, {'tiddlyweb.config':
        {'mselect.separator': '|'}})
    assert ['1','c'] == [tiddler.title for tiddler in selected_tiddlers]
    selected_tiddlers = test_mselect('title:1,title:c', tiddlers, {'tiddlyweb.config':
        {'mselect.separator': '|'}})
    assert [] == [tiddler.title for tiddler in selected_tiddlers]

def test_in_a_recipe():
    from tiddlyweb.config import config
    store = get_store(config)
    bag = Bag('hi')
    store.put(bag)
    tiddler = Tiddler('thing1', 'hi')
    tiddler.tags = ['research']
    store.put(tiddler)
    tiddler = Tiddler('thing2', 'hi')
    store.put(tiddler)

    recipe1 = Recipe('oi')
    recipe1.set_recipe([('hi', 'mselect=tag:research')])
    recipe1.store = store
    recipe2 = Recipe('coi')
    recipe2.set_recipe([('hi', 'select=tag:research')])
    recipe2.store = store
    recipe3 = Recipe('boi')
    recipe3.set_recipe([('hi', '')])
    recipe3.store = store
    environ = {'tiddlyweb.store': store}
    tiddlers = list(control.get_tiddlers_from_recipe(recipe1, environ))
    assert len(tiddlers) == 1
    tiddlers = list(control.get_tiddlers_from_recipe(recipe2, environ))
    assert len(tiddlers) == 1
    tiddlers = list(control.get_tiddlers_from_recipe(recipe3, environ))
    assert len(tiddlers) == 2
