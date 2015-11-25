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

setInterval(updatenotifications, 15000);

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