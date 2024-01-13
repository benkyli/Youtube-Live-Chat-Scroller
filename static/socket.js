// When clicking the "start scrolling" button, connect to websocket and emit the scroll event
const socket = io();

$("#scroll").click(function(){
    socket.connect();
    socket.emit("scroll");
});


socket.on("message", function(details) {
    // Create message string
    var span = document.createElement("span");
    var message = document.createTextNode(details["user"] + ": " + details["message"]);
    span.appendChild(message);

    // create a new div, set class, then insert the new message
    var div = document.createElement("div");
    div.setAttribute("class", "marquee");
    div.appendChild(span);

    // Get scroll container and set message height position
    var container = $('#scroll_container');
    var height = Math.floor(Math.random() * container.height());
    div.style.bottom = height + "px";


    // Create insertion point for new message
    var $parent = $('#scroll_container');
    var $children = $parent.children();             // get possible children
    var n = $children.length;                       // there are n children
    var pos = Math.floor((n + 1) * Math.random());  // and n+1 insert points

    if (n === pos) {
        $parent.append(div);                        // append after last
    } else { 
        $children[pos].before(div);                 // or insert before
    }
    
    // Add event listener to delete the message div when the scroll animation ends.
    $(div).one("animationend", function() {
        $(this).remove();
    });
})