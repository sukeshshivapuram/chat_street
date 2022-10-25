odoo.define('odoov13_6.ClientAction', function (require) {
"use strict";

var ClientactionNew = require('stock_barcode.ClientAction'); 
var concurrency = require('web.concurrency');
var core = require('web.core');
var utils = require('web.utils');


var _t = core._t;


ClientactionNew.include({

	_incrementLines: function (params) {
        var line = this._findCandidateLineToIncrement(params);
        // console.log(params,'fgfdhgfdhhfdhdhhhh');
        var isNewLine = false;
        if (line) {
            // Update the line with the processed quantity.
            if (params.product.tracking === 'none' ||
                params.lot_id ||
                params.lot_name
                ) {
                if (this.actionParams.model === 'stock.picking') {
                    line.qty_done += params.product.qty || 1;
                } else if (this.actionParams.model === 'stock.inventory') {
                    line.product_qty += params.product.qty || 1;
                }
            }
        } else {
            isNewLine = true;
            // Create a line with the processed quantity.
            if (params.product.tracking === 'none' ||
                params.lot_id ||
                params.lot_name
                ) {
                
                line = this._makeNewLine(params.product, params.barcode, params.product.qty || params.qty_done || 1, params.package_id, params.result_package_id);
                // console.log(line,'if');
            } else {
                line = this._makeNewLine(params.product, params.barcode, 0, params.package_id, params.result_package_id);
                // console.log(line,'else');
            }
            this._getLines(this.currentState).push(line);
            this.pages[this.currentPageIndex].lines.push(line);
        }
        if (this.actionParams.model === 'stock.picking') {
            if (params.lot_id) {
                line.lot_id = [params.lot_id];
            }
            if (params.lot_name) {
                line.lot_name = params.lot_name;
            }
        } else if (this.actionParams.model === 'stock.inventory') {
            if (params.lot_id) {
                line.prod_lot_id = [params.lot_id, params.lot_name];
            }
        }
        // console.log(line);
        return {
            'id': line.id,
            'virtualId': line.virtual_id,
            'lineDescription': line,
            'isNewLine': isNewLine,
        };
    },


    _step_lot: function (barcode, linesActions) {
        if (! this.groups.group_production_lot) {
            return Promise.reject();
        }
        this.currentStep = 'lot';
        var errorMessage;
        var self = this;

        // Bypass this step if needed.
        if (this.productsByBarcode[barcode]) {
            return this._step_product(barcode, linesActions);
        } else if (this.locationsByBarcode[barcode]) {
            return this._step_destination(barcode, linesActions);
        }

        var getProductFromLastScannedLine = function () {
            if (self.scannedLines.length) {
                var idOrVirtualId = self.scannedLines[self.scannedLines.length - 1];
                var line = _.find(self._getLines(self.currentState), function (line) {
                    return line.virtual_id === idOrVirtualId || line.id === idOrVirtualId;
                });
                if (line) {
                    var product = self.productsByBarcode[line.product_barcode];
                    // Product was added by lot or package
                    if (!product) {
                        return false;
                    }
                    product.barcode = line.product_barcode;
                    // console.log(product);
                    return product;
                }
            }
            return false;
        };

        var getProductFromCurrentPage = function () {
            return _.map(self.pages[self.currentPageIndex].lines, function (line) {
                return line.product_id.id;
            });
        };

        var getProductFromOperation = function () {
            return _.map(self._getLines(self.currentState), function (line) {
                return line.product_id.id;
            });
        };

        var readProduct = function (product_id) {
            var product_barcode = _.findKey(self.productsByBarcode, function (product) {
                return product.id === product_id;
            });

            if (product_barcode) {
                var product = self.productsByBarcode[product_barcode];
                product.barcode = product_barcode;
                return Promise.resolve(product);
            } else {
                return self._rpc({
                    model: 'product.product',
                    method: 'read',
                    args: [product_id],
                }).then(function (product) {
                    return Promise.resolve(product[0]);
                });
            }
        };

        var getLotInfo = function (lots) {
            var products_in_lots = _.map(lots, function (lot) {
                return lot.product_id[0];
            });
            var products = getProductFromLastScannedLine();
            var product_id = _.intersection(products, products_in_lots);
            if (! product_id.length) {
                products = getProductFromCurrentPage();
                product_id = _.intersection(products, products_in_lots);
            }
            if (! product_id.length) {
                products = getProductFromOperation();
                product_id = _.intersection(products, products_in_lots);
            }
            if (! product_id.length) {
                product_id = [lots[0].product_id[0]];
            }
            return readProduct(product_id[0]).then(function (product) {
                var lot = _.find(lots, function (lot) {
                    return lot.product_id[0] === product.id;
                });
                // console.log(lot,'jdifgibiogbuibsgubuisbugbuiosfuiobg');
                return Promise.resolve({lot_id: lot.id, lot_name: lot.display_name, product: product, prodtuct_qty_lot:lot.product_qty});
            });
        };

        var searchRead = function (barcode) {
            // Check before if it exists reservation with the lot.
            var line_with_lot = _.find(self.currentState.move_line_ids, function (line) {
                return (line.lot_id && line.lot_id[1] === barcode) || line.lot_name === barcode;
            });
            var def;
            if (line_with_lot) {
                def = Promise.resolve([{
                    name: barcode,
                    display_name: barcode,
                    id: line_with_lot.lot_id[0],
                    product_id: [line_with_lot.product_id.id, line_with_lot.display_name],
                }]);
            } else {
                def = self._rpc({
                    model: 'stock.production.lot',
                    method: 'search_read',
                    domain: [['name', '=', barcode]],
                });
            }
            return def.then(function (res) {
                if (! res.length) {
                    errorMessage = _t('The scanned lot does not match an existing one.');
                    return Promise.reject(errorMessage);
                }
                return getLotInfo(res);
            });
        };

        var create = function (barcode, product) {
            return self._rpc({
                model: 'stock.production.lot',
                method: 'create',
                args: [{
                    'name': barcode,
                    'product_id': product.id,
                    'company_id': self.currentState.company_id[0],
                }],
            });
        };

        var def;
        if (this.currentState.use_create_lots &&
            ! this.currentState.use_existing_lots) {
            // Do not create lot if product is not set. It could happens by a
            // direct lot scan from product or source location step.
            var product = getProductFromLastScannedLine();
            if (! product  || product.tracking === "none") {
                return Promise.reject();
            }
            def = Promise.resolve({lot_name: barcode, product: product});
        } else if (! this.currentState.use_create_lots &&
                    this.currentState.use_existing_lots) {
            def = searchRead(barcode);
        } else {
            def = searchRead(barcode).then(function (res) {
                return Promise.resolve(res);
            }, function (errorMessage) {
                var product = getProductFromLastScannedLine();
                if (product && product.tracking !== "none") {
                    return create(barcode, product).then(function (lot_id) {
                        return Promise.resolve({lot_id: lot_id, lot_name: barcode, product: product});
                    });
                }
                return Promise.reject(errorMessage);
            });
        }
        return def.then(function (lot_info) {
        	var pdt_qty;
        	if(self.currentState.putaway){
        		pdt_qty =lot_info.prodtuct_qty_lot;
        	}
        	// console.log(lot_info.product.stock_quant_ids[12],'ghduifbgbdui  vfvdyi  vfvadyivf');
         //    console.log(lot_info);
            var product = lot_info.product;
            if (product.tracking === 'serial' && self._lot_name_used(product, barcode)){
                errorMessage = _t('The scanned serial number is already used.');
                return Promise.reject(errorMessage);
            }

            var res = self._incrementLines({
                'product': product,
                'barcode': lot_info.product.barcode,
                'lot_id': lot_info.lot_id,
                'lot_name': lot_info.lot_name,
                'qty_done': pdt_qty,
            });
            // console.log(res);
            if (res.isNewLine) {
                self.scannedLines.push(res.lineDescription.virtual_id);
                 // console.log('addproduct4',res.lineDescription);
                linesActions.push([self.linesWidget.addProduct, [res.lineDescription, self.actionParams.model]]);
            } else {
                if (self.scannedLines.indexOf(res.lineDescription.id) === -1) {
                    self.scannedLines.push(res.lineDescription.id);
                }
                linesActions.push([self.linesWidget.incrementProduct, [res.id || res.virtualId, 1, self.actionParams.model]]);
                linesActions.push([self.linesWidget.setLotName, [res.id || res.virtualId, barcode]]);
            }
            return Promise.resolve({linesActions: linesActions});
        });
    },




});



});