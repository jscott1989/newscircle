/**
 * @jsx React.DOM
 */

var DiscussionComponent = React.createClass({
    mixins: [BackboneMixin],

    render : function() {
        var commentNodes = this.props.collection.filter(function(comment) {
            return comment.get('parent') == null;
        }).map(function (comment) {
            return <CommentComponent comment={comment} author={USERS.get(comment.get('author'))} />;
        }.bind(this));

        return (
            <div>
                {commentNodes}
                <ReplyComponent />
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

        var group_name = '';
        if (this.props.author.get('group')) {
            group_name = 'Group ' + GROUPS.get(this.props.author.get('group')).get('number');
        }

        return (
            <div className="row post">
                <div className="small-12 columns">
                    <div className="row">
                        <div className="small-2 columns person">
                            <img src="" />
                            <strong>{this.props.author.get('username')}</strong>
                            <div>{group_name}</div>
                        </div>
                        <div className="small-10 columns">
                            <div className="content">
                                <p>{this.props.comment.get('text')}</p>
                            </div>
                            <div className="info">
                                <a>aaa</a>
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
})