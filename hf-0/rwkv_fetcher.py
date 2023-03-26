#from transformers import AutoModel

# '''https://huggingface.co/BlinkDL/rwkv-4-pile-7b/blob/main/RWKV-4-Pile-7B-Instruct-test4-20230326.pth'''
#m0 = AutoModel.from_pretrained('BlinkDL/rwkv-4-pile-7b/RWKV-4-Pile-7B-Instruct-test4-20230326.pth')

from huggingface_hub import hf_hub_download

REPO_ID = 'BlinkDL/rwkv-4-pile-7b'
FN = 'RWKV-4-Pile-7B-Instruct-test4-20230326.pth'

hf_hub_download(REPO_ID, FN)