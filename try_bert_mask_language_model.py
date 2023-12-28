from transformers import AutoTokenizer, BertForMaskedLM
import torch

PRETRAIN_MODEL_NAME = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(PRETRAIN_MODEL_NAME)
model = BertForMaskedLM.from_pretrained(PRETRAIN_MODEL_NAME)

input_text = "巴黎是[MASK]国的[MASK]都。"
inputs = tokenizer(input_text, return_tensors="pt")

with torch.no_grad():
    logits = model(**inputs).logits

# 回傳一個 (True, False) 的 ndarray, 相等則為True, 反之亦然
is_mask_id_matched = (inputs.input_ids == tokenizer.mask_token_id)

# array.nonzero 取回非為零(為True)在'字串中的位置'
mask_token_position = is_mask_id_matched[0].nonzero(as_tuple=True)[0]
print(logits.shape)  # 一個 1 x 11 x 21128 的矩陣
print(logits[0].shape)
print(logits[0, [4, 7]].shape)  # 選擇第4,第7個token，把詞彙預測logit取出來
print(logits[0, 4])  # 第4個token的詞彙預測logit

# 對多項機率歸一化：數值變成0~1之間的機率
softmax_probs = torch.softmax(logits[0, mask_token_position], -1)

# 取前十名的機率和index
probs, indices = torch.topk(softmax_probs, 10)

for position, prob, indice in zip(mask_token_position, probs, indices):
    print(f'At {position}')
    for pred_probability, idx in zip(prob, indice):
        pred_tok = tokenizer.convert_ids_to_tokens(idx.tolist())
        round_prob = round(pred_probability.tolist() * 100, 3)
        print(f"{pred_tok}: {round_prob}%")
