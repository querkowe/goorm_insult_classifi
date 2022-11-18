import torch

from django.conf import settings

def predict_sent(sent):

    # settings.py에서 상수로 가지고 있는 모델과 토크나이저 활용
    model = settings.KNAVE_MODEL
    tokenizer = settings.KNAVE_TOKENIZER
    # 쿠다 장치 설정
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    # 입력된 문장 토크나이징
    tokenized_sent = tokenizer(
        sent,
        return_tensors="pt",
        truncation=True,
        add_special_tokens=True,
        max_length=128
    )

    # 모델이 위치한 GPU로 이동
    tokenized_sent.to(device)

    # 예측
    with torch.no_grad():
        outputs = model(
            input_ids=tokenized_sent["input_ids"],
            attention_mask=tokenized_sent["attention_mask"],
            token_type_ids=tokenized_sent["token_type_ids"]
        )

    # 결과 return
    logits = outputs[0]

    logits = logits.detach().cpu()
    result = logits.argmax(-1)

    if result == 0:
        result = 0
    elif result == 1:
        result = 1

    return result
