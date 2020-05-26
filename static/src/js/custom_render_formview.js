odoo.define('bds.FormController', function (require) {
    "use strict";
    var config = require('web.config');
    var core = require('web.core');
    var dom = require('web.dom');
    var FormControler = require('web.FormController');
    var WebFormRenderer = require('web.FormRenderer');
    var FormView = require('web.FormView');
    var _t = core._t;
    var qweb = core.qweb;

    // WebFormRenderer.include({

    //     _renderHeaderButtons: function (node) {
    //         if (!isNaN(WebFormRenderer.approvalButtonId) && WebFormRenderer.isShowButton) {
    //             var buttonName = WebFormRenderer.approvalButtonId;
    //             if (node.tag === 'header' && !node.children.find(function (e) { return e && e.tag === 'button' && e.attrs.name === buttonName; })) {
    //                 node.children.push({ tag: 'button', attrs: { name: buttonName, string: _t('Approve Status'), type: 'action', class: 'class_tracking_show_button' }, children: [] });
    //             }
    //         }
    //         return this._super.apply(this, arguments);
    //     },
    // });

    FormControler.include({
        /**
         * @override
         */

        // init: function (parent, model, renderer, params) {
        //     this._super.apply(this, arguments);
        //     var d = this.model.get(this.handle);
        //     if (d) {
                
        //     }

        // },
        /**
         * @override
         */
        // start: function () {
        //     var _self = this;
        //     var _super = _self._super.bind(this);
        //     var _args = arguments;
        //     return $.when(
        //         _self._rpc({ model: "ecc.approval.status", method: "get_action_id", args: [{}] }).then(function (_id) {
        //             WebFormRenderer.approvalButtonId = _id;
        //         }).fail(function (err) { console.log("ERROR: ", err); })
        //     ).then(function () {
        //         return _super.apply(_self, _args)
        //     })
        // },

        _updateEnv: function () {
            this._super.apply(this, arguments);
            var house_no = this.$('span.o_house_no');
            var btn_save = this.$('button.o_form_button_edit')
            var d = this.model && this.handle && house_no && house_no.removeClass && house_no.addClass && this.model.get(this.handle);
            console.log('d.data.is_show_house_no: ',d.data.is_show_house_no);
            console.log('btn_save: ',btn_save);
            if (d && d.model === 'crm.product' && !d.data.is_show_house_no){
                house_no.remove();
            }
        },
    });

    FormView.include({
        load_record: function(record) {
            this._super.apply(this, arguments);
            if (this.model=='crm.product' && !this.model.data.is_show_house_no){
                console.log('This is basssste');
                this.$buttons.find('button.o_form_button_edit').css({"display":"none"});
            }
            
        }
        
    });

});