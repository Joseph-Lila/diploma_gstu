from kivy.factory import Factory

from .screen_master import ScreenMasterView
from .loading_screen import LoadingScreenView

Factory.register("ScreenMasterView", cls=ScreenMasterView)
Factory.register("LoadingScreenView", cls=LoadingScreenView)
