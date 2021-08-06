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
        handler_input.response_builder.speak("Ups, das hat nicht geklappt, Thomas")
        return handler_input.response_builder.response

# Chinese Animal Test-Intent - funktioniert
#
class ChineseAnimalIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ChineseAnimalIntent")(handler_input)
    
    def handle(self, handler_input):
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

# Chinese Animal Test-Intent - ENDE


class getEmployeeCostCenterHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("getEmployeeCostCenter")(handler_input)

    def handle(self, handler_input):
        empl_no = handler_input.request_envelope.request.intent.slots['intent_year'].resolutions.resolutions_per_authority[0].values[0].value.id
#         empl_id = handler_input.request_envelope.request.intent.slots['intent_year'].value
        try:
            data = ddb.get_item(
                TableName="smart_empl_costcenter",
                Key={
                    'empl_id': {
                        'N': empl_no
                    }
                }
            )
        except BaseException as e:
            print(e)
            raise(e)

        #slotValue = handler_input.request_envelope.request.intent.slots['slotName'].value
        speech_text = data['Item']['empl_name']['S'] + " hat die Kostenstelle" + data['Item']['empl_costcenter_id']['S'] + '. Möchtest du mehr wissen? Die Kostenstelle heißt ' + data['Item']['empl_costcenter_name']['S']+ '. ' + data['Item']['empl_name']['S'] + 'arbeitet für die' + data['Item']['empl_company_name']['S'] + 'am Standort ' + data['Item']['empl_location_name']['S'] + '.';
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(ChineseAnimalIntentHandler())
sb.add_request_handler(getEmployeeCostCenterHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)