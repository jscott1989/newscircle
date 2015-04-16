var Router = Backbone.Router.extend({
    routes : {
        ""    : "index"
    },
    index : function() {
        GROUPS = new DiscussionGroups([], {mode: "client"});
        COMMENTS = new Discussion([], {mode: "client"});
        USERS = new DiscussionUsers([], {mode: "client"});
        GROUPS.fetch({success: function() {
            USERS.fetch({success: function() {
                COMMENTS.fetch();
            }});
        }});
        
        React.render(
            <DiscussionComponent collection={COMMENTS} />,
            document.getElementById("discussion")
        );
    },
});
 
new Router();
 
Backbone.history.start();