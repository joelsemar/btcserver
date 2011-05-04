app = {}


// Let the library know where WebSocketMain.swf is:
WEB_SOCKET_SWF_LOCATION = "/static/js/websocket_js/WebSocketMain.swf";
function Server(table_id){
    var that = this;
    this.game = new Game(table_id)
    this.connect = function(){
    
        var ws = new WebSocket("ws://{0}:8080/test".strFormat(domain));
        ws.onopen = function(){
            var payload = {
                action: 'register',
                table_id: table_id,
                player_id: player_id
            }
            ws.send(JSON.stringify(payload));
        };
        
        ws.onmessage = function(message){
            console.log("onmessage: " + message.data)
            try {
                var data = JSON.parse(message.data)
            } 
            catch (error) {
                debugger;
            }
            
            
            if (data.registration_success) {
                console.log("registration success");
            }
            else {
                that.game.callback(data);
            }
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

function init(table_id){
    var server = new Server(table_id);
    server.connect();
    app.server = server;
    $('#new_table_form').hide()
    app.server.game.fetch_cards()
    
}


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
    var that = this
    this.current_balance = curr_bal;
    this.player_name = name;
    this.player_id = player_id;
    this.callback = function(new_data){
        if (new_data.action) {
            that[new_data.action](new_data.data)
        }
        else {
            this.update(new_data)
        }
        console.log("Received: " + new_data)
    }
    
    this.update_game = function(game_data){
        this.update_dealer(game_data.dealer_up_cards);
        
        
    }
    this.update_dealer = function(cards){
        $('#dealer_cards').html('')
        for (var i = 0; i < cards.length; i++) {
            this.deal_dealer_card(cards[i])
        }
        
    }
    
    this.deal_card = function(card_data){
        if (card_data) {
            if (card_data.dealt_to == 'dealer') {
                this.deal_dealer_card(card_data)
            }
            else 
                if (card_data.dealt_to == self.player_id) {
                    $('#cards').append(this.get_card_html(card_data))
                }
            hide_bid_form();
            
        }
        
    }
    
    this.get_card_html = function(card_data){
        if (card_data) {
            return '<div class="card_slot card" ><img src="{0}" style="height:100%;" /></div>'.strFormat(card_data.image_url);
        }
        
    }
    
    this.deal_dealer_card = function(card_data){
        $('#dealer_cards').append(this.get_card_html(card_data))
    }
    this.show_dealer_cards = function(cards){
        $('#dealer_cards').html('')
        for (var i = 0; i < cards.length; i++) {
            delay = 0;
            if (i > 1) {
                delay = i * 500;
            }
            setTimeout(function(i){
                return function(){
                    app.server.game.deal_dealer_card(cards[i])
                }
            }(i), delay)
            
        }
        show_bid_form()
        
    }
    this.blackjack = function(data){
        tool_bar_alert('BlackJack!');
    }
    this.update_balance = function(data){
        var new_balance = data.balance;
        var balance_change = data.balance_change;
        current_balance = app.server.game.current_balance
        $("#acct_bal").html(new_balance)
        if (current_balance > new_balance) {
            tool_bar_alert("-" + balance_change, true)
        }
        else 
            if (current_balance < new_balance) {
                tool_bar_alert('+' + balance_change, false)
            }
        app.server.game.current_balance = new_balance;
    }
    
    this.fetch_cards = function(){
        $.ajax({
            url: '/btcserver/blackjack/cards/',
            headers: {
                'Accept': 'application/json'
            },
            type: 'GET',
            success: function(response){
                var cards = response.data.cards;
                if (cards.length) {
                    for (var i = 0; i < cards.length; i++) {
						card = cards[i];
						card.dealt_to = app.server.game.player_id
                        that.deal_card(card);
                    }
                    hide_bid_form();
                }
                else {
                    show_bid_form();
                }
                
                
            }
        });
    }
    this.send_action = function(action, amount, callback){
        var data = {}
        if (amount) {
            data.amount = amount;
        }
        $.ajax({
            url: '/btcserver/blackjack/table/{0}/{1}'.strFormat(that.table_id, action),
            data: data,
            type: 'POST',
            success: function(response){
                if (callback) {
                    callback(response);
                }
                
            }
        })
        
    }
    
}

function bet_button_handler(){
    $('#dealer_cards').html('')
    $('#cards .card').remove()
    app.server.game.send_action('bet', $('#bid_input').val(), bet_callback)
}

function bet_callback(response){
    if (response.success) {
        hide_bid_form();
    }
    else {
        error = response.errors[0]
        tool_bar_alert(error, true)
    }
    
}

function tool_bar_alert(msg, error){
    var options = {}
    if (error) {
        options.color = "#ff0000"
    }
    var label = $("#balance_label");
    var old_html = label.html()
    label.html(msg)
    $("#bottom_toolbar").effect("highlight", options, 2500)
    setTimeout(function(label, old_html){
        return function(){
            label.html(old_html);
        }
    }(label, old_html), 2500)
    
}


function create_table(){
    var table_name = $('#table_name').val();
    if (!table_name) {
        return false;
    }
    var is_public = $("#is_public").checked;
    var selector = $('#table_type_selector');
    var table_type_id = selector.val()
    $.ajax({
        url: '/btcserver/blackjack/table/' + table_type_id,
        headers: {
            'Accept': 'application/json'
        },
        data: {
            name: table_name
        },
        type: 'POST',
        success: function(response){
            window.location = '/blackjack/table';
            init(response.data.table_id);
            
        }
    });
    
}

function leave_table(){
    $.ajax({
        url: '/btcserver/blackjack/table/' + app.server.game.table_id,
        headers: {
            'Accept': 'application/json'
        },
        type: 'DELETE',
        success: function(response){
            window.location = '/blackjack/tables';
        }
    });
}

function hide_bid_form(){
    $("#bid_form").hide()
    $('#option_panel').show()
}

function show_bid_form(){

    $("#bid_form").show()
    $('#option_panel').hide()
}

function join_table(table_id){

}
