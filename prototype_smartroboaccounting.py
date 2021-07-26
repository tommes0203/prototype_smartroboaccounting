import boto3
ddb = boto3.client("dynamodb")
import boto3
ddb = boto3.client("dynamodb")
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Herzlich Willkommen ").set_should_end_session(False)
        return handler_input.response_builder.response    

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Ups there was an error, Thomas")
        return handler_input.response_builder.response

class ChineseAnimalIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ChineseAnimalIntent")(handler_input)
        try:
            data = ddb.get_item(
                TableName="ChineseAnimal",
                Key={
                    'BirthYear': {
                        'N': year
                    }
                }
            )
        except BaseException as e:
            print(e)
            raise(e)
        year = handler_input.request_envelope.request.intent.slots['year'].value
        
        try:
            data = ddb.get_item(
                TableName="ChineseAnimal",
                Key={
                    'BirthYear': {
                        'N': year
                    }
                }
            )
        except BaseException as e:
            print(e)
            raise(e)

        speech_text = "Das gesuchte Tier ist ein " + data['Item']['Animal']['S'] + '. Möchtest du mehr wissen? Die Eigenschaften sind ' + data['Item']['PersonalityTraits']['S']
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response      

class getEmployeeCostCenterHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("getEmployeeCostCenter")(handler_input)
        empl_name = handler_input.request_envelope.request.intent.slots['empl_name'].value
        

        except BaseException as e:
            print(e)
            raise(e)

        speech_text = "Das gesuchte Tier ist ein " + data['Item']['Animal']['S'] + '. Möchtest du mehr wissen? Die Eigenschaften sind ' + data['Item']['PersonalityTraits']['S']
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response      


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(ChineseAnimalIntentHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)