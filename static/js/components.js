/**
 * @jsx React.DOM
 */



function sortComments(comments, sortBy, filter, only_root) {
    if (!filter) {
        filter = '0';
    }

    comments = comments.filter(function(c) { return c });

    function sortComments(comment) {
        if (sortBy == 'votes') {
            return comment.get('liked_by').length - comment.get('disliked_by').length;
        } else if (sortBy == 'groups') {
            // If we want to do groups, we first sort by in-group votes
            // then further down we split it by group
            return comment.group_liked_by().length - comment.group_disliked_by().length;
        } else {
            return moment(comment.get('created_at'), "YYYY-MM-DDTHH:mm:ss.S")
        }
    }

    if (comments.sortBy) {
        comments = comments.sortBy(sortComments);
    } else {
        comments = _.sortBy(comments, sortComments);
    }


    comments = comments.filter(function(comment) {
        if (only_root && comment.get('parent') !== null) {
            return false;
        }
        if (filter == '0') {
            return true;
        } else if (filter == '-1') {
            return USERS.get(comment.get("author")).get("group") == null;
        }

        var group = GROUPS.get(USERS.get(comment.get("author")).get("group"));
        if (group) {
            group = group.get('number');
        }
        return group == filter;
    }).reverse();


    if (sortBy == 'groups') {
        // We need to split the posts by groups now
        var groups = _.groupBy(comments, function(comment) {
            return USERS.get(comment.get("author")).get("group");
        });

        // Order the groups by number of members
        var keys = GROUPS.map(function(group) { return group.get('id') });
        keys.push("null");

        // Ensure we only show groups which exist
        keys = _.filter(keys, function(group_id) {
            return group_id in groups;
        });

        // Now loop through the keys in order, taking one from each until they are all exhausted
        var hasAdded = true;
        var comments = [];
        while (hasAdded) {
            hasAdded = false;
            _.each(keys, function(group_id) {
                if (groups[group_id].length > 0) {
                    hasAdded = true;
                    comments.push(groups[group_id].shift());
                }
            });
        }
    }

    return comments;
}

var GroupButtons = React.createClass({
    changeFilter: function(filter) {
        this.props.changeFilter(filter);
    },

    render: function() {
        var self = this;

        //TODO: If there are no comments at all, hide.

        // if (number_of_ungrouped_users == USERS.length) {
        //     groupNodes = '';
        // } else if (number_of_ungrouped_users == 0 && GROUPS.length < 2) {
        //     groupNodes = '';
        // }

        var number_of_root_comments = COMMENTS.filter(function (c) { return !c.get('parent')}).length;

        var number_of_ungrouped_comments = COMMENTS.length - _.reduce(GROUPS.map(function(group) {
            return group.get('comments').length;
        }), function(m, x) {return m + x;}, 0);

        var number_of_ungrouped_users = USERS.length - _.reduce(GROUPS.map(function(group) {
            return group.get('users').length;
        }), function(m, x) {return m + x;}, 0);

        var number_of_ungrouped_root_comments = number_of_root_comments - _.reduce(GROUPS.map(function(group) {
            return group.get('root_comments').length;
        }), function(m, x) {return m + x;}, 0);
        

        var groupNodes = [<GroupButton title="All Posts" id="0" number_of_users={USERS.length} number_of_comments={COMMENTS.length} number_of_root_comments={number_of_root_comments} changeFilter={this.changeFilter} active={this.props.filter == 0} />].concat(GROUPS.map(function(group) {
            return <GroupButton title={"Group " + group.get('number')} active={self.props.filter == group.get('number')} number_of_users={group.get('users').length} number_of_comments={group.get('comments').length} number_of_root_comments={group.get('root_comments').length} id={group.get('number')} representative_comment={group.get('representative_comment')} changeFilter={self.changeFilter} />
        }));


        if (number_of_ungrouped_users > 0) {
            groupNodes = groupNodes.concat([<GroupButton title="Other" id="-1" number_of_users={number_of_ungrouped_users} number_of_comments={number_of_ungrouped_comments} number_of_root_comments={number_of_ungrouped_root_comments} changeFilter={this.changeFilter} active={this.props.filter == -1} />]);
        }


        window.refresh_groups = function() {
            self.setState({});
        };
        return <div>{groupNodes}</div>;
    }
})


