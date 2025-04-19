from moderation.analyzer import is_message_inappropriate

message = "On va parler de violence"
banned = ["violence", "politique", "drogue"]

result = is_message_inappropriate(message, banned)
print("Message inapproprié :", result)
