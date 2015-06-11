GROUPS = new DiscussionGroups(STARTING_GROUPS, {mode: "client"});
USERS = new DiscussionUsers(STARTING_USERS, {mode: "client"});
COMMENTS = new Discussion(STARTING_COMMENTS, {mode: "client"});


function update(){
    GROUPS.fetch({update: true, success: function() {
        USERS.fetch({update: true, success: function() {
            COMMENTS.fetch({update: true, success: function() {
                refresh_groups();
            }});
        }});
    }})
}

setInterval(update, 5000);

var CACHED_SORTED_COMMENTS

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

        // Clear the cached sort

        React.render(
            <DiscussionComponent collection={COMMENTS} filter={group} sortBy={sortBy} />,
            document.getElementById("discussion")
        );
        $("body").scrollTo("#discussion", 0);
        $(document).foundation('reflow');
    }
});