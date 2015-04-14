var User = Backbone.Model.extend({
    defaults : {
        id       : null,
        username : null,
        avatar_url: null
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
    },

    group_liked_by: Backbone.Computed('liked_by', function() {
        var group = USERS.get(this.get("author")).get("group");
        return _.filter(this.get('liked_by'), function(id) {
            return USERS.get(id).get("group") == group;
        });
    }),

    group_disliked_by: Backbone.Computed('disliked_by', function() {
        var group = USERS.get(this.get("author")).get("group");
        return _.filter(this.get('disliked_by'), function(id) {
            return USERS.get(id).get("group") == group;
        })
    })
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

var DiscussionGroups = Backbone.Collection.extend({
    url: '/' + DISCUSSION_ID + '/groups/',
    model: User,

    parse: function(d) {
        return d.results;
    }
});