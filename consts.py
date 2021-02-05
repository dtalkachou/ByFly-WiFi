CSRF_TOKEN_NAME = 'csrfmiddlewaretoken'

BASE_URL = 'https://ciscowifi.beltelecom.by/'
CONNECT_URL = BASE_URL + 'connect_by_card/'
DISCONNECT_URL = BASE_URL + 'disconnect/'

# Messages
INVALID_CONFIG_MESSAGE = 'Invalid config file'
DISCONNECTED_MESSAGE = 'Disconnected'
UNKNOWN_BEHAVIOR_MESSAGE = 'Unknown behavior' 

# Cookies
MESSAGES_COOKIE_NAME = 'messages'

# ArgumentParser
ARGUMENT_PARSER_DESCRIPRION = 'Quck interaction with ciscowifi.beltelecom.by'

ARGUMENT_PARSER_ACTION_CONNECT_CHOICES = ('c', 'connect')
ARGUMENT_PARSER_ACTION_DISCONNECT_CHOICES = ('d', 'disconnect')
ARGUMENT_PARSER_ACTION_CHOICES = (
    *ARGUMENT_PARSER_ACTION_CONNECT_CHOICES,
    *ARGUMENT_PARSER_ACTION_DISCONNECT_CHOICES
)
ARGUMENT_PARSER_ACTION_HELP = 'action for cisowifi.beltelecom.by'