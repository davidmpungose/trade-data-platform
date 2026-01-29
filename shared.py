from shiny import ui

INPUTS = {
    "name":  ui.input_text("name", "Enter your name"),
    "surname": ui.input_text("surname", "Enter your surname"),
    "institution": ui.input_text("institution", "Enter your institution"),
    "email": ui.input_text("email", "Enter your email"),
    "request details": ui.input_text_area("request_details", "Enter details of your request", rows=5)
}