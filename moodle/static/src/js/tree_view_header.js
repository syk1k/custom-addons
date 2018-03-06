odoo.define('moodle.tree_view_header', function(require){
    "use strict";

    var core = require('web.core');
    var ListView  = require('web.ListView');
    var Qweb = core.qweb;

    ListView.include({
        render_buttons: function($node){
            var self = this;
            self._super($node);
            self.$buttons.find('.print_something_for_test').click(self.proxy('tree_view_action'));
        },
        
        tree_view_action: function(){
            this.do_action({
                type: 'ir.actions.act_window',
                name: 'moodle',
                res_model: 'moodle.course',
                views: [[false, 'form']],
                target: 'current',
                view_type: 'tree',
                view_mode: 'tree',
                flags: {
                    'form': {
                        'action_buttons': true,
                        'options': {
                            'mode': 'edit'
                        }
                    }
                }
            });
            return {
                'type': 'ir.actions.client',
                'tag': 'reloads'
            }
        }
    });
});