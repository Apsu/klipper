# Code for handling the kinematics of 3-axis diff robots
#
# Copyright (C) 2021 Evan Callicoat <apsu@propter.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging, math
import stepper

class DiffXYZKinematics:
    def __init__(self, toolhead, config):
        # Setup axis rails
        self.rails = [ stepper.PrinterRail(config.getsection('stepper_a')),
                       stepper.PrinterRail(config.getsection('stepper_b')),
                       stepper.PrinterRail(config.getsection('stepper_c')),
                       stepper.PrinterRail(config.getsection('stepper_d')) ]
        # Add endstops for every rail to every other rail
        #for rail in self.rails:
        #    for other in self.rails:
        #        if other != rail:
        #            rail.get_endstops()[0][0].add_stepper(other.get_steppers()[0])
        # 4 motor inputs
        self.rails[0].setup_itersolve('diffxyz_stepper_alloc', 'a')
        self.rails[1].setup_itersolve('diffxyz_stepper_alloc', 'b')
        self.rails[2].setup_itersolve('diffxyz_stepper_alloc', 'c')
        self.rails[3].setup_itersolve('diffxyz_stepper_alloc', 'd')
        for s in self.get_steppers():
            s.set_trapq(toolhead.get_trapq())
            toolhead.register_step_generator(s.generate_steps)
        config.get_printer().register_event_handler("stepper_enable:motor_off",
                                                    self._motor_off)
        # Setup boundary checks
#        max_velocity, max_accel = toolhead.get_max_velocity()
#        self.max_z_velocity = config.getfloat(
#            'max_z_velocity', max_velocity, above=0., maxval=max_velocity)
#        self.max_z_accel = config.getfloat(
#            'max_z_accel', max_accel, above=0., maxval=max_accel)
        self.limits = [(1.0, -1.0)] * 3
#        self.axes_min = toolhead.Coord(config.getfloat('min_x'),
#                                       config.getfloat('min_y'),
#                                       config.getfloat('min_z'), e=0.)
#        self.axes_max = toolhead.Coord(config.getfloat('max_x'),
#                                       config.getfloat('max_y'),
#                                       config.getfloat('max_z'), e=0.)
        # ranges = [r.get_range() for r in self.rails]
        # self.axes_min = toolhead.Coord(*[r[0] for r in ranges], e=0.)
        # self.axes_max = toolhead.Coord(*[r[1] for r in ranges], e=0.)
        # Setup stepper max halt velocity
        #max_halt_velocity = toolhead.get_max_axis_halt()
        #max_xy_halt_velocity = max_halt_velocity * math.sqrt(2.)
        #max_xy_accel = max_accel * math.sqrt(2.)
        #self.rails[0].set_max_jerk(max_xy_halt_velocity, max_xy_accel)
        #self.rails[1].set_max_jerk(max_xy_halt_velocity, max_xy_accel)
        #self.rails[2].set_max_jerk(max_xy_halt_velocity, max_xy_accel)
        #self.rails[3].set_max_jerk(max_xy_halt_velocity, max_xy_accel)
        # self.rails[2].set_max_jerk(
        #     min(max_halt_velocity, self.max_z_velocity), self.max_z_accel)
    def get_steppers(self):
        return [s for rail in self.rails for s in rail.get_steppers()]

    def calc_tag_position(self):
        pos = [rail.get_tag_position() for rail in self.rails]
        # x = (a + b)/2 - (c + d)/2
        # y = (a + b)/2 + (c + d)/2
        # z = (a - b)/2 + (c - d)/2
        return [ 0.5*(pos[0] + pos[1]) - 0.5*(pos[2] + pos[3]),
                 0.5*(pos[0] + pos[1]) + 0.5*(pos[2] + pos[3]),
                 0.5*(pos[0] - pos[1]) + 0.5*(pos[2] - pos[3]) ]

    def set_position(self, newpos, homing_axes):
        for i, rail in enumerate(self.rails):
            rail.set_position(newpos)
            if i in homing_axes:
                self.limits[i] = rail.get_range()

    def note_z_not_homed(self):
        # Helper for Safe Z Home
        self.limits[2] = (1.0, -1.0)

    def home(self, homing_state):
        pass

    def _motor_off(self, print_time):
        self.limits = [(1.0, -1.0)] * 3
#    def _check_endstops(self, move):
#        end_pos = move.end_pos
#        for i in (0, 1, 2):
#            if (move.axes_d[i]
#                and (end_pos[i] < self.limits[i][0]
#                     or end_pos[i] > self.limits[i][1])):
#                if self.limits[i][0] > self.limits[i][1]:
#                    raise move.move_error("Must home axis first")
#                raise move.move_error()
    def check_move(self, move):
        pass
    def get_status(self, eventtime):
        pass

def load_kinematics(toolhead, config):
    return DiffXYZKinematics(toolhead, config)
