import re

eachProvider = {}

def processProvider(threads):
    for each_message in threads:
        print(each_message)
        sender = each_message["sender_email_id"]
        content = each_message["text_content"]

        # Extract only the question (assuming it's marked with '?') and remove special characters except numbers and '.'
        question = re.findall(r'[\n]', content)
        cleaned_questions = [re.sub(r'[^a-zA-Z0-9.\s]', '', q) for q in question]

        if sender in eachProvider:
            eachProvider[sender].extend(question)
        else:
            eachProvider[sender] = question

        if len(eachProvider) > 2:
            break
    return eachProvider
