#pip install translate
from translate import Translator
import time

KE_translator=Translator(from_lang="Korean", to_lang="English")
EK_translator=Translator(from_lang="English", to_lang="Korean")

input_KE="당신은 그리핀도르로 배정되었습니다."
start=time.time()
KE_example=KE_translator.translate(input_KE)
inference_1=time.time()-start

input_EK="You are assgined as Griffindor."
start=time.time()
EK_example=EK_translator.translate(input_EK)
inference_2=time.time()-start

print("KE_example Inference time: ",inference_1)
print("input text: ", input_KE)
print("KE_example: ", KE_example)

print("\n============================\n")
print("EK_example Inference time: ",inference_2)
print("input text: ", input_EK)
print("EK_example: ",EK_example)