var GroupButton = React.createClass({
    changeFilter: function() {
        this.props.changeFilter(this.props.id);
    },

    render: function() {
        var representative_comment = null;
        if (this.props.representative_comment) {
            representative_comment = COMMENTS.get(this.props.representative_comment);
        }

        if (representative_comment) {
            var author = USERS.get(representative_comment.get('author'));
            representative_comment = (<div className="representative_comment row">
                <div className="small-4 columns person">
                    <img src="https://disqus.com/api/users/avatars/nhslck.jpg" />
                </div>
                <div className="small-8 columns representative_text">
                    <div><strong>{author.get('username')}</strong></div>
                    {representative_comment.get('text')}
                </div>
            </div>);
        } else {
            representative_comment = (<div className="representative_comment row">
                <div className="small-4 columns person">
                    <img src="https://disqus.com/api/users/avatars/nhslck.jpg" />
                </div>
                <div className="small-8 columns representative_text">
                </div>
            </div>);
        }
        return (
            <div className="small-4 columns">
                <div onClick={this.changeFilter} className={"group group_" + this.props.id + (this.props.active ? ' active' : '')}>
                    {this.props.title}
                    <div>{this.props.number_of_users} users {this.props.number_of_root_comments} root posts ({this.props.number_of_comments} total posts)</div>
                    {representative_comment}
                </div>
            </div>
            );
    }
})

var DiscussionComponent = React.createClass({

    route: function(filter, sort) {
        var nav = "";
        if (filter != 0) {
            nav = "group/" + filter;
        }

        if (sort !== "groups") {
            nav += "/" + sort
        }

        ROUTER.navigate(nav, {trigger: true});
    },

    changeFilter: function(filter) {
        this.route(filter, this.props.sortBy)
    },

    sort_groups: function() {
        this.route(this.props.filter, "groups")
    },

    sort_votes: function() {
        this.route(this.props.filter, "votes")
    },

    sort_recent: function() {
        this.route(this.props.filter, "recent")
    },

    refresh: function() {
        this.setState({});
    },

    render : function() {
        var self = this;

        var number_of_root_comments = COMMENTS.filter(function (c) { return !c.get('parent')}).length;

        var number_of_ungrouped_users = USERS.length - _.reduce(GROUPS.map(function(group) {
            return group.get('users').length;
        }), function(m, x) {return m + x;}, 0);

        groupNodes = <GroupButtons filter={this.props.filter} changeFilter={this.changeFilter} />

        var comments = sortComments(this.props.collection, this.props.sortBy, this.props.filter, true);

        var commentNodes = comments.map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} sortBy={this.props.sortBy} route={this.route} />;
        }.bind(this));

        if (comments.length == 0) {
            commentNodes = <div className="alert-box">No root posts to show for this group.</div>
        }

        if (self.props.filter === 0) {
            // No need to show all users
            userNodes = '';
        } else {
            var userNodes = USERS.filter(function(user) {
                if (self.props.filter == '0') {
                    return true;
                } else if (self.props.filter == '-1') {
                    return user.get("group") == null;
                }

                var group = GROUPS.get(user.get("group"));
                if (group) {
                    group = group.get('number');
                }
                return group == self.props.filter;
            });

            var total_filtered_users = userNodes.length;

            userNodes = <div></div>

            if (total_filtered_users > userNodes.length) {
                userNodes = userNodes.concat([<div>and {total_filtered_users - userNodes.length} more users.</div>]);
            }
        }


        var post_types = "all posts";
        if (self.props.filter == -1) {
            post_types = 'all root posts by ungrouped members';
        }
        else if (self.props.filter !== 0) {
            post_types = 'all root posts by members of group ' + self.props.filter;
        }

        var sorted_by = self.props.sortBy;
        if (sorted_by == "recent") {
            sorted_by = "most recent";
        }

        if (sorted_by == 'groups') {
            if (self.props.filter == -1) {
                // On other we don't have "group votes"
                sorted_by = 'votes';
            } else if (self.props.filter > 0) {
                // Within a group we can only order by in-group votes
                sorted_by = 'group votes';
            }
        }

        if (this.props.collection.length == 0) {
            // If there are no posts at all we need to hide some things
            introductionRow = '';
            commentNodes = '';
        } else {
            introductionRow = (<div className="row" id="introduction-row">
                <div className="small-11 columns">
                    <p id="query-statement">Showing {post_types} sorted by {sorted_by}</p>

                    <NewPostsComponent refresh={self.refresh} comment_count={COMMENTS.length}/>

                    <div className="users">
                        {userNodes}
                    </div>
                </div>
                <div className="small-1 columns">
                    <a className={'order-groups order-button' + (this.props.sortBy == 'groups' ? ' active' : '')} onClick={this.sort_groups} title="Order by groups"><img src="/static/img/group.png" /></a>
                    <a className={'order-votes order-button' + (this.props.sortBy == 'votes' ? ' active' : '')} onClick={this.sort_votes} title="Order by votes"><img src="/static/img/like.png" /></a>
                    <a className={'order-recent order-button' + (this.props.sortBy == 'recent' ? ' active' : '')} onClick={this.sort_recent} title="Order by most recent"><img src="/static/img/clock.png" /></a>
                </div>
            </div>)
        }

        return (
            <div>
                <div className="row">
                    <div className="small-12 columns">
                        <div className="row group-links">
                            {groupNodes}
                        </div>
                        {introductionRow}
                        <ReplyComponent />
                        {commentNodes}
                    </div>
                </div>
            </div>
        );
    }
});


