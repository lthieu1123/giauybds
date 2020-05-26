odoo.define('ecc_approval_process.FormController', function (require) {
    "use strict";
    var core = require('web.core');
    var FormControler = require('web.FormController');
    var _t = core._t;
    var qweb = core.qweb;

    FormControler.include({
        /**
         * @override
         */

        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            var _self = this;
            var d = _self.model.get(this.handle);
            if (d && (d.model=='set.order.to.delivered' || d.model=='set.order.to.returned' || d.model=='set.order.to.delivered.shopee' || d.model=='set.order.to.returned.shopee') && d.viewType=='form') {
                var myAudio = $('#audioFound')
                if (!myAudio || myAudio.length==0) {
                    $('body').append('<audio id="audioFound" src="/ruby/static/src/sounds/co.mp3" type="audio/mpeg"></audio>');                    
                    $('body').append('<audio id="audioNotFound" src="/ruby/static/src/sounds/khong.mp3" type="audio/mpeg"></audio>');  
                    $('body').append('<audio id="audioDuplicated" src="/ruby/static/src/sounds/trung.mp3" type="audio/mpeg"></audio>');
                    $('body').append('<audio id="audioUsed" src="/ruby/static/src/sounds/da_nhap.mp3" type="audio/mpeg"></audio>');                                      
                }
                var tracking_code_count_id = document.getElementsByName('tracking_code_ids');
                var loopCount = 0;
                var handler = {};
                handler.old_value = 0;

                var iid = setInterval(function() {
                    if (tracking_code_count_id && tracking_code_count_id.length){
                        
                        tracking_code_count_id[0].addEventListener("change",function(){
                            var current = $(this).val().toUpperCase();
                            var _model = d.model;
                            _self._rpc({
                                model: _model,
                                method: "find_order",
                                args: [
                                    {
                                    order_number: current
                                    }
                                ]
                            }).then(function(result){
                                var _res = result.result
                                if (_res === true){
                                    var el = $("[name='existed_tracking_code']")[0]
                                    var isFoundInTable = false;
                                    var text = el.value;
                                    if (text.includes(current)){
                                        isFoundInTable = true;
                                    }
                                    if (isFoundInTable){
                                        var e = document.getElementById("audioDuplicated");
                                        e.play();
                                    }else{
                                        var e = document.getElementById("audioFound");
                                        e.play();
                                    }
                                }else if (_res === false){
                                    var e = document.getElementById("audioNotFound");
                                    e.play();
                                }else{
                                    var e = document.getElementById("audioUsed");
                                    e.play();
                                }
                            })
                        });
                        _self.addListenerToTrackingCode = true;
                        if (iid) clearInterval(iid);
                    }else{
                        tracking_code_count_id = document.getElementsByName('tracking_code_ids')
                        if (loopCount++ > 30 && iid) clearInterval(iid);
                    }
                },100);
            }
        },
        

        _updateEnv: function () {
            this._super.apply(this, arguments);
            var _super = this._super.bind(this);
            var _self = this;
            var d = _self.model.get(this.handle);
            if (d && (d.model=='set.order.to.delivered' || d.model=='set.order.to.returned' || d.model=='set.order.to.delivered.shopee' || d.model=='set.order.to.returned.shopee') && d.viewType=='form') {
                var myAudio = $('#audioFound')
                if (!myAudio || myAudio.length==0) {
                    $('body').append('<audio id="audioFound" src="/ruby/static/src/sounds/co.mp3" type="audio/mpeg"></audio>');                    
                    $('body').append('<audio id="audioNotFound" src="/ruby/static/src/sounds/khong.mp3" type="audio/mpeg"></audio>');
                    $('body').append('<audio id="audioDuplicated" src="/ruby/static/src/sounds/trung.mp3" type="audio/mpeg"></audio>');
                    $('body').append('<audio id="audioUsed" src="/ruby/static/src/sounds/da_nhap.mp3" type="audio/mpeg"></audio>');                    
                }
                var tracking_code_count_id = document.getElementsByName('tracking_code_ids');
                var loopCount = 0;
                var handler = {};
                handler.old_value = 0;
                if (!_self.addListenerToTrackingCode){
                    var iid = setInterval(function() {
                        if (tracking_code_count_id && tracking_code_count_id.length){
                            tracking_code_count_id[0].addEventListener("change",function(){
                                var current = $(this).val().toUpperCase();
                                var changes = _self.model.localData[d.id];
                                var _model = d.model;
                                _self._rpc({
                                    model: _model,
                                    method: "find_order",
                                    args: [
                                        {
                                        order_number: current
                                        }
                                    ]
                                }).then(function(result){
                                    var _res = result.result
                                    if (_res === true){
                                        var el = $("[name='existed_tracking_code']")[0]
                                        var isFoundInTable = false;
                                        var text = el.value;
                                        if (text.includes(current)){
                                            isFoundInTable = true;
                                        }
                                        if (isFoundInTable){
                                            var e = document.getElementById("audioDuplicated");
                                            e.play();
                                        }else{
                                            var e = document.getElementById("audioFound");
                                            e.play();
                                        }
                                    }else if (_res === false){
                                        var e = document.getElementById("audioNotFound");
                                        e.play();
                                    }else{
                                        var e = document.getElementById("audioUsed");
                                        e.play();
                                    }
                                })
                            });
                            if (iid) clearInterval(iid);
                        }else{
                            tracking_code_count_id = document.getElementsByName('tracking_code_ids')
                            if (loopCount++ > 30 && iid) clearInterval(iid);
                        }
                    },100);
                }
                
            }
        },
    });

});