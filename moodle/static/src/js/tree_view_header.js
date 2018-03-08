 odoo.define('moodle.tree_view_header', function(require){
    "use strict";

    var core = require('web.core');
    var ListView  = require('web.ListView');
    var Qweb = core.qweb;

    ListView.include({
        render_buttons: function($node){
            var self = this;
            this._super($node);
            this.$buttons.find('.o_refresh_category').click(self.proxy('refresh_category'));
            this.$buttons.find('.o_refresh_course').click(self.proxy('refresh_course'));
        },
        
        refresh_category: function(){
            var Model = require('web.Model');
            var custom_model = new Model('moodle.category');
            custom_model.call('print_something_for_test');

        },

        refresh_course: function(){
            var Model = require('web.Model');
            var custom_model = new Model('moodle.course');
            custom_model.call('get_courses');
        },
    });

});