var CommentComponent = React.createClass({
    viewGroup: function() {
        if (this.props.author.get('group')) {
            this.props.route(GROUPS.get(this.props.author.get('group')).get('number'), "groups");
        }
    },

    toggleReply: function() {
        this.setState({"showReply": !this.state.showReply})
    },

    getInitialState: function() {
        return {showReply: false};
    },

    like: function() {
        if (CURRENT_USER_ID > 0) {
            $.post("/comments/" + this.props.comment.get("id") + "/like");
            var index = this.props.comment.get('liked_by').indexOf(CURRENT_USER_ID);
            if (index > -1) {
                this.props.comment.get('liked_by').splice(index, 1);
            }
            index = this.props.comment.get('disliked_by').indexOf(CURRENT_USER_ID);
            if (index > -1) {
                this.props.comment.get('disliked_by').splice(index, 1);
            }
            this.props.comment.get('liked_by').push(CURRENT_USER_ID);
            this.setState({});
        }
    },

    dislike: function() {
        if (CURRENT_USER_ID > 0) {
            $.post("/comments/" + this.props.comment.get("id") + "/dislike");
            var index = this.props.comment.get('liked_by').indexOf(CURRENT_USER_ID);
            if (index > -1) {
                this.props.comment.get('liked_by').splice(index, 1);
            }
            index = this.props.comment.get('disliked_by').indexOf(CURRENT_USER_ID);
            if (index > -1) {
                this.props.comment.get('disliked_by').splice(index, 1);
            }
            this.props.comment.get('disliked_by').push(CURRENT_USER_ID);
            this.setState({});
        }
    },

    render: function() {
        var replyNodes = sortComments(this.props.comment.get('replies').map(function(comment_id) { return COMMENTS.get(comment_id); }), this.props.sortBy).map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} sortBy={this.props.sortBy} route={this.props.route} />;
        }.bind(this));

        var group_number = 0;
        var group_name = '';
        if (this.props.author.get('group')) {
            group_number = GROUPS.get(this.props.author.get('group')).get('number');
            group_name = 'Group ' + group_number;
        } else {
            group_name = 'No Group'
        }

        var group_like_count = this.props.comment.group_liked_by().length;
        var like_count = this.props.comment.get('liked_by').length;

        var group_dislike_count = this.props.comment.group_disliked_by().length;
        var dislike_count = this.props.comment.get('disliked_by').length;

        // Do I like this?
        var current_position = 0;
        if (this.props.comment.get('liked_by').indexOf(CURRENT_USER_ID) > -1) {
            current_position = 1;
        } else if (this.props.comment.get('disliked_by').indexOf(CURRENT_USER_ID) > -1) {
            current_position = -1;
        }

        // <div className="small-2 columns person">
        //     <img src={this.props.author.get('avatar_url')} />
        // </div>

        var replyContent = '';
        if (this.state.showReply) {
            replyContent = <ReplyComponent toggleReply={this.toggleReply} parent={this.props.comment.get('id')} />;
        }


        var replyToggle = '';
        if (!DISCUSSION_LOCKED && USER_AUTHENTICATED) {
            replyToggle = <a onClick={this.toggleReply} className="reply">reply</a>;
        }

        return (
            <div className={"row post group_" + group_number}>
                <div className="small-12 columns">
                    <div className="row">
                        <div className="small-1 columns votes">
                            <span title={this.props.author.get('group') ? group_like_count + ' likes from ' + group_name + ' of ' + like_count + ' total likes' : like_count + ' likes'}>
                                <i onClick={this.like} className={current_position == 1 ? "fi-like active" : "fi-like"} />
                                {this.props.author.get('group') ? group_like_count + '/' : null}{like_count}
                            </span>
                            <span title={this.props.author.get('group') ? group_dislike_count + ' dislikes from ' + group_name + ' of ' + dislike_count + ' total dislikes' : dislike_count + ' dislikes'}>
                                <i onClick={this.dislike} className={current_position == -1 ? "fi-dislike active" : "fi-dislike"} />
                                {this.props.author.get('group') ? group_dislike_count + '/' : null}{dislike_count}
                            </span>
                        </div>
                        <div className="small-11 columns">
                            <div className="author-info">
                                <strong><a href={"/user/" + this.props.author.get('user_pk')}>{this.props.author.get('username')}</a></strong>
                                <div onClick={this.viewGroup} className={"group_name" + (this.props.author.get('group') ? '' : ' no-group')}>{group_name}</div>
                                <Time time={this.props.comment.get('created_at')} />
                            </div>
                            <div className="content" dangerouslySetInnerHTML={{__html: this.props.comment.get('html')}}>
                            </div>
                            <div className="info">
                                <Time time={this.props.comment.get('created_at')} />
                                {replyToggle}
                            </div>
                            {replyContent}
                            <div className="replies">
                                {replyNodes}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

var NewPostsComponent = React.createClass({

    getInitialState: function() {
        return {"new_comments": 0};
    },

    refreshView: function() {
        this.props.refresh();
        this.setState({"new_comments": 0});
    },

    render: function() {
        var self = this;
        window.check_for_new_posts = function() {
            var new_state = COMMENTS.length - self.props.comment_count;
            if (new_state > self.state.new_comments) {
                self.setState({"new_comments": new_state});
            }
        }

        window.refreshView = self.refreshView;

        if (self.state.new_comments > 0) {
            var new_posts_text = self.state.new_comments + " new comments"
            if (self.state.new_comments == 1) {
                new_posts_text = "1 new comment";
            }
            return <div onClick={self.refreshView} className="new-posts">There has been {new_posts_text} since you started reading. Click to show.</div>
        } else {
            return <div></div>
        }
    }
})


var ReplyComponent = React.createClass({
    getInitialState: function() {
        return {text: ''};
    },
    handleTextChange: function(e) {
        this.setState({text: e.target.value});
    },
    render: function() {
        if (DISCUSSION_LOCKED || !USER_AUTHENTICATED) {
            return <div></div>;
        }
        return (
                <div className="reply">
                    <form>
                        <textarea name="text" value={this.state.text} onChange={this.handleTextChange} />
                        <button type="submit" onClick={this.submitReply}>Reply</button>
                    </form>
                </div>
        );
    },

    submitReply: function() {
        var self = this;
        if (this.props.toggleReply) {
            this.props.toggleReply();
        }
        $.post('/discussion/' + DISCUSSION_ID + '/reply', {"text": this.state.text, "parent": this.props.parent}, function() {
            self.setState({text: ""});
            update(true);
        })
        return false;
    }
});
