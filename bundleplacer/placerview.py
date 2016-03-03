# -*- mode: python; -*-
#
# Copyright 2015 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from urwid import WidgetWrap
from bundleplacer.ui import PlacementView
from ubuntui.ev import EventLoop

from bundleplacer.assignmenttype import AssignmentType

log = logging.getLogger('bundleplacer')


class PlacerView(WidgetWrap):
    def __init__(self, placement_controller, config, cb):
        self.placement_controller = placement_controller
        self.config = config
        self.cb = cb
        self.selected_machine = None
        self.selected_charm = None
        self.pv = PlacementView(
            display_controller=self,
            placement_controller=self.placement_controller,
            config=self.config,
            do_deploy_cb=self.do_deploy)
        super().__init__(self.pv)
        self.pv.reset_selections(top=True)

    def update(self, *args, **kwargs):
        self.pv.update()
        EventLoop.set_alarm_in(1, self.update)

    def status_error_message(self, message):
        pass

    def status_info_message(self, message):
        pass

    def do_deploy(self):
        self.cb()

    def _do_select(self, machine, atype):
        self.placement_controller.assign(machine,
                                         self.selected_charm,
                                         atype)
        self.pv.reset_selections()

    def do_select_baremetal(self, machine):
        self._do_select(machine, AssignmentType.BareMetal)

    def do_select_lxc(self, machine):
        self._do_select(machine, AssignmentType.LXC)

    def do_select_kvm(self, machine):
        self._do_select(machine, AssignmentType.KVM)

    def set_selected_charm(self, charm):
        self.selected_charm = charm

    def edit_placement(self):
        self.pv.edit_placement()

    def edit_relations(self):
        self.pv.edit_relations()
