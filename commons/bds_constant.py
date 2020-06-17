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
    (TRANSFER,'Sang nhượng'),
    (LAND, 'Đất'),
    (BUILDING, 'Toàn nhà'),
    (HOTEL,'Khách sạn'),
    (PREMISES,'Mặt bằng'),
    (HOUSE,'Nhà nguyên căn'),
    (OFFICE,'Văn phòng'),
    (ROOM,'Phòng trọ'),
    (APARTMENT,'Căn hộ'),
    (HOMESTAY,'Homestay'),
    (OTHER,'Khác')
]

######################################
# Type OF ROAD
######################################

FRONT_LINE = 'front_line'
CONNER_TWO_FRONT_LINES = 'conner_two_front_lines'
INTERNAL_ROAD = 'internal_road'
ALLEY_XH = 'alley_xh'
ALLEY_XM = 'alley_xm'
ALLEY_XT = 'alley_xt'
ONE_FRONT_LINE_AND_ONE_FRONT_LINE_ALLEY = 'front_line_and_front_line_alley'
ALLEY_XT_ONE_FRONT_LINE_OR_ALLEY_FRONT_LINE = 'alley_xt_one_front_line_or_alley_front_line'
THREE_FRONT_LINES = 'three_front_lines'
FOUR_FRONT_LINES = 'four_front_lines'
LANE = 'lane'
ALLEY_MOTORCYCLE_TRUCK = 'alley_motorcycle_truck'

TYPE_OF_ROAD = [
    (FRONT_LINE,'Mặt tiền'),
    (CONNER_TWO_FRONT_LINES,'Góc 2 mặt tiền'),
    (INTERNAL_ROAD,'Đường nội bộ'),
    (ALLEY_XH,'Hẻm XH'),
    (ALLEY_XM,'Hẻm XM'),
    (ALLEY_XT,'Hẻm XT'),
    (ONE_FRONT_LINE_AND_ONE_FRONT_LINE_ALLEY,'1 MT đường & 1 MT hẻm'),
    (THREE_FRONT_LINES,'3 Mặt tiền'),
    (FOUR_FRONT_LINES,'4 Mặt tiền'),
    (LANE,'Đường nhỏ'),
    (ALLEY_MOTORCYCLE_TRUCK,'Hẻm xe ba gác')
]

######################################
# CARDINAL  DIRECTION
######################################
TAY_TTT = 't_ttt'
TN_TTT = 'tn_ttt'
TB_TTT = 'tb_ttt'
DB_TTT = 'db_ttt'
CB_DTT = 'cb_dtt'
CD_DTT = 'cd_dtt'
CN_DTT = 'cn_dtt'
DN_DTT = 'dn_dtt'

CARDINAL_DIRECTION = [
    (TAY_TTT, 'Tây - TTT'),
    (TN_TTT, 'Tây Nam - TTT'),
    (TB_TTT, 'Tây Bắc - TTT'),
    (DB_TTT, 'Đông Bắc - TTT'),
    (CB_DTT, 'Chính Bắc - DTT'),
    (CD_DTT, 'Chính Đông - DTT'),
    (CN_DTT, 'Chính Nam - DTT'),
    (DN_DTT, 'Đông Nam - DTT')
]

###############################
#MESSAGES
###############################
BODY_MSG = """<span><a href="http://localhost/web#model=res.partner&amp;id={0}" class="o_mail_redirect" data-oe-id="{1}" data-oe-model="res.partner" target="_blank">@{2}</a>{3}</span>"""