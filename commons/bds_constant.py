# -*- coding: utf-8 -*-

from odoo.tools.translate import _

######################################
# Type OF REAL ESTATE
######################################

TRANSFER = 'transfer'
LAND = 'land'
BUILDING = 'building'
HOTEL = 'hotel'
PREMISES = 'premises'
HOUSE = 'house'
OFFICE = 'office'
ROOM = 'room'
APARTMENT = 'apartment'
HOMESTAY = 'homestay'
OTHER = 'other'

TYPE_OF_REAL_ESTATE = [
    (TRANSFER,'Transfer'),
    (LAND, 'Land'),
    (BUILDING, 'Building'),
    (HOTEL,'Hotel'),
    (PREMISES,'Premises'),
    (HOUSE,'House'),
    (OFFICE,'Office'),
    (ROOM,'Room'),
    (APARTMENT,'Apartment'),
    (HOMESTAY,'Homestay'),
    (OTHER,'Other')
]

######################################
# Type OF ROAD
######################################

FRONT_LINE = 'front_line'
CONNER_TWO_FRONT_LINES = 'conner_two_front_lines'
INTERNAL_ROAD = 'internal_road'
ALLEY_XH = 'alley_xh'
ALLEY_XM = 'alley_xm'
ALLEY_XT_ONE_FRONT_LINE_OR_ALLEY_FRONT_LINE = 'alley_xt_one_front_line_or_alley_front_line'
THREE_FRONT_LINES = 'three_front_lines'
FOUR_FRONT_LINES = 'four_front_lines'
LANE = 'lane'
ALLEY_MOTORCYCLE_TRUCK = 'alley_motorcycle_truck'

TYPE_OF_ROAD = [
    (FRONT_LINE,'Fron line'),
    (CONNER_TWO_FRONT_LINES,'Conner with 2 fron line'),
    (INTERNAL_ROAD,'Internal Road'),
    (ALLEY_XH,'Alley XH'),
    (ALLEY_XM,'Alley XM'),
    (ALLEY_XT_ONE_FRONT_LINE_OR_ALLEY_FRONT_LINE,'Alley XT with 1 fron line or Alley\'s front line'),
    (THREE_FRONT_LINES,'3 Front lines'),
    (FOUR_FRONT_LINES,'4 Front lines'),
    (LANE,'lane'),
    (ALLEY_MOTORCYCLE_TRUCK,'Alley allow motorcycle truck')
]

######################################
# DIRECTION
######################################
W_WNW = 'w_wnw'
