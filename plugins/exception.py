

regex1 = r'botmily crash'

def raise_exception_trigger(message_data,bot):
    raise Exception('test')
    
def raise_exception_command(message_data, bot):
    raise Exception('test')

commands = {"exception_test": raise_exception_command}
triggers = [(regex1, raise_exception_trigger)]

