var Router = Backbone.Router.extend({
    routes : {
        ""    : "index"
    },
    index : function() {
        COMMENTS = new Discussion([], {mode: "client"});
        USERS = new DiscussionUsers([], {mode: "client"});
        GROUPS = new DiscussionGroups([], {mode: "client"});
        COMMENTS.fetch();
        USERS.fetch();
        GROUPS.fetch();
        
        React.render(
            <DiscussionComponent collection={COMMENTS} />,
            document.getElementById("discussion")
        );
    },
});
 
new Router();
 
Backbone.history.start();