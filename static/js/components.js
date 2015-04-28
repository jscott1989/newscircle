/**
 * @jsx React.DOM
 */



function sortComments(comments, sortBy, filter, only_root) {
    if (!filter) {
        filter = '0';
    }

    function sortComments(comment) {
        if (sortBy == 'votes') {
            return comment.get('liked_by').length - comment.get('disliked_by').length;
        } else if (sortBy == 'groups') {
            // If we want to do groups, we first sort by in-group votes
            // then further down we split it by group
            return comment.get('group_liked_by').length - comment.get('group_disliked_by').length;
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
                    <img src={author.get('avatar_url')} />
                </div>
                <div className="small-8 columns representative_text">
                    <div><strong>{author.get('username')}</strong></div>
                    {representative_comment.get('text')}
                </div>
            </div>);
        }
        return (
            <div onClick={this.changeFilter} className={"group group_" + this.props.id + (this.props.active ? ' active' : '')}>
                {this.props.title}
                <div>{this.props.number_of_users} users {this.props.number_of_comments} posts ({this.props.number_of_root_comments} root)</div>
                {representative_comment}
            </div>
            );
    }
})

var DiscussionComponent = React.createClass({
    mixins: [BackboneMixin],

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

    render : function() {
        var self = this;

        var number_of_root_comments = COMMENTS.filter(function (c) { return !c.get('parent')}).length;
        
        var groupNodes = [<GroupButton title="All Posts" id="0" number_of_users={USERS.length} number_of_comments={COMMENTS.length} number_of_root_comments={number_of_root_comments} changeFilter={this.changeFilter} active={this.props.filter == 0} />].concat(GROUPS.map(function(group) {
            return <GroupButton title={"Group " + group.get('number')} active={self.props.filter == group.get('number')} number_of_users={group.get('users').length} number_of_comments={group.get('comments').length} number_of_root_comments={group.get('root_comments').length} id={group.get('number')} representative_comment={group.get('representative_comment')} changeFilter={self.changeFilter} />
        }));

        var comments = sortComments(this.props.collection, this.props.sortBy, this.props.filter, true);

        var commentNodes = comments.map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} sortBy={this.props.sortBy} route={this.route} />;
        }.bind(this));

        if (comments.length == 0) {
            commentNodes = <div className="alert-box">No posts to show in this view.</div>
        }



        var userNodes = USERS.filter(function(user) {
            if (self.props.filter == '0') {
                return true;
            }

            var group = GROUPS.get(user.get("group"));
            if (group) {
                group = group.get('number');
            }
            return group == self.props.filter;
        }).map(function(user) {
            return <div className="user"><img title={user.get('username')} src={user.get('avatar_url')} /></div>
        });


        var post_types = "all posts";
        if (self.props.filter !== 0) {
            post_types = 'all root posts by members of group ' + self.props.filter;
        }

        var sorted_by = self.props.sortBy;
        if (sorted_by == "recent") {
            sorted_by = "most recent";
        }

        return (
            <div>
                <div className="row">
                    <div className="small-12 columns">
                        <div className="row group-links">
                            {groupNodes}
                        </div>
                        <div className="row" id="introduction-row">
                            <div className="small-11 columns">
                                <p id="query-statement">Showing {post_types} sorted by {sorted_by}</p>

                                <div className="users">
                                    {userNodes}
                                </div>
                            </div>
                            <div className="small-1 columns">
                                <a className={'order-groups order-button' + (this.props.sortBy == 'groups' ? ' active' : '')} onClick={this.sort_groups} title="Order by groups"><img src="/static/img/group.png" /></a>
                                <a className={'order-votes order-button' + (this.props.sortBy == 'votes' ? ' active' : '')} onClick={this.sort_votes} title="Order by votes"><img src="/static/img/like.png" /></a>
                                <a className={'order-recent order-button' + (this.props.sortBy == 'recent' ? ' active' : '')} onClick={this.sort_recent} title="Order by most recent"><img src="/static/img/clock.png" /></a>
                            </div>
                        </div>
                        {commentNodes}
                        <ReplyComponent />
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

    render: function() {
        var replyNodes = sortComments(this.props.comment.get('replies').map(function(comment_id) { return COMMENTS.get(comment_id); }), this.props.sortBy).map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} sortBy={this.props.sortBy} route={this.props.route} />;
        }.bind(this));

        var group_number = 0;
        var group_name = '';
        if (this.props.author.get('group')) {
            group_number = GROUPS.get(this.props.author.get('group')).get('number');
            group_name = 'Group ' + group_number;
        }

        var group_like_count = this.props.comment.get('group_liked_by').length;
        var like_count = this.props.comment.get('liked_by').length;

        var group_dislike_count = this.props.comment.get('group_disliked_by').length;
        var dislike_count = this.props.comment.get('disliked_by').length;

        return (
            <div className={"row post group_" + group_number}>
                <div className="small-12 columns">
                    <div className="row">
                        <div className="small-2 columns person">
                            <img src={this.props.author.get('avatar_url')} />
                        </div>
                        <div className="small-10 columns">
                            <div className="author-info">
                                <strong>{this.props.author.get('username')}</strong>
                                <div onClick={this.viewGroup} className="group_name">{group_name}</div>
                            </div>
                            <div className="content">
                                <p>{this.props.comment.get('text')}</p>
                            </div>
                            <div className="info">
                                <Time time={this.props.comment.get('created_at')} />

                                <span title={this.props.author.get('group') ? group_like_count + ' likes from ' + group_name + ' of ' + like_count + ' total likes' : like_count + ' likes'}>
                                    <i className="fi-like" />
                                    {this.props.author.get('group') ? group_like_count + '/' : null}{like_count}
                                </span>
                                <span title={this.props.author.get('group') ? group_dislike_count + ' dislikes from ' + group_name + ' of ' + dislike_count + ' total dislikes' : dislike_count + ' dislikes'}>
                                    <i className="fi-dislike" />
                                    {this.props.author.get('group') ? group_dislike_count + '/' : null}{dislike_count}
                                </span>
                            </div>
                            <div className="replies">
                                {replyNodes}
                            </div>
                            <ReplyComponent parent={this.props.comment.get('id')} />
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});


var ReplyComponent = React.createClass({
    render: function() {
        if (DISCUSSION_LOCKED || !USER_AUTHENTICATED) {
            return <div></div>;
        }
        var csrftoken = $.cookie('csrftoken');
        return (
                <div className="reply">
                    <form method="POST" action={"/discussion/" + DISCUSSION_ID + "/reply"}>
                        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
                        <input type="hidden" name="parent" value={this.props.parent} />
                        <textarea name="text" />
                        <button type="submit">Reply</button>
                    </form>
                </div>
        );
    }
});



var Time = React.createClass({
  componentDidMount: function() {
    var self = this;
    this.interval = setInterval(function() {self.setState({});}, 1000);
  },
  componentWillUnmount: function() {
    clearInterval(this.interval);
  },

  render: function() {
    var m = moment(this.props.time, "YYYY-MM-DDTHH:mm:ss.S");
    var formatted_time = m.fromNow();
    var simple_time = m.format('MMMM Do YYYY, h:mm a');
    return (
      <div title={simple_time}>{formatted_time}</div>
    );
  }
});