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
        "groups"               : "index_groups",
        "votes"                : "index_votes",
        "recent"               : "index_recent",
        "group/:group/:order"  : "group",
        "group/:group"         : "group",
        ""                     : "index"
    },
    index_groups: function() { return this.group(0, "groups")},
    index_votes: function() { return this.group(0, "votes")},
    index_recent: function() { return this.group(0, "recent")},
    index : function() {
        return this.group(0);
    },

    group: function(group, sortBy) {
        if (!sortBy) {
            sortBy = "groups";
        }

        $("body").scrollTo("#discussion", 0);
        React.render(
            <DiscussionComponent collection={COMMENTS} filter={group} sortBy={sortBy} />,
            document.getElementById("discussion")
        );
    }
});
 
var ROUTER = new Router();
 
Backbone.history.start({pushState: true, root: "/discussion/" + DISCUSSION_ID});