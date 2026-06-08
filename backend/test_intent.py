from app.services.intent_engine import detect_intent
from app.services.entity_engine import extract_entities
from app.services.tag_engine import generate_tags

text = "Call Rahul tomorrow at 5 PM regarding internship."

intent = detect_intent(text)
entity=extract_entities(text)
tags=generate_tags(text)
print('intent:',intent)
print('entity:',entity)
print('tags:',tags)




