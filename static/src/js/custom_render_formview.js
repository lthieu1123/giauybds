odoo.define('rubyshop.custom_form_view', function (require) {
    'use strict';

    const core = require('web.core');
    var FormController = require('web.FormController');
    var WebFormRenderer = require('web.FormRenderer');

    FormController.include({
        _updateEnv: function () {
            this._super.apply(this, arguments);
            var btn = $('.o_form_buttons_edit');
            var breadcrumb = $('li.breadcrumb-item.active');
            if (this.model && this.model.get && this.handle && btn && btn.removeClass && btn.addClass) {
                var count = 0;
                var delayCount = 0;
                var d = this.model.get(this.handle);
                if (d.model == 'set.order.to.delivered' || d.model == 'set.order.to.returned' || d.model == 'set.order.to.delivered.shopee' || d.model == 'set.order.to.returned.shopee') {
                    var iid = setInterval(function () {
                        if (btn && btn.length) {
                            btn.addClass('o_invisible_modifier');
                            breadcrumb = $('li.breadcrumb-item.active')[0]
                            if (d.model == 'set.order.to.delivered' || d.model == 'set.order.to.delivered.shopee') {
                                breadcrumb.innerText = "Giao Hàng";
                            } else if (d.model == 'set.order.to.returned' || d.model == 'set.order.to.returned.shopee') {
                                breadcrumb.innerText = "Hàng Trả";
                            }
                            clearInterval(iid);
                        }
                        if (delayCount++ < 3) return;
                        btn = $('.o_form_buttons_edit');
                        if (count++ >= 30) clearInterval(iid);
                    }, 300);
                }
            }

        }
    });
});