// This just ensures we don't re-render for each comment added
COMMENTS_FETCHED = false;
default_group = null;
default_sortBy = null;

GROUPS = new DiscussionGroups([], {mode: "client"});
COMMENTS = new Discussion([], {mode: "client"});
USERS = new DiscussionUsers([], {mode: "client"});
GROUPS.fetch({success: function() {
    USERS.fetch({success: function() {
        COMMENTS.fetch({success: function() {
            COMMENTS_FETCHED = true;
            React.render(
                <DiscussionComponent collection={COMMENTS} filter={default_group} sortBy={default_sortBy} />,
                document.getElementById("discussion")
            );
            $("body").scrollTo("#discussion", 0);
        }});
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

        if (COMMENTS_FETCHED) {
            React.render(
                <DiscussionComponent collection={COMMENTS} filter={group} sortBy={sortBy} />,
                document.getElementById("discussion")
            );
            $("body").scrollTo("#discussion", 0);
        } else {
            default_group = group;
            default_sortBy = sortBy;
        }
        
    }
});