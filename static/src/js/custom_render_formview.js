odoo.define('bds.FormController', function (require) {
    "use strict";
    var config = require('web.config');
    var core = require('web.core');
    var dom = require('web.dom');
    var FormController = require('web.FormController');
    var WebFormRenderer = require('web.FormRenderer');
    var FormView = require('web.FormView');
    var _t = core._t;
    var qweb = core.qweb;

    FormController.include({

        _updateEnv: function () {
            this._super.apply(this, arguments);
            var house_no = this.$('span.bds_show_house_no');
            var phone_no = this.$('div.bds_show_phone_no');
            var map = this.$('li.bds_show_map');
            var attachment = this.$('button.o_chatter_button_attachment');
            var active_attach = this.$('dev.o_mail_chatter_attachments');
            var class_active_attach = 'o_active_attach';
            var d = this.model && this.handle && house_no && house_no.removeClass && house_no.addClass && this.model.get(this.handle);
            //Remove all elememt to restrict user access (RCUD)
            if (d && d.model === 'crm.product'){
                if (!d.data.is_brokerage_specialist){
                    if (!d.data.is_show_attachment){
                        if (attachment.hasClass(class_active_attach)){
                            var active_attach = this.$('dev.o_mail_chatter_attachments');
                            active_attach.addClass('o_invisible_modifier');
                        }
                        attachment.addClass('o_invisible_modifier');
                    }else{
                        attachment.removeClass('o_invisible_modifier');
                    }
                    if (!d.data.is_show_house_no) {
                        house_no.remove();
                        phone_no.remove();
                    }
                    if (!d.data.is_show_map) map.remove();
                }
            }
        },

        /*
        * This function is override super function that will be show the warning when you try to edit the record
        * and do not accept user to edit
        */
        // _onEdit: function () {
        //     var d = this.model && this.handle && this.model.get(this.handle);
        //     if (d && d.model === 'crm.product' && !d.data.is_brokerage_specialist) this.do_warn("Bạn không có quyền sửa hồ sơ này");
        //     else this._setMode('edit');
        // },
    });

});