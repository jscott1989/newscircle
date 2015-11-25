/**
 * @jsx React.DOM
 */

/**
 * React for managing notifications
 */

 var Notification = Backbone.Model.extend({
    defaults : {
        created_time       : null,
        html               : null,
        read               : null
    },
});

 var Notifications = Backbone.Collection.extend({
    url: '/1/notifications',
    // The /1/ was just so I didn't have to change the API router
    model: Notification,

    parse: function(d) {
        return d.results;
    }
});

NOTIFICATIONS = new Notifications(STARTING_NOTIFICATIONS, {mode: "client"})

function updatenotifications() {
    NOTIFICATIONS.fetch({update: true});
}

setInterval(updatenotifications, 5000);

var NotificationList = React.createClass({
   mixins: [BackboneMixin],
   render: function() {
    var notifications = this.props.collection.slice(0, 3);
       var notificationNodes = notifications.map(function (notification) {
           return <NotificationComponent notification={notification} />;
       });

       return <ul>
           {{notificationNodes}}
       </ul>
   }
});

var RecentNotifications = React.createClass({
    componentDidMount: function() {
        var self = this;
        this.interval = setInterval(function() {self.setState({});}, 1000);
    },
    componentWillUnmount: function() {
        clearInterval(this.interval);
    },

    render: function() {
        var notifications = _.sortBy(this.props.collection.filter(function(notification) {
            if (notification.get('read')) return false;
            var m = moment(notification.get('created_time'), "YYYY-MM-DDTHH:mm:ss.S");
            return m.add(15, 'seconds').isAfter();
        }), function(notification) {
            return notification.get('created_time');
        });

        var notificationNodes = notifications.map(function (notification) {
            return <NotificationComponent notification={notification} />;
        });

        return <ul class="notifications">
            {{notificationNodes}}
        </ul>
    }
})

var NotificationComponent = React.createClass({
   render: function() {
        return <li>
                    <a href={this.props.notification.get('main_link')}>
                        <div className="row">
                            <div className="small-1 columns" style={{padding: 0, 'padding-top': '1em'}} dangerouslySetInnerHTML={{__html: this.props.notification.get('image')}}></div>
                            <div className="small-11 columns">
                                <div dangerouslySetInnerHTML={{__html: this.props.notification.get('short')}}></div>
                            </div>
                        </div>
                        <div className="notification-time"><Time time={this.props.notification.get('created_time')} /></div>
                    </a>
               </li>;
   }
});

var NotificationButton = React.createClass({
    mixins: [BackboneMixin],
    render: function() {
        unread_count = this.props.collection.filter(function(n) {
            return n.get('read') == false;
        }).length;
        if (unread_count > 0) {
            return <div><i className="fi-clipboard"></i>
                    <span className="alert round label">{unread_count}</span></div>
        } else {
            return <div><i className="fi-clipboard"></i></div>
        }
    }
})

React.render(
   <NotificationList collection={NOTIFICATIONS} />,
   document.getElementById("notifications-list")
);

React.render(
   <NotificationButton collection={NOTIFICATIONS} />,
   document.getElementById("notifications-button")
);

React.render(
   <RecentNotifications collection={NOTIFICATIONS} />,
   document.getElementById("recent-notifications")
);


$("#notifications-button").hover(function() {
    unread_count = NOTIFICATIONS.filter(function(n) {
            return n.get('read') == false;
    }).length;

    if (unread_count > 0) {
        $.post("/notifications/read");
        NOTIFICATIONS.each(function(notification) {
            notification.set('read', true);
        });
    }
});