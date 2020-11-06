# -*- coding: utf-8 -*-

import base64
import codecs
import collections
import unicodedata

import chardet
import datetime
import io
import itertools
import logging
import psycopg2
import operator
import os
import re
import requests

from PIL import Image

from odoo import api, fields, models, exceptions
from odoo.exceptions import AccessError
from odoo.tools.translate import _
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools import config, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat


class Import(models.TransientModel):
    _inherit = 'base_import.import'

    @api.multi
    def do(self, fields, columns, options, dryrun=False):
        if not self.env.user.has_group('base.group_system'):
            raise exceptions.ValidationError('Bạn không có quyền nạp tập tin')
        return super().do(fields, columns, options, dryrun)
    