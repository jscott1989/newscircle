GROUPS = new DiscussionGroups([], {mode: "client"});
COMMENTS = new Discussion([], {mode: "client"});
USERS = new DiscussionUsers([], {mode: "client"});
GROUPS.fetch({success: function() {
    USERS.fetch({success: function() {
        COMMENTS.fetch();
    }});
}});

var Router = Backbone.Router.extend({
    routes : {
        "group/:group"      : "group",
        ""                  : "index"
    },
    index : function() {
        React.render(
            <DiscussionComponent collection={COMMENTS} />,
            document.getElementById("discussion")
        );
    },

    group: function(group) {
        React.render(
            <DiscussionComponent collection={COMMENTS} filter={group} />,
            document.getElementById("discussion")
        );
    }
});
 
var ROUTER = new Router();
 
Backbone.history.start({pushState: true, root: "/discussion/" + DISCUSSION_ID});