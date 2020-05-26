odoo.define('ruby.custom_list_view', function (require) {
    'use strict';
    
    var Dialog = require("web.Dialog");
    var core = require("web.core");
    var _t = core._t;
    let ListController = require('web.ListController');
    ListController.include({
        renderButtons: function($node) {
            this._super.apply(this, arguments);
            if (this.$buttons && this.modelName == 'sale.order.management') {
                this.$buttons.find('.o_button_process_csv').on('click', this.proxy('redirect_to_process_csv'));
                this.$buttons.find('.o_button_deliver_order').on('click', this.proxy('redirect_to_delivered_order'));
                this.$buttons.find('.o_button_returned_order').on('click', this.proxy('redirect_to_returned_order'));
            }
            if (this.$buttons && this.modelName == 'shopee.management'){
                this.$buttons.find('.o_button_process_excel').on('click', this.proxy('redirect_to_process_excel'));
            }
        },

        redirect_to_process_csv: function(event) {
            event.stopPropagation();
            event.preventDefault();
            var d = $.Deferred();
            var self = this;
            var button = [{
                text: _t("OK"),
                close: true,
                click: function() {
                    if (d) d.reject();
                    d = null;
                    location.reload();
                }
            }];
            return this._rpc({
                model: 'sale.order.management',
                method: 'btn_process_csv',
                args: [{}]
            }).then(function(data){
                var msg_type = data.messages[0].type
                var msg = data.messages[0].message
                var view_id = data.messages[0].view_id
                var message = "";
                if (msg_type == "Error"){
                    message = msg
                }else{
                    var body = "";
                    for (var i = 0; i < msg.length; i++){
                        var data = msg[i];
                        var shop = data.shop;
                        var create = data.create;
                        var del = data.del;
                        body += "<tr class=\"o_data_row\"><td class=\"o_data_cell o_readonly_modifier\">"+shop+"</td><td>"+create+"</td><td>"+del+"</td></tr>"
                    }
                    message = "<table class=\"o_list_view table table-sm table-hover table-striped o_list_view_ungrouped\"><thread><tr><th>Shop</th><th>Create</th><th>Delete</th></tr></thread><tbody>"+body+"</tbody></table>"
                }
                return self.do_action({
                    name: 'Result',
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: 'shop.announce',
                    views: [[view_id, 'form']],
                    target: 'new',
                    context: {
                        default_message: message,
                        default_model: 'sale.order.management'
                    }
                })
            })
        },

        redirect_to_process_sale_done: function(event){
            event.stopPropagation();
            event.preventDefault();
            return this._rpc({
                model: 'sale.order.management',
                method: 'btn_process_sale_done',
                args: [{}]
            }).then(function(data){
                var msg_type = data.messages[0].type
                var msg = data.messages[0].message
                var message = "";
                msg.forEach(function(item,idx,array){
                    if(idx === array.length-1){
                        message+= item;
                    }else{
                        message+= item+" | ";
                    }
                })
                Dialog.alert(this, msg,{
                $content: $("<main/>", {
                    role: "alert",
                    text: message
                }),
                title: msg_type
                });
            })
        },

        redirect_to_reconcile: function(event){
            event.stopPropagation();
            event.preventDefault();
            return this.do_action({
                name: 'Reconcile Date',
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'set.reconcile.date',
                views: [[false, 'form']],
                target: 'new',
                context: {}
            })
        },

        redirect_to_process_excel: function(event){
            event.stopPropagation();
            event.preventDefault();
            var d = $.Deferred();
            var self = this;
            var button = [{
                text: _t("OK"),
                close: true,
                click: function() {
                    if (d) d.reject();
                    d = null;
                    location.reload();
                }
            }];
            return this._rpc({
                model: 'shopee.management',
                method: 'btn_process_excel',
                args: [{}]
            }).then(function(data){
                var msg_type = data.messages[0].type
                var msg = data.messages[0].message
                var view_id = data.messages[0].view_id
                var message = "";
                if (msg_type == "Error"){
                    message = msg
                }else{
                    var body = "";
                    for (var i = 0; i < msg.length; i++){
                        var data = msg[i];
                        var shop = data.shop;
                        var create = data.create;
                        var del = data.del;
                        body += "<tr class=\"o_data_row\"><td class=\"o_data_cell o_readonly_modifier\">"+shop+"</td><td>"+create+"</td><td>"+del+"</td></tr>"
                    }
                    message = "<table class=\"o_list_view table table-sm table-hover table-striped o_list_view_ungrouped\"><thread><tr><th>Shop</th><th>Create</th><th>Delete</th></tr></thread><tbody>"+body+"</tbody></table>"
                }
                return self.do_action({
                    name: 'Result',
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: 'shop.announce',
                    views: [[view_id, 'form']],
                    target: 'new',
                    context: {
                        default_message: message,
                        default_model: 'shopee.management'
                    }
                })
            })
        },
        

    });

    core.action_registry.add('sale.order.management', ListController);
    // return the object.
    return ListController;
});