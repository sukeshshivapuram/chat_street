odoo.define('odoov13_16.vendor_actions', function (require) {
"use strict";

var concurrency = require('web.concurrency');
var publicWidget = require('web.public.widget');
var utils = require('web.utils');
var Dialog = require('web.Dialog');

publicWidget.registry.VendorPurchaseActions = publicWidget.Widget.extend({
    selector: '#vendor_action_form',

    events: {
        // "change select[name='vendor_acceptence']": "check_visible_block",
        "change input[name='vendor_acceptence']": "show_submit_button",
        "change select[name='dispatch_status']": "show_submit_button",
        "change textarea[name='rejected_reason']": "show_submit_button",
        "change input[name='estimated_delivery_date']": "show_submit_button",

        "click #submit": "submit_data",
        "change input.bg-danger": "check_form_validity",
        "change textarea.bg-danger": "check_form_validity",



    },
    init: function(parent, options) {
        this._super(parent);
        this.dp = new concurrency.DropPrevious();
        this.check_visible_block();
        this.check_delivery_date();
        
    },
    willStart: function() {
        var def2 = this._super();
        
        return Promise.all([def2]);
    },

    check_delivery_date: function(){
         var estimated_delivery_date = $("input[name='estimated_delivery_date']").val();
         var recieptdate = $("input[name='reciept_date']").val();
         var aproved_status = $("select[name='approve_delivery_date']").val();
         var delivery_date_alert_div = $("div[name='delivery_date_alert']");
         var delivery_date_accept_alert_div = $("div[name='delivery_date_accept_alert']");
         var delivery_date_reject_alert_div = $("div[name='delivery_date_reject_alert']");
         var dispatch_status_field = $("select[name='dispatch_status']").val();
         if(recieptdate){

          var reciept_dateTimeSplit = recieptdate.split(' ');
          var reciept_date = reciept_dateTimeSplit[0];

         }
         if(estimated_delivery_date > reciept_date){
            if(aproved_status === 'accept' && dispatch_status_field == false){
                delivery_date_accept_alert_div.removeClass('d-none');
                // $("select[name='dispatch_status']").attr('disabled','');
                $("input[name='estimated_delivery_date']").attr('disabled','');
            }
            if(aproved_status == false){
                delivery_date_alert_div.removeClass('d-none');
                $("select[name='dispatch_status']").attr('disabled','');
            }
            if(aproved_status === 'reject'){
                delivery_date_reject_alert_div.removeClass('d-none');
                $("select[name='dispatch_status']").attr('disabled','');
            }
            if(aproved_status === 'accept' && dispatch_status_field == 'dispatch'){
               
                $("input[name='estimated_delivery_date']").attr('disabled','');
            }

         }
         if(estimated_delivery_date == false){
            $("select[name='dispatch_status']").attr('disabled','');
         }

         // console.log(estimated_delivery_date);
         console.log(aproved_status);


    },

    get_vendor_acceptence: function() {
        return {
            'vendor_acceptence': $("input[name='vendor_acceptence']:checked").val(),
            'estimated_delivery_date':$("input[name='estimated_delivery_date']").val(),
             };
    },

    get_dispatch_status: function() {
        return {
            'dispatch_state': $("select[name='dispatch_status']").val(),
             };
    },

    get_reject_reason: function() {
        return {
            'reject_reason': $("textarea[name='rejected_reason']").val(),
             };
    },

    get_advantages: function() {
        return {
            'vendor_acceptance_status': this.get_vendor_acceptence(),
            'dispatch_status':this.get_dispatch_status(),
            'rejected_reasons':this.get_reject_reason(),
        };
    },

    get_form_info: function() {
        var self = this;
         
        var advantages = self.get_advantages();
            // _.extend(advantages.personal_info);

        return {
            'order_id': parseInt($("input[name='order_id']").val()),
            'advantages': advantages,
            'original_link': $("input[name='original_link']").val(),
        };
     
    },

    show_submit_button: function(){
        var submit_button_div = $("div[name='submit_button']");
            submit_button_div.removeClass('d-none');
        var vend_acceptance = $("input[name='vendor_acceptence']:checked").val();
        var dispatch_status_field = $("select[name='dispatch_status']").val();
        var expceted_delivery_date_div = $("div[name='estimated_delivery_date']");
        var dispatch_status_div = $("div[name='dispatch_status']");
        var reject_reson_div = $("div[name='rejected_reason']");
        if(vend_acceptance === 'rejected') {
            reject_reson_div.removeClass('d-none');
            dispatch_status_div.addClass('d-none');
            expceted_delivery_date_div.addClass('d-none');
            $("textarea[name='rejected_reason']").attr('required', '');
            $("input[name='estimated_delivery_date']").removeAttr('required');
        }
        if(vend_acceptance === 'accepted') {
            reject_reson_div.addClass('d-none');
            dispatch_status_div.removeClass('d-none');
            expceted_delivery_date_div.removeClass('d-none');
            $("textarea[name='rejected_reason']").removeAttr('required');
            $("input[name='estimated_delivery_date']").attr('required', '');
        }
        // if(dispatch_status_field === 'dispatch'){
        //     $("select[name='dispatch_status']").attr('disabled','');
        // }

    },
    check_visible_block: function() {

        var vend_acceptance = $("input[name='vendor_acceptence']:checked").val();
        var dispatch_status_field = $("select[name='dispatch_status']").val();
        var expceted_delivery_date_div = $("div[name='estimated_delivery_date']");
        var dispatch_status_div = $("div[name='dispatch_status']");
        var reject_reson_div = $("div[name='rejected_reason']");

        var delivery_date_alert_div = $("div[name='delivery_date_alert']");
         var delivery_date_accept_alert_div = $("div[name='delivery_date_accept_alert']");
         var delivery_date_reject_alert_div = $("div[name='delivery_date_reject_alert']");

        if(vend_acceptance === 'rejected') {
            reject_reson_div.removeClass('d-none');
            dispatch_status_div.addClass('d-none');
            expceted_delivery_date_div.addClass('d-none');
            $("textarea[name='rejected_reason']").attr('required', '');
            $("input[name='estimated_delivery_date']").removeAttr('required');
        }
        if(vend_acceptance === 'accepted') {
            reject_reson_div.addClass('d-none');
            dispatch_status_div.removeClass('d-none');
            expceted_delivery_date_div.removeClass('d-none');
            $("textarea[name='rejected_reason']").removeAttr('required');
            $("input[name='estimated_delivery_date']").attr('required', '');
        }
        if(dispatch_status_field === 'dispatch'){
            $("select[name='dispatch_status']").attr('disabled','');
            delivery_date_alert_div.addClass('d-none');
            delivery_date_accept_alert_div.addClass('d-none');
            delivery_date_reject_alert_div.addClass('d-none');
        }
        if(vend_acceptance === 'rejected' || vend_acceptance === 'accepted' ){
            $("input[name='vendor_acceptence']").attr('disabled','');
        }
        
    },

    check_form_validity: function() {
        var required_empty_input = _.find($("input:required"), function(input) {return input.value === ''; });
        var required_empty_textarea = _.find($("textarea:required"), function(input) {return $("textarea[name='rejected_reason']").val() === ''; });
        var required_empty_select = _.find($("select:required"), function(select) {return $(select).val() === ''; });
        if(required_empty_input || required_empty_select || required_empty_textarea) {
            // $("button#submit").parent().append("<div class='alert alert-danger alert-dismissable fade show'>" + _('Some required fields are not filled') + "</div>");
            _.each($("input:required"), function(input) {
                if (input.value === '') {
                    Dialog.alert(this, "Please Update Estimated Delivery date");
                } else {
                    $(input).removeClass('bg-danger');
                }
            });
            _.each($("select:required"), function(select) {
                if ($(select).val() === '') {
                    $(select).parent().find('.select2-choice').addClass('bg-danger');
                } else {
                    $(select).parent().find('.select2-choice').removeClass('bg-danger');
                }
            });
            _.each($("textarea:required"), function(select) {
                if ($("textarea[name='rejected_reason']").val() === '') {
                   Dialog.alert(this, "Please provide Rejected Reason");
                } else {
                    $("textarea[name='rejected_reason']").removeClass('bg-danger');
                }
            });
        }
        // $(".alert").delay(4000).slideUp(200, function() {
        //     $(this).alert('close');
        // });
        return !required_empty_textarea && !required_empty_input && !required_empty_select;
    },

    submit_data: function(event) {
        var self = this;
        var originallink =  $("input[name='original_link']").val();

        if (this.check_form_validity()) {
            var form_info = self.get_form_info();
                self._rpc({
                route: '/submit/',
                params: form_info,
            }).then(function (data) {
                if (data['error']) {
                    $("form#vendor_action_form").parent().append("<div class='alert alert-danger alert-dismissable fade show'>" + data['error_msg'] + "</div>");
                } else {
                    document.location.href = originallink;
                }
            }); 
            
        }
    },

    // vendro_acceptance_changes: function(event) {
    //     var self = this;
    //     var originallink =  $("input[name='original_link']").val();
    //     var form_info = self.get_form_info();
    //     self._rpc({
    //         route: '/submit/',
    //         params: form_info,
    //     }).then(function (data) {
    //         if (data['error']) {
    //             $("form#vendor_action_form").parent().append("<div class='alert alert-danger alert-dismissable fade show'>" + data['error_msg'] + "</div>");
    //         } else {
    //             document.location.href = originallink;
    //         }
    //     });   
    // },
    // dispatch_status_changes: function(event) {
    //     var self = this;
    //     var originallink =  $("input[name='original_link']").val();
    //     var form_info = self.get_form_info();
    //     self._rpc({
    //         route: '/submit/',
    //         params: form_info,
    //     }).then(function (data) {
    //         if (data['error']) {
    //             $("form#vendor_action_form").parent().append("<div class='alert alert-danger alert-dismissable fade show'>" + data['error_msg'] + "</div>");
    //         } else {
    //             document.location.href = originallink;
    //         }
    //     });   
    // },

    // reject_reason: function(event) {
    //     var self = this;
    //     var originallink =  $("input[name='original_link']").val();
    //     var form_info = self.get_form_info();
    //     self._rpc({
    //         route: '/submit/',
    //         params: form_info,
    //     }).then(function (data) {
    //         if (data['error']) {
    //             $("form#vendor_action_form").parent().append("<div class='alert alert-danger alert-dismissable fade show'>" + data['error_msg'] + "</div>");
    //         } else {
    //             document.location.href = originallink;
    //         }
    //     });   
    // },


});
return publicWidget.registry.VendorPurchaseActions;
});
