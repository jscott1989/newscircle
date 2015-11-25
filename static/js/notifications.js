/**
 * React for managing notifications
 */

 var Notification = Backbone.Model.extend({
    defaults : {
        created_time       : null,
        html               : null,
        read               : null
    },
});

 var Notifications = Backbone.Collection.extend({
    url: '/notifications',
    model: Notification,

    parse: function(d) {
        return d.results;
    }
});