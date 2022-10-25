odoo.define('odoov13_6.picking_client_action', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var PickingClientActionNew = require('stock_barcode.picking_client_action');
var ClientAction = require('stock_barcode.ClientAction');
var ViewsWidget = require('stock_barcode.ViewsWidget');
var rpc = require('web.rpc');
var _t = core._t;

PickingClientActionNew.include({

	_makeNewLine: function (product, barcode, qty_done, package_id, result_package_id) {
        var self = this;
        var virtualId = this._getNewVirtualId();
        var currentPage = this.pages[this.currentPageIndex];
        
        var suggested_bin_loc;        
        
        var newLine = {
            'picking_id': this.currentState.id,
            'product_id': {
                'id': product.id,
                'display_name': product.display_name,
                'barcode': barcode,
                'tracking': product.tracking,
            },
            'product_barcode': barcode,
            'display_name': product.display_name,
            'product_uom_qty': 0,
            'product_uom_id': product.uom_id,
            'qty_done': qty_done,
            'location_id': {
                'id': currentPage.location_id,
                'display_name': currentPage.location_name,
            },
            'location_dest_id': {
                'id': currentPage.location_dest_id,
                'display_name': currentPage.location_dest_name,
            },
            'package_id': package_id,
            'result_package_id': result_package_id,
            'state': 'assigned',
            'reference': this.name,
            'virtual_id': virtualId,
            'putaway' : this.currentState.putaway,
           
        };


       ajax.jsonRpc("/get_suggested_bin", 'call', {

                           'productid' : product.id,

                     }).then(function (ress) {
                        //                         .push({
                        //     key:   "keyName",
                        //     value: "the value"
                        // });
                         // suggested_bin_loc = ress;

                         //    newLine['suggested_bin_loc'] =ress;  
                           $("#sugg_id").html(ress); 

                    });

       // this._rpc({
       //          'model': 'stock.move.line',
       //          'method': 'get_suggested_bin',
       //          'args': [[],product.id],
       //      }).then(function(ress) { 
       //            newLine['suggested_bin_loc'] = ress;
       //             // return newLine;

       //  });
            // console.log(this.suggested_bin_loc); // i can see the value here 
     
        return  newLine;
    },



});




});