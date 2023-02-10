# pip install googletrans==3.1.0a0
import googletrans
from googletrans import Translator
import time

# print("Supported Languge List")
# print(googletrans.LANGUAGES)  #ko: korean , en: english

translator=Translator()



input_KE="당신은 그리핀도르로 배정되었습니다."
start=time.time()
KE_example=translator.translate(input_KE, src='ko', dest='en')
inference_1=time.time()-start

input_EK="You are assgined as Griffindor."
start=time.time()
EK_example=translator.translate(input_EK,  src='en', dest='ko')
inference_2=time.time()-start



print("KE_example Inference time: ",inference_1)
# print("KE_example: ",KE_example.src)
# print("KE_example: ",KE_example.dest)
print("input text: ", input_KE)
print("KE_example: ",KE_example.text)

print("\n============================\n")
print("EK_example Inference time: ",inference_2)
# print("EK_example: ",EK_example.src)
# print("EK_example: ",EK_example.dest)
print("input text: ", input_EK)
print("EK_example: ",EK_example.text)

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-t", "--task", type=str, help="NLP task")
#     parser.add_argument("-m", "--model", type=str, help="NLP model for task in model card")
#     parser.add_argument("-p", "--project_id", type=str, help="Google Pub/Sub Project ID")
#     parser.add_argument("-s", "--subscription_id", type=str, help="Google Pub/Sub subscription ID")
#     parser.add_argument("--topic_id", type=str, help="Google Pub/Sub Topic ID")
#     args = parser.parse_args()

#     controller = NLPTaskController(
#         args.task, args.model, project_id=args.project_id, topic_id=args.topic_id
#     )
#     controller.eventsub(args.subscription_id)