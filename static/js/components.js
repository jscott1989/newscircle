/**
 * @jsx React.DOM
 */


var GroupButton = React.createClass({
    changeFilter: function() {
        this.props.changeFilter(this.props.id);
    },

    render: function() {
        return <div onClick={this.changeFilter} className={"group group_" + this.props.id}>{this.props.title}</div>;
    }
})

var DiscussionComponent = React.createClass({
    mixins: [BackboneMixin],

    changeFilter: function(f) {
        this.setState({filter: f});
    },

    getInitialState: function() {
        return {filter: "0", sortBy: "groups"};
    },

    resort: function() {
        this.setState({sortBy: React.findDOMNode(this.refs.sort).value})
    },

    render : function() {
        var self = this;
        
        var groupNodes = [<GroupButton title="All Posts" id="0" changeFilter={this.changeFilter} />].concat(GROUPS.sortBy(function(group) {
            // TODO: How do we sort groups? probably by size?
        }).map(function(group) {
            return <GroupButton title={"Group " + group.get('number')} id={group.get('number')} changeFilter={self.changeFilter} />
        }));

        var commentNodes = this.props.collection.sortBy(function(comment) {
            if (self.state.sortBy == 'votes') {
                return comment.get('liked_by').length - comment.get('disliked_by').length;
            } else if (self.state.sortBy == 'groups') {
                // TODO - this probably needs something more complex than sortBy
            } else {
                return moment(comment.get('created_at'), "YYYY-MM-DDTHH:mm:ss.S")
            }
        }).filter(function(comment) {
            if (comment.get('parent') !== null) {
                return false;
            }
            if (self.state.filter == '0') {
                return true;
            }

            var group = GROUPS.get(USERS.get(comment.get("author")).get("group"));
            if (group) {
                group = group.get('number');
            }
            return group == self.state.filter;
        }).reverse().map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} />;
        }.bind(this));

        return (
            <div>
                <div className="row">
                    <div className="small-1 columns group-links">
                        {groupNodes}
                    </div>
                    <div className="small-11 columns">
                        <div>
                            Sort
                            <select onChange={this.resort} ref="sort">
                                <option value="groups">groups</option>
                                <option value="votes">most popular</option>
                                <option value="chronology">most recent</option>
                            </select>
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
        var replyNodes = this.props.comment.get('replies').map(function (comment_id) {
            var comment = COMMENTS.get(comment_id);
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} />;
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
                            <strong>{this.props.author.get('username')}</strong>
                            <div>{group_name}</div>
                        </div>
                        <div className="small-10 columns">
                            <div className="content">
                                <p>{this.props.comment.get('text')}</p>
                            </div>
                            <div className="info">
                                <Time time={this.props.comment.get('created_at')} />

                                <span>
                                    <i className="fi-like" />
                                    {group_like_count}/{like_count}
                                </span>
                                <span>
                                    <i className="fi-dislike" />
                                    {group_dislike_count}/{dislike_count}
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