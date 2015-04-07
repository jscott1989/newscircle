var User = Backbone.Model.extend({
    defaults : {
        id       : null,
        username : null
    }
});

var Group = Backbone.Model.extend({
    defaults : {
        name   : null,
        colour : null
    }
});

var Comment = Backbone.Model.extend({
    defaults : {
        text        : null,
        parent      : null,
        author      : null,
        liked_by    : null,
        disliked_by : null,
        replies     : null
        
    }
});

var DiscussionUsers = Backbone.Collection.extend({
    url: '/' + DISCUSSION_ID + '/users/',
    model: User,

    parse: function(d) {
        return d.results;
    }
});

var Discussion = Backbone.Collection.extend({
    url: '/' + DISCUSSION_ID + '/comments/',
    model: Comment,

    parse: function(d) {
        return d.results;
    }
});