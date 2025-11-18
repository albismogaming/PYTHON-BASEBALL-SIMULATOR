from CONTEXT.TICKET_CONTEXT import Ticket
from CONTEXT.PLAY_CONTEXT import PlayContext


class MatchupTicketGenerator:
    """
    Generates Tickets by wrapping PlayContext objects.
    Simple factory - outcome executors create PlayContext, this wraps it in a Ticket.
    """
    
    @staticmethod
    def generate_ticket(play_context):
        """
        Generate a ticket from a PlayContext (returned by outcome executors).
        
        Args:
            play_context: PlayContext object with all play details
            
        Returns:
            Ticket: Ticket wrapping the play context
        """
        return Ticket(play_context=play_context)
    