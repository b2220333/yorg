from itertools import product
from direct.gui.OnscreenText import OnscreenText
from yyagl.engine.gui.page import Page, PageGui, PageFacade
from yyagl.engine.gui.imgbtn import ImgBtn
from yyagl.engine.network.server import Server
from yyagl.gameobject import GameObject
from .carpage import CarPage, CarPageServer, CarPageProps
from .netmsgs import NetMsgs
from .thankspage import ThanksPageGui


class TrackPageProps(object):

    def __init__(self, cars, car_path, phys_path, tracks, tracks_tr, track_img,
                 player_name, drivers_img, cars_img, drivers):
        self.cars = cars
        self.car_path = car_path
        self.phys_path = phys_path
        self.tracks = tracks
        self.tracks_tr = tracks_tr
        self.track_img = track_img
        self.player_name = player_name
        self.drivers_img = drivers_img
        self.cars_img = cars_img
        self.drivers = drivers


class TrackPageGui(ThanksPageGui):

    def __init__(self, mdt, menu, trackpage_props):
        self.props = trackpage_props
        ThanksPageGui.__init__(self, mdt, menu)

    def bld_page(self):
        menu_gui = self.mdt.menu.gui
        widgets = [OnscreenText(text=_('Select the track'), pos=(0, .8),
                                **menu_gui.menu_args.text_args)]
        t_a = self.mdt.menu.gui.menu_args.text_args.copy()
        t_a['scale'] = .06
        tracks_per_row = 2
        for row, col in product(range(2), range(tracks_per_row)):
            if row * tracks_per_row + col >= len(self.props.tracks):
                break
            z_offset = 0 if len(self.props.tracks) > tracks_per_row else .35
            num_tracks = len(self.props.tracks) - tracks_per_row if row == 1 \
                else min(tracks_per_row, len(self.props.tracks))
            x_offset = .5 * (tracks_per_row - num_tracks)
            widgets += [ImgBtn(
                scale=.3,
                pos=(-.5 + col * 1.0 + x_offset, 1, .4 - z_offset - row * .7),
                frameColor=(0, 0, 0, 0),
                image=self.props.track_img % self.props.tracks[
                    col + row * tracks_per_row],
                command=self.on_track, extraArgs=[self.props.tracks[
                    col + row * tracks_per_row]],
                **self.mdt.menu.gui.menu_args.imgbtn_args)]
            txt = OnscreenText(
                self.props.tracks_tr()[col + row * tracks_per_row],
                pos=(-.5 + col * 1.0 + x_offset, .14 - z_offset - row * .7),
                **t_a)
            widgets += [txt]
        map(self.add_widget, widgets)
        ThanksPageGui.bld_page(self)

    def on_track(self, track):
        self.mdt.menu.track = track
        carpage_props = CarPageProps(
            self.props.cars, self.props.car_path, self.props.phys_path,
            self.props.player_name, self.props.drivers_img,
            self.props.cars_img, self.props.drivers)
        self.mdt.menu.push_page(CarPage(
            self.mdt.menu.gui.menu_args, carpage_props, self.mdt.menu))

    def destroy(self):
        if hasattr(self.mdt.menu, 'track'):
            del self.mdt.menu.track
        PageGui.destroy(self)


class TrackPageGuiServer(TrackPageGui):

    def on_track(self, track):
        self.menu.track = track
        self.menu.push_page(CarPageServer(self.menu))
        Server().send([NetMsgs.track_selected, track])


class TrackPage(Page):
    gui_cls = TrackPageGui

    def __init__(self, menu_args, trackpage_props, menu):
        self.menu_args = menu_args
        self.menu = menu
        init_lst = [
            [('event', self.event_cls, [self])],
            [('gui', self.gui_cls, [self, self.menu_args, trackpage_props])]]
        GameObject.__init__(self, init_lst)
        PageFacade.__init__(self)


class TrackPageServer(TrackPage):
    gui_cls = TrackPageGuiServer
