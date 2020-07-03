# -*- coding: utf-8 -*-

from odoo.tools.translate import _

######################################
# REQUIREMENT
######################################
REQUIREMENT_PRODUCT = [('rental', 'Cho thuê'), ('sale', 'Cần bán')]
REQUIREMENT_REQUEST = [('rental', 'Cần thuê'), ('sale', 'Cần mua')]

######################################
# CURRENCY
######################################
CURRENCY = [('usd','$'),('mil','Triệu'),('bil','Tỷ')]

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
TWO_FRONT_LINES_ALLEY = 'two_front_lines_alley'

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
    (ALLEY_MOTORCYCLE_TRUCK,'Hẻm xe ba gác'),
    (TWO_FRONT_LINES_ALLEY,'2 mặt tiền hẽm')
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

######################################
# NHU CAU KINH DOANH
######################################
SHOP = 'shop'
CUA_HANG = 'cua_hang'
PHONG_GYM = 'phong_gym'
PHONG_KHAM = 'phong_kham'
PHONG_GAME = 'phong_game'
TRUONG_HOC = 'truong_hoc'
RAP_CHIEU_PHIM = 'rap_chieu_phim'
KHO = 'kho'
CAN_HO = 'can_ho'
PHONG_TRO = 'phong_tro'
KS = 'ks'
HT = 'ht'
NHA_HANG = 'nha_hang'
QUAN_AN = 'quan_an'
CAFE = 'cafe'
NGAN_HANG = 'ngan_hang'
SPA = 'spa'
SHOWROOM = 'showroom'
PHONG_XAM = 'phong_xam'
NHA_SACH = 'nha_sach'
SALON = 'salon'
BIDA = 'bida'
SIEU_THI = 'sieu_thi'
VAN_PHONG = 'van_phong'
BAR = 'bar'
THUOC_TAY = 'thuoc_tay'
MAT_KINH = 'mat_kinh'
NHA_O = 'nha_o'
KARAOKE = 'karaoke'
QUAN_NHAU = 'quan_nhau'
DAU_TU = 'dau_tu'


NCKD = [
    (DAU_TU,'ĐẦU TƯ'),    
    (NHA_O,'NHÀ Ở'),
    (SHOP, 'SHOP'),
    (CUA_HANG, 'CỬA HÀNG'),
    (PHONG_GYM, 'PHÒNG GYM'),
    (PHONG_KHAM, 'PHÒNG KHÁM'),
    (PHONG_GAME, 'PHÒNG GAME'),
    (TRUONG_HOC, 'TRƯỜNG HỌC'),
    (RAP_CHIEU_PHIM, 'RẠP CHIẾU PHIM'),
    (KHO, 'KHO'),
    (CAN_HO, 'CĂN HỘ'),
    (PHONG_TRO, 'PHÒNG TRỌ'),
    (KS, 'KS'),
    (HT, 'HT'),
    (NHA_HANG, 'NHÀ HÀNG'),
    (QUAN_AN, 'QUÁN ĂN'),
    (CAFE, 'CAFÉ'),
    (NGAN_HANG, 'NGÂN HÀNG'),
    (SPA, 'SPA'),
    (SHOWROOM, 'SHOWROOM'),
    (PHONG_XAM, 'PHÒNG XĂM'),
    (NHA_SACH, 'NHÀ SÁCH'),
    (SALON, 'SALON'),
    (BIDA, 'BIDA'),
    (SIEU_THI, 'SIÊU THỊ'),
    (VAN_PHONG, 'VĂN PHÒNG'),
    (BAR, 'BAR'),
    (THUOC_TAY, 'THUỐC TÂY'),
    (MAT_KINH,'MẮT KÍNH'),
    (KARAOKE,'KARAOKE'),
    (QUAN_NHAU,'QUÁN NHẬU'),
]


BODY_MSG = """<span><a href="{0}/web#model=res.partner&amp;id={1}" class="o_mail_redirect" data-oe-id="{2}" data-oe-model="res.partner" target="_blank">@{3}</a>{4}</span>""" 