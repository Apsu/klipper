// CoreXY kinematics stepper pulse time generation
//
// Copyright (C) 2021 Evan Callicoat <apsu@propter.net>
//
// This file may be distributed under the terms of the GNU GPLv3 license.

#include <stdlib.h>    // malloc
#include <string.h>    // memset
#include "compiler.h"  // __visible
#include "itersolve.h" // struct stepper_kinematics
#include "trapq.h"     // move_get_coord

static double
diffxyz_stepper_a_calc_position(struct stepper_kinematics *sk, struct move *m, double move_time)
{
    struct coord c = move_get_coord(m, move_time);
    // return c.x + c.y;
    return (c.x + c.y) / 2.0 + c.z;
}

static double
diffxyz_stepper_b_calc_position(struct stepper_kinematics *sk, struct move *m, double move_time)
{
    struct coord c = move_get_coord(m, move_time);
    return (c.x + c.y) / 2.0 - c.z;
}

static double
diffxyz_stepper_c_calc_position(struct stepper_kinematics *sk, struct move *m, double move_time)
{
    struct coord c = move_get_coord(m, move_time);
    return (-c.x + c.y) / 2.0 + c.z;
}

static double
diffxyz_stepper_d_calc_position(struct stepper_kinematics *sk, struct move *m, double move_time)
{
    struct coord c = move_get_coord(m, move_time);
    return (-c.x + c.y) / 2.0 - c.z;
}

struct stepper_kinematics *__visible
diffxyz_stepper_alloc(char type)
{
    struct stepper_kinematics *sk = malloc(sizeof(*sk));
    memset(sk, 0, sizeof(*sk));
    switch (type)
    {
    case 'a':
        sk->calc_position_cb = diffxyz_stepper_a_calc_position;
        break;
    case 'b':
        sk->calc_position_cb = diffxyz_stepper_b_calc_position;
        break;
    case 'c':
        sk->calc_position_cb = diffxyz_stepper_c_calc_position;
        break;
    case 'd':
        sk->calc_position_cb = diffxyz_stepper_d_calc_position;
        break;
    }

    sk->active_flags = AF_X | AF_Y | AF_Z;
    return sk;
}
