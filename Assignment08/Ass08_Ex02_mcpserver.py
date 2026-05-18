from fastmcp import FastMCP
from datetime import datetime
from typing import Optional

# Create MCP server
mcp = FastMCP("MyHTTPTools",
              instructions="This is a simple HTTP tool server that acts as a support ticketing system. It can create support tickets based on user issues."
              "Use create_ticket function to open a new ticket for an entirely new task or a subtask of an alsready existing one."
              "Use edit_ticket function to edit an already existing tickets details."
              "And use query_ticket to query the status and details of a ticket.")

# Ticket storage
_tickets = {}
_next_id = 1


# Define tools
# creating ticket for task/subtask
@mcp.tool()
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    global _next_id
    ticket_id = _next_id
    _next_id += 1

    _tickets[ticket_id] = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    return (
        f"Ticket #{ticket_id} created.\n"
        f"  Title:    {title}\n"
        f"  Priority: {priority}\n"
        f"  Status:   open"
    )

# editing the ticket
@mcp.tool()
def edit_ticket(
    ticket_id: int,
    status: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> str:
    

    if ticket_id not in _tickets:
        return f"Error: The ticket #{ticket_id} could not be found."

    ticket = _tickets[ticket_id]
    changes = []

    if status is not None:
        ticket["status"] = status
        changes.append(f"status → {status}")
    if title is not None:
        ticket["title"] = title
        changes.append(f"title → {title}")
    if description is not None:
        ticket["description"] = description
        changes.append("description updated")
    if priority is not None:
        ticket["priority"] = priority
        changes.append(f"priority → {priority}")

    ticket["updated_at"] = datetime.now().isoformat()

    if not changes:
        return f"Ticket #{ticket_id}: no changes requested."

    return f"Ticket #{ticket_id} updated: {', '.join(changes)}."


@mcp.tool()
def query_ticket(ticket_id: int) -> str:
    if ticket_id not in _tickets:
        return f"Ticket #{ticket_id}: no changes requested."

    t = _tickets[ticket_id]
    return (
        f"Ticket #{t['id']}\n"
        f"  Title:       {t['title']}\n"
        f"  Description: {t['description']}\n"
        f"  Priority:    {t['priority']}\n"
        f"  Status:      {t['status']}\n"
        f"  Created:     {t['created_at']}\n"
        f"  Updated:     {t['updated_at']}"
    )

# Run as HTTP server
if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000
    )