app = {}
var noop = function(){
}
var ON_ENTER_CALLBACK = noop;
var ON_ESC_CALLBACK = noop;
var ACTIONS = ['hit', 'stand', 'double', 'split', 'surrender']
$(document).keydown(function(e){
    if (e.keyCode == 13) {
        ON_ENTER_CALLBACK()
        return false;
    }
    if (e.keyCode == 27) {
        ON_ESC_CALLBACK();
        return false;
    }
});

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

var ChatBox = {
    open: function(){
        $("#chat_form").show();
        ON_ENTER_CALLBACK = ChatBox.send;
        ON_ESC_CALLBACK = ChatBox.close;
        $("#chat_input").focus()
        
    },
    send: function(){
        $.ajax({
            url: '/btcserver/table/{0}/chat'.strFormat(app.server.game.table_id),
            headers: {
                'Accept': 'application/json'
            },
            type: 'POST',
            data: {
                'message': $('#chat_input').val()
            },
            success: function(response){
                ChatBox.close();
                $('#chat_input').val('')
            }
        });
    },
    close: function(){
        $("#chat_form").hide();
        ON_ENTER_CALLBACK = ChatBox.open;
        ON_ESC_CALLBACK = noop;
    },
    chat_received: function(data){
        var chat_log = $("#chat_log_inner")
        chat_log.append(this.get_chat_html(data))
        chat_log.attr('scrollTop', chat_log.attr('scrollHeight'), 3000);
    },
    get_chat_html: function(data){
        var html = "<div class='chat_entry'>";
        html += "<span class='chat_entry_label'>{0}:</span>";
        html += "<span class='chat_entry_text'>{1}</span>";
        return html.strFormat(data.from_name, data.message)
    }
}

function Player(name, id){
    this.name = name;
    this.id = id;
    this.hand = [];
    this.seat_id = seat_id;
}

function Game(table_id){
    this.table_id = table_id;
    this.players = [];
    this.dealers_hand = [];
    var that = this;
    this.current_balance = curr_bal;
    this.player_name = name;
    this.player_id = player_id;
    this.game_state = 'bidding';
    
    $.ajax({
        url: '/btcserver/blackjack/table/{0}/game_data'.strFormat(table_id),
        headers: {
            'Accept': 'application/json'
        },
        type: 'GET',
        success: function(response){
            var game_data = response.data.game_data;
            that.update_game(game_data);
            if (game_data.dealer_up_cards) {
                that.init_dealer(game_data.dealer_up_cards);
            }
            
            
        }
    });
    
    
    this.callback = function(new_data){
        if (new_data.action) {
            that[new_data.action](new_data.data);
        }
        else {
            this.update(new_data);
        }
        console.log("Received: " + new_data);
    }
    
    this.update_game = function(game_data){
        ///this.update_dealer(game_data.dealer_up_cards);
        this.update_game_state(game_data.game_state);
        this.update_players(game_data.seats);
        
    }
    
    this.update_game_state = function(state){
        that.game_state = state;
        if (state == 'bidding') {
            $("#bid_form").show();
            $('#option_panel').hide();
            ON_ENTER_CALLBACK = bet_button_handler;
        }
        else 
            if (state == 'playing') {
                $("#bid_form").hide();
                $('#option_panel').show();
                ON_ENTER_CALLBACK = ChatBox.open;
            }
    }
    
    this.init_dealer = function(cards){
        for (var i = 0; i < cards.length; i++) {
            var card = cards[i];
            card.dealt_to = 'dealer';
            this.deal_card(card)
        }
        
    }
    
    
    this.update_players = function(player_data){
        for (var i = 0; i < player_data.length; i++) {
            var player = player_data[i];
            var tab = $("#player_tab_pos_{0}".strFormat(player.position));
            if (player.player_id == player_id && player.available_actions) {
                app.server.game.update_available_actions(player.available_actions)
            }
            if (tab && player.player_id) {
                tab.html(this.player_tab_html(player));
                if (player.current_turn) {
                    tab.addClass('current_turn');
                }
                else {
                    tab.removeClass('current_turn');
                }
            }
            else {
                tab.html('Empty Seat');
                tab.removeClass('current_turn');
            }
        }
        if (!$('.current_turn').length && that.game_state == 'playing' && player_data.length > 1) {
            $("#option_panel").effect("highlight", {}, 2500)
            
        }
        
    }
    this.player_tab_html = function(player){
        html = "<span class='player_tab_name'>";
        html += player.player_name;
		html += "</span>"
		if (player.player_id == player_id){
			
			html += "<div id='balance_label'>";
			html += "<span id='acct_bal'>{0}</span> BTC".strFormat(curr_bal);
			html += "<div>";
		}
        html += "<div class='player_tab_cards'>";
        if (player.cards) {
            for (var i = 0; i < player.cards.length; i++) {
                var img_class = 'player_card';
                
                html += "<img class='player_card' src='{0} />".strFormat(player.cards[i].image_url);
            }
        }
        html += "</div>";
        html += "</span>";
        return html
        
    }
    
    
    this.deal_card = function(card_data){
        if (card_data) {
            if (card_data.dealt_to == 'dealer') {
                $('#dealer_cards').append(this.get_card_html(card_data))
            }
            else 
                if (card_data.dealt_to == self.player_id) {
                    $('#cards').append(this.get_card_html(card_data))
                }
            
        }
        
    }
    
    this.get_card_html = function(card_data){
        var dom_id = card_data.id || "down_card";
        return '<div class="card_slot card" id="{1}" ><img src="{0}" style="height:100%;" /></div>'.strFormat(card_data.image_url, dom_id);
        
    }
    
    this.flip_down_card = function(card_data){
        $("#down_card").html('<img src="{0}" style="height:100%;" /></div>'.strFormat(card_data.image_url))
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
                }
            }
        });
    }
    this.send_action = function(action, amount, callback){
        var data = {}
        var callback = callback || noop;
        if (amount) {
            data.amount = amount;
        }
        $.ajax({
            url: '/btcserver/blackjack/table/{0}/{1}'.strFormat(that.table_id, action),
            data: data,
            type: 'POST',
            success: function(response){
                if (response && response.data.hasOwnProperty('available_actions')) {
                    var available_actions = response.data.available_actions;
                    app.server.game.update_available_actions(available_actions);
                }
                callback(response);
                if (response.errors.length) {
                    tool_bar_alert(response.errors[0], true)
                }
            }
        })
        
    }
    
    this.chat = function(data){
        ChatBox.chat_received(data);
    }
    
    this.update_available_actions = function(available_actions){
        for (var i = 0, l = ACTIONS.length; i < l; i++) {
            var action = ACTIONS[i];
            var button = $("#{0}_option".strFormat(action))
            if (available_actions.includes(action)) {
                button.show();
            }
            else {
                button.hide();
            }
        }
    }
    
    
}

function bet_button_handler(){
    $('#dealer_cards').html('')
    $('#cards .card').remove()
    app.server.game.send_action('bet', $('#bid_input').val(), bet_callback)
}

function bet_callback(response){
    if (response.success) {
        $("#bid_form").hide();
    }
    else {
        error = response.errors[0]
        tool_bar_alert(error, true)
    }
    
}

function tool_bar_alert(msg, error){
    var options = {color: '#4444444'}
    if (error) {
        options.color = "#ff0000"
    }
    var label = $("#message_bar");
    var old_html = label.html()
    label.html(msg)
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

