from webservice_tools.utils import BaseHandler
from webservice_tools.decorators import login_required
from backend.models import Player
from btcblackjack.models import BlackJackTable, BlackJackTableType


class BlackJackTablesHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = BlackJackTable
    extra_fields = ('num_seats', 'num_available_seats')
    
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
    extra_fields = ('num_seats', 'num_available_seats')
    
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
        """
        try:
            table_type = BlackJackTableType.objects.get(id=id)
        except BlackJackTableType.DoesNotExist:
            return response.send(errors='Invalid table type')
        
        table = BlackJackTable.objects.create(type=table_type)
        seat = table.available_seats[0]
        seat.player = request.user.get_profile()
        seat.save()
        return response.send()
        

    @login_required
    def update(self, request, id, response):
        """
        Attempt to join a table
        API Handler: PUT  /blackack/table/{id}/join
        Params:
          id [id] id of the table you are trying to join
        """
        try:
            table = BlackJackTable.objects.get(id=id)
        except BlackJackTable.DoesNotExist:
            return response.send(errors="Table not found", status=404)
        
        seats = table.available_seats
        if not seats:
            return response.send(errors="No seats available!", status=404)
        
        seat = seats[0]
        seat.player = request.user.get_profile()
        seat.save()
        return response.send(status=201)


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
