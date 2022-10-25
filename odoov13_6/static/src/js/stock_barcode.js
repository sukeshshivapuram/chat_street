odoo.define('odoov13_6.MainMenu', function (require) {
"use strict";

var MainMenuNew = require('stock_barcode.MainMenu').MainMenu;
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var Session = require('web.session');
var _t = core._t;

MainMenuNew.include({
	
	events: {
		    "click .button_operations": function(){
            this.do_action('stock_barcode.stock_picking_type_action_kanban');
	        },
	        "click .button_inventory": function(){
	            this.open_inventory();
	        },
	        "click .o_stock_barcode_menu": function(){
	            this.trigger_up('toggle_fullscreen');
	            this.trigger_up('show_home_menu');
	        },
	         "click .button_putaway": function(){
	            this.create_putaway();
	        },
	    },
	    create_putaway: function(){

	        var self = this;
	        return Session.rpc('/stock_barcode/scan_from_main_menu1', {
	                
	            }).then(function(result) {
	            if (result.action) {
	                self.do_action(result.action);
	            } else if (result.warning) {
	                self.do_warn(result.warning);
	            }
	        });


	    },

	});


});