from webservice_tools.utils import BaseHandler
from webservice_tools.decorators import login_required
from backend.models import Seat
from blackjack.models import BlackJackHand, BlackJackTable, BlackJackTableType
from backend.handlers import BaseCardsHandler
from decimal import Decimal, InvalidOperation
from django.db.models import F

class BlackJackTablesHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BlackJackTable
    extra_fields = ('num_seats', 'num_available_seats', 'players')
    
    @login_required
    def read(self, request, response):
        """
        Fetch all the active blackjack tables
        API Handler: GET /blackjack/tables
        """
        tables = BlackJackTable.objects.all()
        response.set(tables=tables)
        return response.send()


class BlackJackTableHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = BlackJackTable
    extra_fields = ('num_seats', 'num_available_seats', 'players')
    
    def read(self, request, id, response):
        """
        Return table state.
        API Handler: GET  /blackack/table/{id}
        Params:
          id [id] id of the table
        """
        try:
            table = BlackJackTable.objects.get(id=id)
        except BlackJackTable.DoesNotExist:
            return response.send(errors='Table not found', status=404)
        
        response.set(table=table)
        return response.send()
    
    @login_required
    def create(self, request, id, response):
        """
        Create a new BlackJack Table
        API Handler: POST /blackjack/table/{id}
        PARMS:
            id [id] identifier for the type of table you'd like to create
            name [string] Name for this table
        """
        try:
            table_type = BlackJackTableType.objects.get(id=id)
        except BlackJackTableType.DoesNotExist:
            return response.send(errors='Invalid table type')
        
        name = request.POST.get('name')
        if not name:
            return response.send(errors="Please provide a name")
        
        table = BlackJackTable.objects.create(type=table_type, name=name)
        seat = table.available_seats[0]
        seat.player = request.user.get_profile()
        seat.save()
        response.set(table_id=table.id)
        return response.send()
        

    @login_required
    def update(self, request, id, response):
        """
        Attempt to join a table
        API Handler: PUT  /blackack/table/{id}/join
        Params:
          id [id] id of the table you are trying to join
        """
        player = request.user.get_profile()
        try:
            table = BlackJackTable.objects.get(id=id)
        except BlackJackTable.DoesNotExist:
            return response.send(errors="Table not found", status=404)
        
        seats = table.available_seats
        if not seats:
            return response.send(errors="No seats available!", status=404)
        
        try:
            current_seat = Seat.objects.get(player=player)
            return response.send(errors='You appear to be already setting at Table %s,\
                                         if this is not right, try logging out and logging back in.' % current_seat.table.name)
        except Seat.DoesNotExist:
            pass
        
        seat = seats[0]
        seat.player = request.user.get_profile()
        seat.save()
        table.update_game()
        return response.send(status=201)

    @login_required
    def delete(self, request, id, response):
        """
        Leave Table
        API Handler: DELETE /blackjack/table/{id}
        """
        player = request.user.get_profile()
        try:
            table = BlackJackTable.objects.get(id=id)
        except BlackJackTable.DoesNotExist:
            return response.send(errors="Table not found", status=404)
        
        seats = table.seats
        try:
            current_seat = [s for s in seats if s.player == player][0]
        except IndexError:
            return response.send()
        current_seat.player = None
        current_seat.save()
        if table.current_turn == current_seat:
            table.next_turn()
        table.update_game()
        
        return response.send()

class BlackJackTableTypesHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BlackJackTableType
    @login_required
    def read(self, request, response):
        """
        Return a list of all available blackjack table types
        API Handler: GET /blackjack/tabletypes
        """
        response.set(types=BlackJackTableType.objects.all())
        return response.send()


class CardsHandler(BaseCardsHandler):
    HAND_MODEL = BlackJackHand
        
        
class PlayerActionHandler(BaseHandler):
    allowed_methods = ('POST',)
    possible_actions = ('hit', 'stand', 'double', 'split', 'bet', 'surrender')
    
    def create(self, request, id, action, response):
        """
        API Handler: POST /blackjack/table/{id}/{action}
        
        Params:
            @amount[decimal] amount to bet, to 8 digits
        """
        player = request.user.get_profile()
        if action not in self.possible_actions:
            return response.send(status=404)
        
        try:
            table = BlackJackTable.objects.get(id=id)
        except BlackJackTable.DoesNotExist:
            return response.send(errors="Not found", status=404)
        
        try:
            player_seat = [s for s in table.seats if s.player == player][0]
        except IndexError:
            return response.send(errors="You aren't sitting at that table", status=500)
        
        if action != 'bet' and (table.current_turn != player_seat):
            return response.send(errors="It's not your turn!", status=505)
        
        return getattr(self, action)(request, response, player, table)
    
    def bet(self, request, response, player, table):
        amount = request.POST.get('amount')
        try:
            if  Decimal(amount) > player.balance:
                return response.send(errors="Insufficient funds", status=500)
        except (InvalidOperation, TypeError):
            return response.send(errors="Invalid Amount", status=505)
        
        round = table.current_round
        if round and round.taking_bets:
            try:
                BlackJackHand.objects.get(player=player, round=round)
                return response.send(errors="You've already bet on this hand")
            except BlackJackHand.DoesNotExist:
                BlackJackHand.objects.create(player=player, round=round, bet=amount)
                return response.send()
            
        return response.send(status=500)
    
    def hit(self, request, response, player, table):
        available_actions = ['hit', 'stand']
        try:
            current_hand = BlackJackHand.objects.get(player=player, round=table.current_round, resolved=False)
        except BlackJackHand.DoesNotExist:
            return response.send(status=404)
        
        if current_hand.doubled:
            return response.send(status=499)
        
        current_hand.add_card(table.pull_card())
        table.save()
        if current_hand.busted:
            current_hand.available_actions = '[]'
            current_hand.lost()
            current_hand.round.table.next_turn()
        
        current_hand.set_available_actions(available_actions)
        response.set(available_actions=available_actions)
        
        return response.send()
    
    
    def stand(self, request, response, player, table):
        table.next_turn()
        response.set(available_actions=[])
        return response.send()
    
    
    def double(self, request, response, player, table):
        """
        Double the user's current bet, no further action is allowed by this user
        """
        available_actions = ['hit','stand']
        try:
            current_hand = BlackJackHand.objects.get(player=player, round=table.current_round, resolved=False)
        except BlackJackHand.DoesNotExist:
            return response.send(status=404)
        
        if current_hand.doubled:
            return response.send(status=499)
        
        current_hand.bet = current_hand.bet * Decimal(2)
        current_hand.doubled = True
        current_hand.save()
        
        current_hand.add_card(table.pull_card())
        table.save()
        if current_hand.busted:
            current_hand.lost()
        current_hand.round.table.next_turn()
        current_hand.set_available_actions(available_actions)
        response.set(available_actions=available_actions)
        return response.send()
     
    def surrender(self, request, response, player, table):
        available_actions = []
        try:
            current_hand = BlackJackHand.objects.get(player=player, round=table.current_round, resolved=False)
        except BlackJackHand.DoesNotExist:
            return response.send(status=404)
        
        current_hand.bet = current_hand.bet / Decimal(2)
        current_hand.save()
        current_hand.lost()
        current_hand.round.table.next_turn()
        
        response.set(available_actions=available_actions)
        return response.send()
          

class BlackJackGameDataHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    @login_required
    def read(self, request, id, response):
        try:
            table = BlackJackTable.objects.get(id=id)
        except BlackJackTable.DoesNotExist:
            response.send(errors='Not found', status=404)
        
        response.set(game_data=table.get_game_data())
        return response.send()
