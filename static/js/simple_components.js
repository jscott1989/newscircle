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

var DiscussionComponent = React.createClass({
    mixins: [BackboneMixin],

    route: function(sort) {
        var nav = "";

        if (sort !== "groups") {
            nav += "/" + sort
        }

        ROUTER.navigate(nav, {trigger: true});
    },

    sort_groups: function() {
        this.route("groups")
    },

    sort_votes: function() {
        this.route("votes")
    },

    sort_recent: function() {
        this.route("recent")
    },

    render : function() {
        var self = this;
        
        var comments = sortComments(this.props.collection, this.props.sortBy, this.props.filter, true);

        var commentNodes = comments.map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} sortBy={this.props.sortBy} route={this.route} />;
        }.bind(this));

        if (comments.length == 0) {
            commentNodes = <div className="alert-box">No posts to show in this view.</div>
        }

        return (
            <div>
                <div className="row">
                    <div className="small-12 columns">
                        <div className="row">
                            <div className="small-10 columns" id="comments-count">
                                {COMMENTS.length} comments
                            </div>
                            <div className="small-2 columns">
                                <a className={'order-votes simple-order-button' + (this.props.sortBy == 'votes' ? ' active' : '')} onClick={this.sort_votes} title="Order by votes"><img src="/static/img/like.png" /></a>
                                <a className={'order-recent simple-order-button' + (this.props.sortBy == 'recent' ? ' active' : '')} onClick={this.sort_recent} title="Order by most recent"><img src="/static/img/clock.png" /></a>
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
    render: function() {
        var replyNodes = sortComments(this.props.comment.get('replies').map(function(comment_id) { return COMMENTS.get(comment_id); }), this.props.sortBy).map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} sortBy={this.props.sortBy} route={this.props.route} />;
        }.bind(this));

        var like_count = this.props.comment.get('liked_by').length;
        var dislike_count = this.props.comment.get('disliked_by').length;

        var votes = like_count - dislike_count;

        return (
            <div className={"row post"}>
                <div className="small-12 columns">
                    <div className="row">
                        <div className="small-1 columns person">
                            <img src={this.props.author.get('avatar_url')} />
                        </div>
                        <div className="small-11 columns">
                            <strong title={this.props.author.get('username')}>{this.props.author.get('username')}</strong>
                            <div className="content">
                                <p>{this.props.comment.get('text')}</p>
                            </div>
                            <div className="info">
                                <Time time={this.props.comment.get('created_at')} />

                                <span>
                                    <i className="fi-like" />
                                    {votes}
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