import torch
from transformers import AutoTokenizer, BertForSequenceClassification

EMOTION_MODEL_NAME = "textattack/bert-base-uncased-yelp-polarity"
tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(EMOTION_MODEL_NAME)

input_text = "Hello, my dog is cute"
inputs = tokenizer(input_text, return_tensors="pt")

with torch.no_grad():
    logits = model(**inputs).logits

predicted_class_id = logits.argmax().item()
label_name = model.config.id2label[predicted_class_id]
print(label_name)
