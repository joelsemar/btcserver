app = {}


// Let the library know where WebSocketMain.swf is:
WEB_SOCKET_SWF_LOCATION = "/static/js/websocket_js/WebSocketMain.swf";
function Server(game){
    that = this;
    this.game = game;
    this.connect = function(){
    
        var ws = new WebSocket("ws://{0}:8080/test".strFormat(domain));
        ws.onopen = function(){
            var payload = {
                action: 'register',
                table_id: game.table_id
            }
            ws.send(JSON.stringify(payload));
        };
        
        ws.onmessage = function(e){
            that.game.callback(e.data);
        };
        ws.onclose = function(){
            console.log("closed");
        };
        that.socket = ws;
    };
    
    this.send = function(data){
        this.socket.send(JSON.stringify(data))
    }
    
    
}

$(document).ready(function(){

    var game = new Game(2);
    var server = new Server(game);
    server.connect();
    app.game = game;
    app.server = server;
	
});


function Player(name, id){
    this.name = name;
    this.id = id;
    this.hand = []
    this.seat_id = seat_id;
}

function Game(table_id){
    this.table_id = table_id;
    this.players = []
    this.dealers_hand = []
    
    
    this.callback = function(new_data){
		console.log("Received: "  + new_data)
	}
}

